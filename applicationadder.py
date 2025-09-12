import os
import sys
import json
import subprocess
import time
import traceback

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFileDialog, QMessageBox, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt

# try to reuse your settings util if present
try:
    from settings_utils import save_state, load_state
except Exception:
    save_state = None
    load_state = None

STATE_FILE = "user_apps.json"

def _fallback_load():
    if load_state:
        try:
            s = load_state()
            # adopt older structure if it's nested in APP_STATE
            if isinstance(s, dict) and 'user_apps' in s:
                return s['user_apps']
            return s.get('user_apps', []) if isinstance(s, dict) else s or []
        except Exception:
            pass
    # fallback read simple file
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _fallback_save(user_apps):
    if save_state:
        try:
            # If save_state expects a global APP_STATE, wrap it
            save_state({'user_apps': user_apps})
            return
        except Exception:
            pass
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(user_apps, f, indent=2, ensure_ascii=False)
    except Exception:
        traceback.print_exc()

def load_user_apps():
    return _fallback_load()

def save_user_apps(user_apps):
    _fallback_save(user_apps)

# ----- External app runner widget (can be returned in APP_MAPPING) -----
from PyQt6.QtWidgets import QVBoxLayout
class ExternalAppWidget(QWidget):
    def __init__(self, cmd, cwd=None, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.ico'))
        self.cmd = cmd
        self.cwd = cwd or os.getcwd()
        self.proc = None

        layout = QVBoxLayout(self)
        self.title = QLabel(f"External App\n{cmd}")
        self.title.setWordWrap(True)
        layout.addWidget(self.title)

        btn_row = QHBoxLayout()
        self.launch_btn = QPushButton("Launch")
        self.kill_btn = QPushButton("Stop")
        self.kill_btn.setEnabled(False)
        btn_row.addWidget(self.launch_btn)
        btn_row.addWidget(self.kill_btn)
        layout.addLayout(btn_row)

        self.launch_btn.clicked.connect(self.launch)
        self.kill_btn.clicked.connect(self.stop)

    def launch(self):
        if self.proc:
            QMessageBox.information(self, "Already running", "Process already running.")
            return
        try:
            # Use shell=True because user may paste arbitrary command; be cautious.
            self.proc = subprocess.Popen(self.cmd, shell=True, cwd=self.cwd)
            self.launch_btn.setEnabled(False)
            self.kill_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Launch failed", f"Could not start:\n{e}")
            self.proc = None

    def stop(self):
        if not self.proc:
            return
        try:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1.0)
            except Exception:
                self.proc.kill()
        except Exception:
            pass
        self.proc = None
        self.launch_btn.setEnabled(True)
        self.kill_btn.setEnabled(False)

    def closeEvent(self, ev):
        if self.proc:
            try:
                self.proc.terminate()
                time.sleep(0.05)
                if self.proc.poll() is None:
                    self.proc.kill()
            except Exception:
                pass
        super().closeEvent(ev)

# Helper to register application globally in Luxxer_OS if available
def register_app_globally(entry: dict):
    try:
        import Luxxer_OS
    except Exception:
        return False

    name = entry.get('name')
    cmd = entry.get('cmd')
    if not name or not cmd:
        return False

    # register in APP_MAPPING
    try:
        # factory that creates the widget when launch_app calls it
        Luxxer_OS.APP_MAPPING[name] = (lambda c=cmd: ExternalAppWidget(c))
    except Exception:
        pass

    # attempt to add dock button (best-effort)
    try:
        main_win = globals().get('main_win') or getattr(Luxxer_OS, 'main_win', None) or Luxxer_OS.__dict__.get('main_win', None)
        if main_win is None and hasattr(Luxxer_OS, 'MainWindow') and isinstance(Luxxer_OS, type):
            main_win = Luxxer_OS.globals().get('main_win', None)
    except Exception:
        main_win = None

    # safer: try to import main_win from Luxxer_OS module if it exposes it
    try:
        main_win = getattr(Luxxer_OS, 'main_win', main_win)
    except Exception:
        pass

    success = False
    if main_win:
        # try adding to dock: create simple QPushButton and add to layout if possible
        try:
            from PyQt6.QtWidgets import QPushButton
            btn = QPushButton(name)
            def _on_click():
                try:
                    # prefer main_win.launch_app if exists
                    if hasattr(main_win, 'launch_app'):
                        main_win.launch_app(name)
                        return
                    # fallback: instantiate ExternalAppWidget and show as window
                    w = ExternalAppWidget(cmd)
                    w.setWindowTitle(name)
                    w.show()
                except Exception:
                    traceback.print_exc()
            btn.clicked.connect(_on_click)

            # try to add to bottom dock layout (if main_win.dock has a layout and widget)
            try:
                dock = getattr(main_win, 'dock', None)
                if dock:
                    # if dock has layout addWidget, do it
                    if hasattr(dock, 'layout') and callable(getattr(dock, 'layout')):
                        l = dock.layout()
                        if l:
                            l.addWidget(btn)
                            success = True
                    else:
                        # some docks are custom widgets with .container or .layout attribute
                        if hasattr(dock, 'addWidget'):
                            dock.addWidget(btn)
                            success = True
                        else:
                            # try to find inner layout attribute
                            for attr in ('layout', 'container', 'inner'):
                                inner = getattr(dock, attr, None)
                                if inner and hasattr(inner, 'addWidget'):
                                    inner.addWidget(btn)
                                    success = True
                                    break
            except Exception:
                pass

            # if placement wants Start menu, try add to start_menu.listw
            try:
                if 'start' in (entry.get('placements') or []):
                    sm = getattr(main_win, 'start_menu', None)
                    if sm and hasattr(sm, 'listw'):
                        sm.listw.addItem(name)
                        success = True
            except Exception:
                pass
        except Exception:
            traceback.print_exc()

    return True

def unregister_app_globally(name: str):
    try:
        import Luxxer_OS
    except Exception:
        Luxxer_OS = None

    if Luxxer_OS:
        try:
            if name in Luxxer_OS.APP_MAPPING:
                Luxxer_OS.APP_MAPPING.pop(name, None)
        except Exception:
            pass
        # remove potential dock/start buttons if any (best-effort)
        try:
            main_win = getattr(Luxxer_OS, 'main_win', None)
            if main_win:
                dock = getattr(main_win, 'dock', None)
                if dock and hasattr(dock, 'layout'):
                    # remove QPushButton with text==name
                    try:
                        layout = dock.layout()
                        for i in reversed(range(layout.count())):
                            w = layout.itemAt(i).widget()
                            if w and getattr(w, 'text', lambda: '')() == name:
                                w.setParent(None)
                    except Exception:
                        pass
                # start_menu removal
                sm = getattr(main_win, 'start_menu', None)
                if sm and hasattr(sm, 'listw'):
                    for i in range(sm.listw.count()):
                        if sm.listw.item(i).text() == name:
                            sm.listw.takeItem(i)
                            break
        except Exception:
            pass

# ApplicationAdder GUI
class ApplicationAdder(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Adder")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(700, 420)

        # load existing
        self.user_apps = load_user_apps() or []
        if not isinstance(self.user_apps, list):
            self.user_apps = []

        central = QWidget()
        self.setCentralWidget(central)
        g = QGridLayout(central)

        # Left: list
        self.listw = QListWidget()
        g.addWidget(self.listw, 0, 0, 6, 1)
        self._refresh_list()

        # Right: form
        self.name_edit = QLineEdit()
        self.cmd_edit = QLineEdit()
        self.icon_edit = QLineEdit()
        self.icon_btn = QPushButton("Browse icon...")
        self.browse_btn = QPushButton("Browse command (script/exe)...")
        self.placement_dock = QCheckBox("Add to Dock")
        self.placement_start = QCheckBox("Add to Start Menu")
        self.placement_desktop = QCheckBox("Add to Desktop")

        add_btn = QPushButton("Add / Update")
        remove_btn = QPushButton("Remove selected")
        launch_btn = QPushButton("Launch selected")

        # layout
        right_v = QVBoxLayout()
        right_v.addWidget(QLabel("App name:"))
        right_v.addWidget(self.name_edit)
        right_v.addWidget(QLabel("Command to run (shell):"))
        right_v.addWidget(self.cmd_edit)
        right_v.addWidget(self.browse_btn)
        right_v.addWidget(QLabel("Icon path (optional):"))
        right_v.addWidget(self.icon_edit)
        right_v.addWidget(self.icon_btn)
        right_v.addWidget(QLabel("Placements:"))
        right_v.addWidget(self.placement_dock)
        right_v.addWidget(self.placement_start)
        right_v.addWidget(self.placement_desktop)
        right_v.addStretch()
        btn_h = QHBoxLayout()
        btn_h.addWidget(add_btn)
        btn_h.addWidget(remove_btn)
        btn_h.addWidget(launch_btn)
        right_v.addLayout(btn_h)

        g.addLayout(right_v, 0, 1, 6, 2)

        # connections
        self.listw.currentRowChanged.connect(self._on_select)
        self.browse_btn.clicked.connect(self._browse_command)
        self.icon_btn.clicked.connect(self._browse_icon)
        add_btn.clicked.connect(self._on_add)
        remove_btn.clicked.connect(self._on_remove)
        launch_btn.clicked.connect(self._on_launch)

    def _refresh_list(self):
        self.listw.clear()
        for item in self.user_apps:
            name = item.get('name') or item.get('cmd') or "<unnamed>"
            display = f"{name} — {item.get('cmd','')}"
            self.listw.addItem(display)

    def _on_select(self, idx):
        if idx < 0 or idx >= len(self.user_apps):
            self.name_edit.clear(); self.cmd_edit.clear(); self.icon_edit.clear()
            self.placement_dock.setChecked(False); self.placement_start.setChecked(False); self.placement_desktop.setChecked(False)
            return
        e = self.user_apps[idx]
        self.name_edit.setText(e.get('name',''))
        self.cmd_edit.setText(e.get('cmd',''))
        self.icon_edit.setText(e.get('icon','') or '')
        placements = e.get('placements', [])
        self.placement_dock.setChecked('dock' in placements)
        self.placement_start.setChecked('start' in placements)
        self.placement_desktop.setChecked('desktop' in placements)

    def _browse_command(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select executable / script", os.getcwd(), "All Files (*)")
        if file:
            self.cmd_edit.setText(file)

    def _browse_icon(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select icon (png, ico)", os.getcwd(), "Images (*.png *.ico *.jpg)")
        if file:
            self.icon_edit.setText(file)

    def _on_add(self):
        name = self.name_edit.text().strip()
        cmd = self.cmd_edit.text().strip()
        icon = self.icon_edit.text().strip() or None
        if not name or not cmd:
            QMessageBox.warning(self, "Invalid", "Name and Command are required.")
            return
        placements = []
        if self.placement_dock.isChecked(): placements.append('dock')
        if self.placement_start.isChecked(): placements.append('start')
        if self.placement_desktop.isChecked(): placements.append('desktop')

        # update existing with same name or append
        found = False
        for e in self.user_apps:
            if e.get('name') == name:
                e.update({'cmd': cmd, 'icon': icon, 'placements': placements})
                found = True
                break
        if not found:
            self.user_apps.append({'name': name, 'cmd': cmd, 'icon': icon, 'placements': placements})

        save_user_apps(self.user_apps)
        self._refresh_list()

        # Try to register runtime in Luxxer_OS if available
        try:
            register_app_globally(self.user_apps[-1] if not found else e)
        except Exception:
            traceback.print_exc()

        QMessageBox.information(self, "Saved", f"Application '{name}' saved and registered (if possible).")

    def _on_remove(self):
        idx = self.listw.currentRow()
        if idx < 0 or idx >= len(self.user_apps):
            return
        name = self.user_apps[idx].get('name')
        ok = QMessageBox.question(self, "Confirm", f"Remove '{name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ok != QMessageBox.StandardButton.Yes:
            return
        entry = self.user_apps.pop(idx)
        save_user_apps(self.user_apps)
        # unregister from global mapping if present
        try:
            unregister_app_globally(entry.get('name'))
        except Exception:
            pass
        self._refresh_list()
        QMessageBox.information(self, "Removed", f"Removed '{name}'.")

    def _on_launch(self):
        idx = self.listw.currentRow()
        if idx < 0 or idx >= len(self.user_apps):
            return
        entry = self.user_apps[idx]
        # try to use Luxxer main launcher if available
        try:
            import Luxxer_OS
            mw = getattr(Luxxer_OS, 'main_win', None) or globals().get('main_win')
            if mw and hasattr(mw, 'launch_app') and entry.get('name') in getattr(Luxxer_OS, 'APP_MAPPING', {}):
                mw.launch_app(entry.get('name'))
                return
        except Exception:
            pass
        # fallback: launch subprocess
        try:
            subprocess.Popen(entry.get('cmd'), shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Failed", f"Could not launch: {e}")

class ApplicationAdderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.ico'))
        layout = QVBoxLayout(self)
        self.adder = ApplicationAdder(self)
        btn_open = QPushButton("Open Application Adder")
        layout.addWidget(QLabel("Application Adder"))
        layout.addWidget(btn_open)
        btn_open.clicked.connect(self._open_window)
        self._win = None

    def _open_window(self):
        if not self._win:
            self._win = ApplicationAdder()
        self._win.show()
        self._win.raise_()