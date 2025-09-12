from __future__ import annotations

import sys
import os
import subprocess
import threading
import traceback
import datetime
from typing import Optional, Callable

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QFileDialog, QMessageBox, QTextEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont, QClipboard, QPaintEvent, QPainterPath, QPen

# BSOD GUI

class _FaceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, ev: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w = self.width()
        h = self.height()
        cx = w // 2
        cy = h // 2
        r = min(w, h) // 3

        # shadow
        shadow_color = QColor(0, 0, 0, 40)
        painter.setBrush(shadow_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - r + 6, cy - r + 10, 2 * r, 2 * r)

        # White face circle
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)

        # Eyes
        eye_w = max(8, r // 6)
        eye_h = max(8, r // 5)
        eye_dx = r // 2
        painter.setBrush(QColor("#111111"))
        painter.drawEllipse(cx - eye_dx - eye_w//2, cy - r//6 - eye_h//2, eye_w, eye_h)
        painter.drawEllipse(cx + eye_dx - eye_w//2, cy - r//6 - eye_h//2, eye_w, eye_h)

        # sad mouth
        path = QPainterPath()
        mouth_w = int(r * 1.1)
        path.moveTo(cx - mouth_w//2, cy + r//8)
        path.cubicTo(cx - mouth_w//4, cy + r//1.8, cx + mouth_w//4, cy + r//1.8, cx + mouth_w//2, cy + r//8)
        pen = QPen(QColor("#111111"))
        pen.setWidth(max(6, r // 10))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        painter.end()

class BSODWindow(QMainWindow):
    def __init__(self, title: str = "A problem has been detected", details: str = "", code: Optional[int] = None,
                 restart_callback: Optional[Callable] = None):
        super().__init__(None, Qt.WindowType.Window)
        self.setWindowTitle("Blue Screen")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowState(self.windowState() | Qt.WindowState.WindowFullScreen)

        self.restart_callback = restart_callback

        # style: classic blue but nicer
        blue = "#0078D7"
        panel_blue = "#0063b1"
        btn_bg = "#ffffff"
        btn_fg = "#00304d"
        txt_color = "#ffffff"

        style = f"""
            QMainWindow {{ background: {blue}; }}
            QWidget {{ color: {txt_color}; }}
            QLabel#big {{ color: {txt_color}; font-size: 26px; font-weight: 700; }}
            QLabel#small {{ color: {txt_color}; font-size: 12px; }}
            QTextEdit {{ background: rgba(0,0,0,0.12); color: #fff; border: 1px solid rgba(255,255,255,0.08); border-radius:6px; }}
            QPushButton {{ background: transparent; color: {txt_color}; border: 1px solid rgba(255,255,255,0.12); padding:8px 12px; border-radius:8px; min-width:100px; }}
            QPushButton#primary {{ background: {btn_bg}; color: {btn_fg}; border: none; font-weight:700; }}
            QPushButton#primary:hover {{ background: #f2f2f2; }}
            QPushButton#danger {{ background: rgba(255,255,255,0.06); color: #fff; border: 1px solid rgba(255,255,255,0.08); }}
        """
        self.setStyleSheet(style)

        central = QWidget(self)
        lay = QVBoxLayout(central)
        lay.setContentsMargins(80, 36, 80, 28)
        lay.setSpacing(14)
        lay.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        face = _FaceWidget(self)
        lay.addWidget(face, alignment=Qt.AlignmentFlag.AlignHCenter)

        lbl_big = QLabel(":(\nA problem has been detected and Luxxer OS has been shut down to prevent damage.")
        lbl_big.setObjectName("big")
        lbl_big.setWordWrap(True)
        lbl_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_big.setFont(QFont("Segoe UI", 22, QFont.Weight.DemiBold))
        lay.addWidget(lbl_big)

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        code_text = f"ERROR CODE: {code}" if code is not None else ""
        lbl_small = QLabel(f"{code_text}\n{ts}\n\nIf this is the first time you've seen this screen, try restarting the application.")
        lbl_small.setObjectName("small")
        lbl_small.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_small.setFont(QFont("Segoe UI", 11))
        lay.addWidget(lbl_small)

        self.details = details or "(no details)"
        self._details_box = QTextEdit()
        self._details_box.setReadOnly(True)
        self._details_box.setPlainText(self.details)
        self._details_box.setVisible(False)
        self._details_box.setMinimumHeight(180)
        lay.addWidget(self._details_box)

        bottom = QHBoxLayout()
        bottom.setSpacing(10)

        left_group = QHBoxLayout()
        self.btn_details = QPushButton("Show details")
        self.btn_details.clicked.connect(self._toggle_details)
        left_group.addWidget(self.btn_details)

        btn_copy = QPushButton("Copy error")
        btn_copy.clicked.connect(self._copy_error)
        left_group.addWidget(btn_copy)

        btn_save = QPushButton("Save log")
        btn_save.clicked.connect(self._save_log)
        left_group.addWidget(btn_save)

        bottom.addLayout(left_group)
        bottom.addStretch()

        right_group = QHBoxLayout()
        btn_restart = QPushButton("Attempt Restart")
        btn_restart.setObjectName("primary")
        btn_restart.clicked.connect(self._attempt_restart)
        right_group.addWidget(btn_restart)

        btn_quit = QPushButton("Quit")
        btn_quit.setObjectName("danger")
        btn_quit.clicked.connect(self._quit)
        right_group.addWidget(btn_quit)

        bottom.addLayout(right_group)

        lay.addLayout(bottom)
        self.setCentralWidget(central)

        # ensure it fills screen and is on top
        QTimer.singleShot(10, self._raise_fullscreen)

        # keyboard shortcuts
        central.setFocus()
        central.grabKeyboard()

    def _raise_fullscreen(self):
        self.showFullScreen()
        self.raise_()
        self.activateWindow()

    def _toggle_details(self):
        v = not self._details_box.isVisible()
        self._details_box.setVisible(v)
        self.btn_details.setText("Hide details" if v else "Show details")

    def _copy_error(self):
        cb: QClipboard = QApplication.clipboard()
        cb.setText(self.details)
        QMessageBox.information(self, "Copied", "Error text copied to clipboard")

    def _save_log(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save error log", "luxxer-bsod-log.txt", "Text files (*.txt);;All Files (*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.details)
                QMessageBox.information(self, "Saved", f"Saved log to {path}")
            except Exception as e:
                QMessageBox.warning(self, "Save failed", str(e))

    def _attempt_restart(self):
        # call restart_callback if provided (monitor will pass a setter)
        if callable(self.restart_callback):
            try:
                # close the BSOD window and call restart callback so monitor can restart child
                self.close()
                self.restart_callback()
            except Exception as e:
                QMessageBox.warning(self, "Restart failed", str(e))
        else:
            QMessageBox.information(self, "Restart", "No restart callback provided.")

    def _quit(self):
        QApplication.quit()

# Helpers & non-GUI hooks

def _format_exception(ex_type, ex_value, tb) -> str:
    text = "".join(traceback.format_exception(ex_type, ex_value, tb))
    header = f"Exception: {ex_type.__name__}: {ex_value}\n"
    ts = datetime.datetime.now().isoformat()
    return f"Timestamp: {ts}\n{header}\nTraceback:\n{text}"

def _show_bsod(details: str, code: Optional[int] = None, restart_callback: Optional[Callable] = None):
    """
    Show BSOD window; if no QApplication exists, create one (blocks).
    If QApplication exists, show BSOD window on top (non-blocking).
    """
    app = QApplication.instance()
    created_app = False
    if app is None:
        app = QApplication(sys.argv)
        created_app = True

    win = BSODWindow(title="Critical Error", details=details, code=code, restart_callback=restart_callback)
    win.showFullScreen()
    win.raise_()
    win.activateWindow()

    # If we created the app specifically to show BSOD, exec() (block) so user interacts.
    # If an outer application exists, assume it will keep running event loop; we still show window.
    if created_app:
        try:
            app.exec()
        except Exception:
            pass

# Excepthook for convenience (legacy)
def bsod_excepthook(ex_type, ex_value, tb):
    try:
        details = _format_exception(ex_type, ex_value, tb)
    except Exception:
        details = "Failed to format exception"
    _show_bsod(details=details, code=None)

def bsod_threading_excepthook(args):
    try:
        details = _format_exception(args.exc_type, args.exc_value, args.exc_traceback)
    except Exception:
        details = "Failed to format thread exception"
    _show_bsod(details=details, code=None)

def install_global_handlers(restart_callback: Optional[Callable] = None):
    """
    Install global hooks (sys.excepthook and threading.excepthook) to show BSOD
    for uncaught exceptions. restart_callback may be passed and will be called
    when user clicks Attempt Restart in the BSOD window.
    """
    def hook(ex_type, ex_value, tb):
        details = _format_exception(ex_type, ex_value, tb)
        _show_bsod(details=details, code=None, restart_callback=restart_callback)
    sys.excepthook = hook

    try:
        import threading as _thr
        if hasattr(_thr, "excepthook"):
            def th_hook(args):
                details = _format_exception(args.exc_type, args.exc_value, args.exc_traceback)
                _show_bsod(details=details, code=None, restart_callback=restart_callback)
            _thr.excepthook = th_hook
    except Exception:
        pass

# Supervised runner

def run_with_bsod(main_callable: Callable, *args, restart_callback: Optional[Callable] = None, **kwargs):
    """
    Supervised runner.

    Behavior:
      - If environment variable LUX_SUPERVISED != "1": act as monitor:
          spawn a child process running the same Python interpreter and same argv
          with LUX_SUPERVISED=1 set. Wait for child to exit. If exitcode != 0,
          show BSOD in monitor process with child's stderr/stdout and give option
          to restart child (Attempt Restart).
      - If LUX_SUPERVISED == "1": behave like previous run_with_bsod: run
        main_callable inside try/except so Python exceptions become non-zero exits.
    """
    SUP_ENV = "LUX_SUPERVISED"

    # MONITOR mode
    if os.environ.get(SUP_ENV) != "1":
        # We're the monitor process.
        while True:
            env = os.environ.copy()
            env[SUP_ENV] = "1"

            try:
                # spawn child: same interpreter + same argv
                p = subprocess.Popen(
                    [sys.executable] + sys.argv,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    text=True
                )
            except Exception as e:
                details = f"Failed to spawn child process: {e}\n\nTraceback:\n{traceback.format_exc()}"
                # show BSOD and then return non-zero
                _show_bsod(details=details, code=None, restart_callback=restart_callback)
                return 1

            out, err = p.communicate()
            code = p.returncode if p.returncode is not None else -1

            # If child exits cleanly, exit monitor cleanly
            if code == 0:
                return 0

            # child crashed or returned non-zero -> show BSOD with child's output
            details = (
                f"Child process exited with code {code}\n\n"
                f"=== STDOUT ===\n{out}\n\n"
                f"=== STDERR ===\n{err}\n\n"
                "This may be a Python exception or a native crash (access violation, etc.)."
            )

            # event to indicate user requested restart
            restart_event = threading.Event()

            def _set_restart():
                try:
                    restart_event.set()
                except Exception:
                    pass

            # show BSOD; pass restart setter so when user clicks Attempt Restart we set the event
            _show_bsod(details=details, code=code, restart_callback=_set_restart)

            if restart_event.is_set():
                # user requested restart -> loop to spawn child again
                continue
            else:
                # user quit or closed BSOD -> exit with child's code
                try:
                    return int(code)
                except Exception:
                    return 1

    # SUPERVISED (child) mode
    else:
        # We're the child process; run the main_callable and ensure exceptions lead to non-zero exit.
        try:
            orig_hook = sys.excepthook

            def _child_excepthook(tp, val, tb):
                # Print full traceback to stderr so monitor can capture it
                traceback.print_exception(tp, val, tb, file=sys.stderr)
                # call original hook if present
                try:
                    if callable(orig_hook):
                        orig_hook(tp, val, tb)
                except Exception:
                    pass
                # force non-zero exit so monitor will show BSOD
                os._exit(1)

            sys.excepthook = _child_excepthook

            # Run main callable (expected to create QApplication and exec)
            main_callable(*args, **kwargs)

            # If we reach here normally, return 0 to monitor
            return 0
        except SystemExit as se:
            # Let monitor detect this via exit code (re-raise)
            raise
        except Exception:
            # print traceback to stderr for monitor to capture then exit non-zero
            traceback.print_exc(file=sys.stderr)
            os._exit(1)