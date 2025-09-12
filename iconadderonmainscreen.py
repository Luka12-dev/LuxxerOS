from typing import Optional, List
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication, QMenu
)
from PyQt6.QtGui import (
    QPixmap, QColor, QMouseEvent, QDragEnterEvent, QDropEvent,
    QDrag, QFont, QIcon, QImage, QPainter
)
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal, QSize, QMimeData
import sys

# IconItem
class IconItem(QWidget):
    def __init__(self, name: str, pixmap: Optional[QPixmap] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.name = name
        self.selected = False

        cell_size = getattr(parent, "cell_size", 72)
        icon_size = min(54, cell_size - 22)

        # icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if pixmap and not pixmap.isNull():
            self.icon_label.setPixmap(pixmap.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            ic = QIcon.fromTheme("application-x-executable")
            pm = ic.pixmap(icon_size, icon_size)
            if pm.isNull():
                pm = QPixmap(icon_size, icon_size)
                pm.fill(QColor(200, 200, 200))
            self.icon_label.setPixmap(pm)

        # label
        self.text_label = QLabel(self.name)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setFont(QFont("Segoe UI", 10))
        self.text_label.setFixedHeight(36)

        # layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

        self.setFixedSize(QSize(cell_size, cell_size))
        self._update_style()
        self._drag_start_pos: Optional[QPoint] = None

    def mouseDoubleClickEvent(self, ev):
        try:
            parent = self.parentWidget()
            while parent and not hasattr(parent, "icon_activated"):
                parent = parent.parentWidget()
            if parent and hasattr(parent, "icon_activated"):
                parent.icon_activated.emit(self.name)
        except Exception:
            pass
        super().mouseDoubleClickEvent(ev)

    def sizeHint(self) -> QSize:
        return self.size()

    def set_selected(self, value: bool):
        self.selected = value
        self._update_style()

    def _update_style(self):
        if self.selected:
            self.setStyleSheet("background: rgba(0,120,215,0.12); border-radius:6px;")
        else:
            self.setStyleSheet("background: transparent;")

    # drag support

    def mouseMoveEvent(self, ev: QMouseEvent):
        if ev.buttons() & Qt.MouseButton.LeftButton and self._drag_start_pos:
            if (ev.pos() - self._drag_start_pos).manhattanLength() > QApplication.startDragDistance():
                mime = QMimeData()
                mime.setText(self.name)
                drag = QDrag(self)
                drag.setMimeData(mime)
                drag.setPixmap(self.grab())
                drag.exec(Qt.DropAction.CopyAction)
        super().mouseMoveEvent(ev)

# IconAdderArea
class IconAdderArea(QWidget):
    icon_added = pyqtSignal(str, int, QPoint)
    icon_activated = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None, cell_size: int = 96, spacing: int = 12):
        super().__init__(parent)
        self.icons: List[IconItem] = []
        self.cell_size = max(64, cell_size)
        self.spacing = max(6, spacing)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._cols = 1

    def mousePressEvent(self, ev: QMouseEvent):
        child = self.childAt(ev.pos())
        icon_widget = self._find_icon_parent(child)

        if ev.button() == Qt.MouseButton.RightButton and icon_widget:
            if not icon_widget.selected:
                for it in self.icons:
                    it.set_selected(False)
                icon_widget.set_selected(True)
            menu = QMenu(self)
            menu.addAction("Delete", self._delete_selected)
            menu.addAction("Share", lambda: self.share_app(icon_widget))
            menu.exec(self.mapToGlobal(ev.pos()))
        super().mousePressEvent(ev)

    def share_app(self, icon: IconItem):
        # placeholder
        print(f"Sharing {icon.name}...")

    def add_icon(self, name: str, pixmap: Optional[QPixmap] = None):
        if any(it.name == name for it in self.icons):
            return
        item = IconItem(name, pixmap, self)
        item.show()
        self.icons.append(item)
        self._relayout_icons()
        cell_pos = self._index_to_cell_pos(len(self.icons) - 1)
        self.icon_added.emit(name, len(self.icons) - 1, cell_pos)

    def clear_icons(self):
        for icon in self.icons:
            icon.setParent(None)
            icon.deleteLater()
        self.icons.clear()
        self.update()

    def _relayout_icons(self):
        if not self.icons:
            return
        w = max(1, self.width())
        cell_total = self.cell_size + self.spacing
        cols = max(1, w // cell_total)
        self._cols = cols
        for i, item in enumerate(self.icons):
            row, col = divmod(i, cols)
            x = col * cell_total + self.spacing // 2
            y = row * cell_total + self.spacing // 2
            item.move(x, y)
            item.setFixedSize(self.cell_size, self.cell_size)
        self.update()

    def _index_to_cell_pos(self, index: int) -> QPoint:
        cell_total = self.cell_size + self.spacing
        cols = max(1, self.width() // cell_total)
        row, col = divmod(index, cols)
        return QPoint(col * cell_total + self.spacing // 2, row * cell_total + self.spacing // 2)

    # drag/drop support
    def dragEnterEvent(self, ev):
        if ev.mimeData().hasText() or ev.mimeData().hasImage():
            ev.acceptProposedAction()

    def dragMoveEvent(self, ev):
        if ev.mimeData().hasText() or ev.mimeData().hasImage():
            ev.acceptProposedAction()

    def dropEvent(self, ev):
        md = ev.mimeData()
        if md.hasText():
            app_name = md.text().strip()
            pix = None
            if md.hasImage():
                img = md.imageData()
                if isinstance(img, QImage):
                    pix = QPixmap.fromImage(img)
                elif isinstance(img, QPixmap):
                    pix = img
            self.add_icon(app_name, pixmap=pix)
            ev.acceptProposedAction()

    # IconItem
    def _find_icon_parent(self, widget):
        while widget and not isinstance(widget, IconItem):
            widget = widget.parentWidget()
        return widget

    def _delete_selected(self):
        to_delete = [icon for icon in self.icons if icon.selected]
        for icon in to_delete:
            icon.setParent(None)
            icon.deleteLater()
            self.icons.remove(icon)
        self._relayout_icons()

# IconAdderAreaMarquee
class IconAdderAreaMarquee(IconAdderArea):
    def __init__(self, parent=None, cell_size=72, spacing=12):
        super().__init__(parent, cell_size, spacing)
        self._marquee_start: Optional[QPoint] = None
        self._marquee_rect: Optional[QRect] = None
        self._marquee_active = False
        self._marquee_selected_icons: set[IconItem] = set()

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            self._marquee_start = ev.pos()
            self._marquee_rect = QRect(self._marquee_start, self._marquee_start)
            self._marquee_active = True
            self._marquee_selected_icons.clear()
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent):
        if self._marquee_active and self._marquee_start:
            self._marquee_rect = QRect(self._marquee_start, ev.pos()).normalized()
            self._update_marquee_selection()
            self.update()
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        if self._marquee_active and ev.button() == Qt.MouseButton.LeftButton:
            self._marquee_start = None
            self._marquee_rect = None
            self._marquee_active = False
            self.update()
        super().mouseReleaseEvent(ev)

    def paintEvent(self, ev):
        super().paintEvent(ev)
        if self._marquee_rect:
            painter = QPainter(self)
            painter.setBrush(QColor(0, 120, 215, 60))  # overlay
            painter.setPen(QColor(0, 120, 215, 180))   # border
            painter.drawRect(self._marquee_rect)

    def _update_marquee_selection(self):
        if not self._marquee_rect:
            return
        ctrl = QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        for icon in self.icons:
            icon_rect = QRect(icon.pos(), icon.size())
            if self._marquee_rect.intersects(icon_rect):
                icon.set_selected(True)
                self._marquee_selected_icons.add(icon)
            elif not ctrl:
                icon.set_selected(False)

    # Override for drag & drop
    def dropEvent(self, ev):
        md = ev.mimeData()
        if md.hasText():
            app_name = md.text().strip()
            pix = None
            if md.hasImage():
                img = md.imageData()
                if isinstance(img, QImage):
                    pix = QPixmap.fromImage(img)
                elif isinstance(img, QPixmap):
                    pix = img
            self.add_icon(app_name, pixmap=pix)
            ev.acceptProposedAction()