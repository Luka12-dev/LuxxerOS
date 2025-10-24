# applicationadder.py  (updated)
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

# We will operate on the existing global app_state.json (same place as your main code)
APP_STATE_FILE = "app_state.json"

def _read_full_state():
    """Return the full app_state dict from app_state.json or via load_state() if available."""
    if load_state:
        try:
            s = load_state()
            if isinstance(s, dict):
                return s
        except Exception:
            traceback.print_exc()
    # fallback direct read
    if os.path.exists(APP_STATE_FILE):
        try:
            with open(APP_STATE_FILE, "r", encoding="utf-8") as f:
                s = json.load(f)
                if isinstance(s, dict):
                    return s
        except Exception:
            traceback.print_exc()
    # default minimal structure
    return {
        "settings": {
            "theme": "transparent",
            "username": "",
            "show_start": True,
            "wallpaper": "ScreenPhoto2-2560x1440px.png"
        },
        "desktop_icons": [],
        "user_apps": [],
        "files": {"Documents": {}},
        "last_index": 0
    }

def _write_full_state(state: dict):
    """Write full state back using save_state() if present, otherwise directly."""
    if save_state:
        try:
            save_state(state)
            return
        except Exception:
            traceback.print_exc()
    try:
        folder = os.path.dirname(APP_STATE_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(APP_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        traceback.print_exc()

def load_user_apps():
    """Return list of user_apps stored inside the main app_state.json (key 'user_apps')."""
    state = _read_full_state()
    ua = state.get("user_apps", [])
    if not isinstance(ua, list):
        return []
    return ua

def save_user_apps(user_apps):
    """Save list of user_apps into the main app_state.json under 'user_apps'."""
    state = _read_full_state()
    state["user_apps"] = user_apps or []
    _write_full_state(state)

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
    """
    Best-effort: register app in Luxxer_OS.APP_MAPPING and add UI elements to dock/start/desktop.
    Returns True if registration attempted.
    """
    try:
        import Luxxer_OS
    except Exception:
        Luxxer_OS = None

    name = entry.get('name')
    cmd = entry.get('cmd')
    icon = entry.get('icon')
    placements = entry.get('placements', []) or []

    if not name or not cmd:
        return False

    # Register factory in APP_MAPPING so MainWindow.launch_app can instantiate it
    try:
        if Luxxer_OS is not None:
            Luxxer_OS.APP_MAPPING[name] = (lambda c=cmd: ExternalAppWidget(c))
        else:
            # Try to update a module-level APP_MAPPING if present in globals (best-effort)
            gmap = globals().get('APP_MAPPING')
            if isinstance(gmap, dict):
                gmap[name] = (lambda c=cmd: ExternalAppWidget(c))
    except Exception:
        traceback.print_exc()

    # Try to update the persistent app_state: ensure it's in user_apps
    try:
        state = _read_full_state()
        user_apps = state.get('user_apps', [])
        # replace or append
        replaced = False
        for i, e in enumerate(user_apps):
            if e.get('name') == name:
                user_apps[i] = entry
                replaced = True
                break
        if not replaced:
            user_apps.append(entry)
        state['user_apps'] = user_apps
        _write_full_state(state)
    except Exception:
        traceback.print_exc()

    # Try to add to UI if possible (main_win)
    try:
        main_win = None
        if Luxxer_OS:
            main_win = getattr(Luxxer_OS, 'main_win', None)
        # fallback: try globals
        if main_win is None:
            main_win = globals().get('main_win')

        if main_win:
            # Add to APP_MAPPING on main_win module if available
            try:
                if hasattr(main_win, 'APP_MAPPING') and isinstance(main_win.APP_MAPPING, dict):
                    main_win.APP_MAPPING[name] = (lambda c=cmd: ExternalAppWidget(c))
            except Exception:
                pass

            # Add to Dock (best-effort)
            try:
                # if main_win has a method to add dock apps, prefer it
                if hasattr(main_win, 'add_to_dock') and callable(getattr(main_win, 'add_to_dock')):
                    main_win.add_to_dock(name, icon)
                else:
                    dock = getattr(main_win, 'dock', None)
                    if dock:
                        # try common approaches
                        if hasattr(dock, 'add_app'):
                            try:
                                dock.add_app(name, icon)
                            except Exception:
                                pass
                        else:
                            # try to insert a button into dock.layout()
                            layout = None
                            try:
                                layout = dock.layout()
                            except Exception:
                                # maybe custom attribute that stores container
                                for attr in ('container', 'inner', 'inner_layout'):
                                    candidate = getattr(dock, attr, None)
                                    if candidate and hasattr(candidate, 'layout'):
                                        layout = candidate.layout()
                                        break
                            if layout and hasattr(layout, 'addWidget'):
                                try:
                                    btn = QPushButton(name)
                                    def onclick(n=name):
                                        try:
                                            if hasattr(main_win, 'launch_app'):
                                                main_win.launch_app(n)
                                            else:
                                                # fallback show ExternalAppWidget
                                                w = ExternalAppWidget(cmd)
                                                w.setWindowTitle(n)
                                                w.show()
                                        except Exception:
                                            traceback.print_exc()
                                    btn.clicked.connect(onclick)
                                    layout.addWidget(btn)
                                except Exception:
                                    traceback.print_exc()
            except Exception:
                traceback.print_exc()

            # Add to Start menu list if requested
            if 'start' in placements:
                try:
                    sm = getattr(main_win, 'start_menu', None)
                    if sm and hasattr(sm, 'listw'):
                        # Avoid duplicates
                        found = False
                        for i in range(sm.listw.count()):
                            if sm.listw.item(i).text() == name:
                                found = True
                                break
                        if not found:
                            sm.listw.addItem(name)
                except Exception:
                    traceback.print_exc()

            # Add to Desktop icons if requested
            if 'desktop' in placements:
                try:
                    app_state = _read_full_state()
                    desktop_icons = app_state.get('desktop_icons', [])
                    if name not in desktop_icons:
                        desktop_icons.append(name)
                        app_state['desktop_icons'] = desktop_icons
                        _write_full_state(app_state)
                    # update UI immediately
                    try:
                        if hasattr(main_win, '_load_desktop_icons'):
                            main_win._load_desktop_icons()
                        elif hasattr(main_win, 'icon_area') and hasattr(main_win.icon_area, 'add_icon'):
                            main_win.icon_area.add_icon(name)
                    except Exception:
                        traceback.print_exc()
                except Exception:
                    traceback.print_exc()

    except Exception:
        traceback.print_exc()

    return True

def unregister_app_globally(name: str):
    try:
        import Luxxer_OS
    except Exception:
        Luxxer_OS = None

    try:
        if Luxxer_OS and hasattr(Luxxer_OS, 'APP_MAPPING') and name in Luxxer_OS.APP_MAPPING:
            Luxxer_OS.APP_MAPPING.pop(name, None)
    except Exception:
        traceback.print_exc()

    # remove from persistent state
    try:
        state = _read_full_state()
        user_apps = state.get('user_apps', [])
        new = [e for e in user_apps if e.get('name') != name]
        if len(new) != len(user_apps):
            state['user_apps'] = new
            _write_full_state(state)
    except Exception:
        traceback.print_exc()

    # remove from dock/start/desktop UI (best-effort)
    try:
        main_win = None
        if Luxxer_OS:
            main_win = getattr(Luxxer_OS, 'main_win', None)
        if main_win is None:
            main_win = globals().get('main_win')

        if main_win:
            try:
                if hasattr(main_win, 'APP_MAPPING') and name in main_win.APP_MAPPING:
                    main_win.APP_MAPPING.pop(name, None)
            except Exception:
                pass

            try:
                dock = getattr(main_win, 'dock', None)
                if dock:
                    try:
                        layout = dock.layout()
                        for i in reversed(range(layout.count())):
                            w = layout.itemAt(i).widget()
                            if w and getattr(w, 'text', lambda: '')() == name:
                                w.setParent(None)
                    except Exception:
                        pass
            except Exception:
                pass

            try:
                sm = getattr(main_win, 'start_menu', None)
                if sm and hasattr(sm, 'listw'):
                    for i in range(sm.listw.count()):
                        if sm.listw.item(i).text() == name:
                            sm.listw.takeItem(i)
                            break
            except Exception:
                pass

            try:
                # remove from desktop icons persisted state
                state = _read_full_state()
                di = state.get('desktop_icons', [])
                if name in di:
                    di.remove(name)
                    state['desktop_icons'] = di
                    _write_full_state(state)
                    # refresh UI
                    if hasattr(main_win, '_load_desktop_icons'):
                        main_win._load_desktop_icons()
            except Exception:
                pass

    except Exception:
        traceback.print_exc()

# ApplicationAdder GUI
class ApplicationAdder(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Adder")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(700, 420)

        # load existing from the unified app_state.json
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

        # build entry
        entry = {'name': name, 'cmd': cmd, 'icon': icon, 'placements': placements}

        # update existing with same name or append
        found = False
        for e in self.user_apps:
            if e.get('name') == name:
                e.update(entry)
                found = True
                break
        if not found:
            self.user_apps.append(entry)

        # persist into main app_state.json
        try:
            save_user_apps(self.user_apps)
        except Exception:
            traceback.print_exc()

        # Register globally in runtime (so main window can launch it)
        try:
            register_app_globally(entry)
        except Exception:
            traceback.print_exc()

        # If dock/desktop placement requested and main window exists, try immediate UI update
        try:
            import Luxxer_OS
            main_win = getattr(Luxxer_OS, 'main_win', None)
        except Exception:
            main_win = globals().get('main_win')

        if main_win:
            try:
                # Add to dock if requested and main_win supports it
                if 'dock' in placements:
                    try:
                        if hasattr(main_win, 'add_to_dock'):
                            main_win.add_to_dock(name, icon)
                        elif hasattr(main_win, 'dock') and hasattr(main_win.dock, 'add_app'):
                            main_win.dock.add_app(name, icon)
                        else:
                            # fallback: try adding a QPushButton to dock layout
                            try:
                                layout = main_win.dock.layout()
                                btn = QPushButton(name)
                                btn.clicked.connect(lambda n=name: main_win.launch_app(n) if hasattr(main_win, 'launch_app') else None)
                                layout.addWidget(btn)
                            except Exception:
                                pass
                    except Exception:
                        traceback.print_exc()

                # Add to desktop if requested
                if 'desktop' in placements:
                    try:
                        # update main_win state and UI
                        app_state = _read_full_state()
                        di = app_state.get('desktop_icons', [])
                        if name not in di:
                            di.append(name)
                            app_state['desktop_icons'] = di
                            _write_full_state(app_state)
                        try:
                            if hasattr(main_win, '_load_desktop_icons'):
                                main_win._load_desktop_icons()
                            elif hasattr(main_win, 'icon_area') and hasattr(main_win.icon_area, 'add_icon'):
                                main_win.icon_area.add_icon(name)
                        except Exception:
                            traceback.print_exc()
                    except Exception:
                        traceback.print_exc()

                # Add to Start menu UI if requested
                if 'start' in placements:
                    try:
                        sm = getattr(main_win, 'start_menu', None)
                        if sm and hasattr(sm, 'listw'):
                            # avoid duplicates
                            found = False
                            for i in range(sm.listw.count()):
                                if sm.listw.item(i).text() == name:
                                    found = True
                                    break
                            if not found:
                                sm.listw.addItem(name)
                    except Exception:
                        traceback.print_exc()
            except Exception:
                traceback.print_exc()

        self._refresh_list()
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
        # persist removal
        try:
            save_user_apps(self.user_apps)
        except Exception:
            traceback.print_exc()
        # unregister from global mapping if present
        try:
            unregister_app_globally(entry.get('name'))
        except Exception:
            traceback.print_exc()
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