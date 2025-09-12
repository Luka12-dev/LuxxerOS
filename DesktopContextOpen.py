from PyQt6.QtCore import Qt, QPoint, QObject
from PyQt6.QtWidgets import (
     QWidget, QMenu, QFileDialog, QMessageBox, QApplication
)
from PyQt6.QtGui import QCursor, QAction
import traceback

class DesktopContextMenu(QObject):
    def __init__(self, main_ref):
        super().__init__(main_ref)
        self.main_ref = main_ref
        self._installed = False
        self._overlay = None
        self._patched = False

    def install(self):
        if self._installed:
            return

        target = getattr(self.main_ref, "mdi", None)
        if target is None:
            target = getattr(self.main_ref, "centralWidget", None)
        if target is None:
            return

        try:
            widget = target.viewport() if hasattr(target, "viewport") else target

            widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            widget.customContextMenuRequested.connect(self._on_context)

            if not hasattr(widget, "_desktop_context_patched"):
                self._patch_mouse_press(widget)

            self._installed = True
            print("[DesktopContextMenu] Installed on:", widget)
        except Exception as e:
            print("[DesktopContextMenu] install error:", e)
            traceback.print_exc()

    def _patch_mouse_press(self, widget):
        try:
            old_mouse = widget.mousePressEvent

            def patched_mouse(e):
                try:
                    gp = e.globalPosition().toPoint() if hasattr(e, "globalPosition") else e.globalPos()
                    if e.button() == Qt.MouseButton.RightButton:
                        self._show_menu(QPoint(gp.x(), gp.y()))
                        return
                except Exception:
                    pass
                try:
                    old_mouse(e)
                except Exception:
                    pass

            widget.mousePressEvent = patched_mouse
            widget._desktop_context_patched = True
            self._patched = True
            print("[DesktopContextMenu] Patched mousePressEvent on viewport")
        except Exception as e:
            print("[DesktopContextMenu] patch error:", e)
            traceback.print_exc()

    def _on_context(self, pos):
        try:
            widget = self.main_ref.mdi.viewport() if hasattr(self.main_ref, "mdi") else self.main_ref.centralWidget()
            global_pos = widget.mapToGlobal(pos)
            self._show_menu(global_pos)
        except Exception as e:
            print("[DesktopContextMenu] _on_context error:", e)
            traceback.print_exc()

    def _show_menu(self, global_pos: QPoint):
        try:
            # overlay dim
            overlay = QWidget(self.main_ref)
            overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            overlay.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
            overlay.setStyleSheet("background: rgba(0,0,0,0.22);")
            overlay.setGeometry(self.main_ref.rect())
            overlay.show()
            self._overlay = overlay
        except Exception:
            self._overlay = None

        try:
            menu = QMenu(self.main_ref)
            a_refresh = QAction("Refresh", menu)
            a_settings = QAction("Settings", menu)
            a_change_wallpaper = QAction("Change wallpaper...", menu)
            a_exit = QAction("Exit Luxxer", menu)

            menu.addAction(a_refresh)
            menu.addAction(a_settings)
            menu.addAction(a_change_wallpaper)
            menu.addSeparator()
            menu.addAction(a_exit)

            a_refresh.triggered.connect(self._do_refresh)
            a_settings.triggered.connect(self._open_settings)
            a_change_wallpaper.triggered.connect(self._choose_wallpaper)
            a_exit.triggered.connect(lambda: QApplication.instance().quit())

            menu.exec(global_pos)
        except Exception as e:
            print("[DesktopContextMenu] menu exec error:", e)
            traceback.print_exc()
        finally:
            # cleanup overlay
            try:
                if self._overlay:
                    self._overlay.hide()
                    self._overlay.deleteLater()
                    self._overlay = None
            except Exception:
                pass

    def _do_refresh(self):
        try:
            if hasattr(self.main_ref, "_apply_mdi_background"):
                self.main_ref._apply_mdi_background()
            else:
                self.main_ref.repaint()
        except Exception as e:
            print("[DesktopContextMenu] refresh error:", e)
            traceback.print_exc()

    def _open_settings(self):
        try:
            from Luxxer_OS import SettingsApp
        except Exception:
            try:
                from .Luxxer_OS import SettingsApp
            except Exception:
                SettingsApp = None

        if SettingsApp:
            try:
                try:
                    settings = SettingsApp(self.main_ref)
                except TypeError:
                    settings = SettingsApp()
                settings.show()
            except Exception as e:
                QMessageBox.warning(self.main_ref, "Settings", f"Failed to open Settings: {e}")
        else:
            QMessageBox.information(self.main_ref, "Settings", "Settings app not available.")

    def _choose_wallpaper(self):
        try:
            path, _ = QFileDialog.getOpenFileName(
                self.main_ref,
                "Choose wallpaper",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
            )
            if path:
                if hasattr(self.main_ref, "set_wallpaper"):
                    self.main_ref.set_wallpaper(path)
                else:
                    QMessageBox.information(self.main_ref, "Wallpaper", "Main window does not support set_wallpaper().")
        except Exception as e:
            QMessageBox.warning(self.main_ref, "Wallpaper", f"Failed to set wallpaper: {e}")
            traceback.print_exc()