
import json
import os
from typing import Optional, List
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication,
    QMenu, QMessageBox, QFileDialog, QMainWindow, QListWidget, QPushButton
)
from PyQt6.QtGui import (
    QPixmap, QColor, QMouseEvent, QDragEnterEvent, QDropEvent,
    QDrag, QFont, QIcon, QImage, QPainter, QBrush, QPen, QCursor, QEnterEvent
)
from PyQt6.QtCore import (
    Qt, QRect, QPoint, pyqtSignal, QSize, QTimer, QMimeData
)

# ---------------- Theme ----------------
@dataclass
class ThemeConfig:
    name: str
    bg_primary: str
    bg_secondary: str
    text_primary: str
    text_secondary: str
    accent: str
    accent_hover: str
    selection_bg: str
    selection_border: str
    border_color: str
    shadow_color: str

DARK_THEME = ThemeConfig(
    name="dark",
    bg_primary="#1a1a1a",
    bg_secondary="#2d2d2d",
    text_primary="#ffffff",
    text_secondary="#b0b0b0",
    accent="#00a8ff",
    accent_hover="#00d4ff",
    selection_bg="rgba(0, 0, 0, 0.35)",         # darker selection for contrast
    selection_border="rgba(0, 168, 255, 0.45)",
    border_color="#404040",
    shadow_color="rgba(0, 0, 0, 0.5)"
)



# ---------------- IconItem ----------------
class IconItem(QWidget):
    """
    Individual icon with safer signals and small dark dock-like background.
    Signals:
      - activated(str) : emits name on double-click
      - context_menu_requested(object, QPoint) : emits (IconItem_instance, globalPos)
          (backwards compatible: handler can accept string name too)
    """
    activated = pyqtSignal(str)
    # send object (IconItem) and QPoint - safer than str only
    context_menu_requested = pyqtSignal(object, QPoint)

    def __init__(self, name: str, pixmap: Optional[QPixmap] = None,
                 parent: Optional[QWidget] = None, theme: Optional[ThemeConfig] = None):
        super().__init__(parent)
        self.name = name
        self.selected = False
        self.hovered = False
        self.theme = theme or DARK_THEME

        cell_size = getattr(parent, "cell_size", 96)
        self.icon_size = min(64, cell_size - 28)
        self.cell_size = cell_size

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # small dark "dock" background around icon (via stylesheet)
        # we'll style the whole widget but make it subtle
        self.icon_frame = QLabel()
        self.icon_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_icon(pixmap)
        self.icon_frame.setFixedHeight(self.icon_size + 6)
        layout.addWidget(self.icon_frame, 0, Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel(self.name)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setFont(QFont("Segoe UI", 9))
        self.text_label.setFixedHeight(36)
        layout.addWidget(self.text_label)

        self.setLayout(layout)
        # overall size includes text and frame
        self.setFixedSize(QSize(cell_size, cell_size))
        self.setMouseTracking(True)
        self._update_style()

        self._drag_start_pos: Optional[QPoint] = None

    def _set_icon(self, pixmap: Optional[QPixmap]) -> None:
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(self.icon_size, self.icon_size,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.icon_frame.setPixmap(scaled)
        else:
            # fallback pixmap
            ic = QIcon.fromTheme("application-x-executable")
            pm = ic.pixmap(self.icon_size, self.icon_size)
            if pm.isNull():
                pm = QPixmap(self.icon_size, self.icon_size)
                pm.fill(QColor(self.theme.accent))
            self.icon_frame.setPixmap(pm)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.hovered = True
        self._update_style()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.hovered = False
        self._update_style()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, ev: QMouseEvent) -> None:
        try:
            self.activated.emit(self.name)
        except Exception:
            pass
        super().mouseDoubleClickEvent(ev)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = ev.pos()
        elif ev.button() == Qt.MouseButton.RightButton:
            # emit object + globalPos (safe)
            try:
                self.context_menu_requested.emit(self, ev.globalPos())
            except Exception:
                # fallback: emit name (backcompat)
                try:
                    self.context_menu_requested.emit(self.name, ev.globalPos())
                except Exception:
                    pass
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if ev.buttons() & Qt.MouseButton.LeftButton and self._drag_start_pos:
            if (ev.pos() - self._drag_start_pos).manhattanLength() > QApplication.startDragDistance():
                self._start_drag()
        super().mouseMoveEvent(ev)

    def _start_drag(self) -> None:
        mime = QMimeData()
        mime.setText(self.name)
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(self.grab())  # visual feedback
        drag.setHotSpot(QPoint(self.width() // 2, self.height() // 2))
        drag.exec(Qt.DropAction.CopyAction)

    def set_selected(self, value: bool) -> None:
        if self.selected != value:
            self.selected = value
            self._update_style()

    def set_theme(self, theme: ThemeConfig) -> None:
        self.theme = theme
        self._update_style()

    def _update_style(self) -> None:
        base_bg = "rgba(0,0,0,0.65)"
        hover_bg = "rgba(255,255,255,0.08)"
        press_bg = "rgba(255,255,255,0.04)"
        border_radius = int(self.icon_size * 0.25)

        if self.selected:
            bg = self.theme.selection_bg
            border = "2px solid #0078D7"  # plava Windows selekcija
        elif self.hovered:
            bg = hover_bg
            border = "1px solid #000000"  # čvrsto crno
        else:
            bg = base_bg
            border = "1px solid #000000"  # čvrsto crno i kad nije hover

        self.setStyleSheet(f"""
            IconItem {{
                background-color: {bg};
                border-radius: {border_radius}px;
                border: {border};
            }}
            IconItem:hover {{
                background-color: {hover_bg};
            }}
            IconItem:pressed {{
                background-color: {press_bg};
            }}
        """)

        self.text_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme.text_primary};
                font-size: 9pt;
                font-weight: 500;
            }}
        """)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))

    def sizeHint(self) -> QSize:
        return self.size()

# ---------------- IconAdderArea ----------------
class IconAdderArea(QWidget):
    icon_added = pyqtSignal(str, int, QPoint)
    icon_removed = pyqtSignal(str)
    icon_activated = pyqtSignal(str)
    selection_changed = pyqtSignal(list)

    def __init__(self, parent: Optional[QWidget] = None, cell_size: int = 96, spacing: int = 12,
                 theme: Optional[ThemeConfig] = None):
        super().__init__(parent)
        self.icons: List[IconItem] = []
        self.cell_size = max(64, cell_size)
        self.spacing = max(6, spacing)
        self.theme = theme or DARK_THEME
        self._cols = 1

        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._update_background()

        self._relayout_timer = QTimer()
        self._relayout_timer.setSingleShot(True)
        self._relayout_timer.timeout.connect(self._relayout_icons)
        self.resizeEvent = self._handle_resize

    def _handle_resize(self, ev) -> None:
        self._relayout_timer.stop()
        self._relayout_timer.start(100)
        super().resizeEvent(ev)

    def _update_background(self) -> None:
        self.setStyleSheet(f"""
            IconAdderArea {{
                background-color: {self.theme.bg_primary};
                border: 0px;
            }}
        """)

    def set_theme(self, theme: ThemeConfig) -> None:
        self.theme = theme
        self._update_background()
        for icon in self.icons:
            icon.set_theme(theme)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            child = self.childAt(ev.pos())
            icon_widget = self._find_icon_parent(child)
            if not icon_widget:
                self._clear_selection()
        super().mousePressEvent(ev)

    # Note: we don't normally override contextMenuEvent here because we
    # rely on IconItem to emit context_menu_requested. Keep for safety:
    def contextMenuEvent(self, ev) -> None:
        child = self.childAt(ev.pos())
        icon_widget = self._find_icon_parent(child)
        if icon_widget:
            self._show_icon_menu(icon_widget, ev.globalPos())

    def _show_icon_menu(self, icon, pos: QPoint) -> None:
        # normalize icon -> IconItem instance or None
        icon_widget = None
        if isinstance(icon, str):
            icon_widget = next((it for it in self.icons if it.name == icon), None)
        else:
            # could be IconItem or may be name as fallback
            icon_widget = icon if isinstance(icon, IconItem) else next((it for it in self.icons if it.name == str(icon)), None)

        if icon_widget is None:
            return

        if not icon_widget.selected:
            self._clear_selection()
            icon_widget.set_selected(True)

        menu = QMenu(self)
        menu.setStyleSheet(self._get_menu_stylesheet())

        menu.addAction("Open", lambda: self.icon_activated.emit(icon_widget.name))
        menu.addSeparator()
        menu.addAction("Delete", lambda: self._delete_icon(icon_widget))
        menu.addAction("Delete", lambda _, i=icon_widget: self._delete_icon(i))

        if len([i for i in self.icons if i.selected]) > 1:
            menu.addSeparator()
            menu.addAction("Delete Selected", self._delete_selected)

        if not isinstance(pos, QPoint):
            pos = QCursor.pos()
        menu.exec(pos)

    def _get_menu_stylesheet(self) -> str:
        return f"""
            QMenu {{
                background-color: {self.theme.bg_secondary};
                color: {self.theme.text_primary};
                border: 1px solid {self.theme.border_color};
                border-radius: 6px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme.accent};
                color: white;
            }}
        """

    def _share_icon(self, icon: IconItem) -> None:
        QMessageBox.information(self, "Share", f"Sharing: {icon.name}")

    def add_icon(self, name: str, pixmap: Optional[QPixmap] = None, animate: bool = True) -> bool:
        if any(it.name == name for it in self.icons):
            return False

        item = IconItem(name, pixmap, self, self.theme)
        # Forward activation signal in a safe way
        item.activated.connect(lambda name, i=item: self.icon_activated.emit(name))
        # context_menu_requested will send (IconItem, QPoint)
        item.context_menu_requested.connect(self._show_icon_menu)

        item.show()
        self.icons.append(item)
        self._relayout_icons()

        cell_pos = self._index_to_cell_pos(len(self.icons) - 1)
        self.icon_added.emit(name, len(self.icons) - 1, cell_pos)
        return True

    def remove_icon(self, name: str) -> bool:
        icon = next((i for i in self.icons if i.name == name), None)
        if icon:
            self._delete_icon(icon)
            return True
        return False

    def _delete_icon(self, icon: IconItem) -> None:
        try:
            icon.setParent(None)
            icon.deleteLater()
            self.icons.remove(icon)
            self.icon_removed.emit(icon.name)
            self._relayout_icons()
        except Exception:
            pass

    def _delete_selected(self) -> None:
        to_delete = [icon for icon in self.icons if icon.selected]
        for icon in to_delete:
            self._delete_icon(icon)

    def clear_icons(self) -> None:
        for icon in list(self.icons):
            self._delete_icon(icon)

    def _clear_selection(self) -> None:
        for icon in self.icons:
            icon.set_selected(False)
        self.selection_changed.emit([])

    def get_selected(self) -> List[str]:
        return [icon.name for icon in self.icons if icon.selected]

    def _relayout_icons(self) -> None:
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

    def dragEnterEvent(self, ev: QDragEnterEvent) -> None:
        if ev.mimeData().hasText() or ev.mimeData().hasImage():
            ev.acceptProposedAction()

    def dragMoveEvent(self, ev) -> None:
        if ev.mimeData().hasText() or ev.mimeData().hasImage():
            ev.acceptProposedAction()

    def dropEvent(self, ev: QDropEvent) -> None:
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

    def _find_icon_parent(self, widget: Optional[QWidget]) -> Optional[IconItem]:
        while widget and not isinstance(widget, IconItem):
            widget = widget.parentWidget()
        return widget

# ---------------- IconAdderAreaMarquee ----------------
class IconAdderAreaMarquee(IconAdderArea):
    def __init__(self, parent: Optional[QWidget] = None, cell_size: int = 96, spacing: int = 12,
                 theme: Optional[ThemeConfig] = None):
        super().__init__(parent, cell_size, spacing, theme)
        self._marquee_start: Optional[QPoint] = None
        self._marquee_rect: Optional[QRect] = None
        self._marquee_active = False

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = ev.pos()
        elif ev.button() == Qt.MouseButton.RightButton:
            try:
                self.context_menu_requested.emit(self, ev.globalPos())
            except Exception:
                pass
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self._marquee_active and self._marquee_start:
            self._marquee_rect = QRect(self._marquee_start, ev.pos()).normalized()
            self._update_marquee_selection()
            self.update()
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self._marquee_active and ev.button() == Qt.MouseButton.LeftButton:
            self._marquee_start = None
            self._marquee_rect = None
            self._marquee_active = False
            self.update()
        super().mouseReleaseEvent(ev)

    def paintEvent(self, ev) -> None:
        super().paintEvent(ev)
        if self._marquee_rect:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            brush_color = QColor("#0078D7")  # Windows plava
            brush_color.setAlpha(60)
            painter.setBrush(QBrush(brush_color))
            pen_color = QColor("#0078D7")
            pen_color.setAlpha(180)
            painter.setPen(QPen(pen_color, 2))
            painter.drawRect(self._marquee_rect)
            painter.end()

    def _update_marquee_selection(self) -> None:
        if not self._marquee_rect:
            return
        ctrl_pressed = QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        for icon in self.icons:
            icon_rect = QRect(icon.pos(), icon.size())
            intersects = self._marquee_rect.intersects(icon_rect)
            if intersects:
                icon.set_selected(True)
            elif not ctrl_pressed:
                icon.set_selected(False)
        self.selection_changed.emit(self.get_selected())