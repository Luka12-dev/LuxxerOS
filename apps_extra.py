import sys
import random
import datetime

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QProgressBar, QSpinBox, QLabel, QGridLayout, QSizePolicy, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import QTimer, Qt

import sys
import random
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QProgressBar
)
from PyQt6.QtCore import QTimer


# hacker_simulator_fixed.py
import sys
import random
import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QLineEdit, QProgressBar, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QIcon, QTextCursor
from PyQt6.QtCore import QTimer, Qt


class HackerSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hacker Simulator")
        try:
            self.setWindowIcon(QIcon('icon.ico'))
        except Exception:
            pass
        self.resize(800, 520)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Terminal output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background: #000; color: #66ff66; font-family: monospace;")

        # Input line
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type command (help)")

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setVisible(False)

        # Buttons
        controls = QHBoxLayout()
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self._cmd_clear)
        self.btn_help = QPushButton("Help")
        self.btn_help.clicked.connect(lambda: self._queue_output(self._help_text()))
        controls.addWidget(self.btn_clear)
        controls.addWidget(self.btn_help)
        controls.addStretch()

        # Layout
        layout.addWidget(self.output, 1)
        layout.addLayout(controls)
        layout.addWidget(self.progress)
        layout.addWidget(self.input)
        self.setCentralWidget(central)

        # Typing effect
        self._typing_timer = QTimer()
        self._typing_timer.setInterval(20)  # faster typing
        self._typing_timer.timeout.connect(self._type_step)
        self._typing_queue = []
        self._type_buffer = ""
        self._type_index = 0
        self._typing_active = False

        self.input.returnPressed.connect(self._on_enter)

        # show welcome
        self._queue_output("Hacker Simulator v1.0\nType 'help' for commands.\n")

    def _help_text(self):
        return (
            "Available commands:\n"
            "  help                 show this text\n"
            "  clear                clear terminal\n"
            "  hack <target>        fake hack target (e.g. hack nasa)\n"
            "  scan <ip>            fake network scan\n"
            "  echo <text>          print text\n"
            "  ping <host>          fake ping test\n"
            "  whoami               show fake username\n"
            "  ls                   list fake files\n"
            "  cd <dir>             change fake directory\n"
            "  date                 show system date/time\n"
            "  exit                 close simulator\n"
        )

    def _on_enter(self):
        txt = self.input.text().strip()
        self.input.clear()
        if not txt:
            return
        self._append_now(f"> {txt}\n")

        parts = txt.split()
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd == "help":
                self._queue_output(self._help_text())
            elif cmd == "clear":
                self._cmd_clear()
            elif cmd == "hack":
                target = " ".join(args) or "target"
                self._simulate_hack(target)
            elif cmd == "scan":
                target = args[0] if args else "192.168.0.0/24"
                self._simulate_scan(target)
            elif cmd == "echo":
                self._queue_output(" ".join(args) + "\n")
            elif cmd == "ping":
                host = args[0] if args else "127.0.0.1"
                self._simulate_ping(host)
            elif cmd == "whoami":
                self._queue_output("root\n")
            elif cmd == "ls":
                fake_files = ["main.py", "passwords.txt", "secrets.db", "exploit.sh"]
                self._queue_output("\n".join(fake_files) + "\n")
            elif cmd == "cd":
                if args:
                    self._queue_output(f"Changed directory to {args[0]}\n")
                else:
                    self._queue_output("cd: missing argument\n")
            elif cmd == "date":
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._queue_output(now + "\n")
            elif cmd == "exit":
                self.close()
            else:
                self._queue_output(f"Unknown command: {cmd}\n")
        except Exception as e:
            # be friendly but informative
            self._queue_output(f"Error while executing command: {e}\n")

    def _append_now(self, text: str):
        """
        Insert text immediately into QTextEdit at the end (safe cursor operations).
        """
        cursor = self.output.textCursor()
        # move to end, insert text, then ensure visible
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    # Typing effect queue
    def _queue_output(self, text):
        self._typing_queue.append(str(text))
        if not self._typing_active:
            self._start_typing()

    def _start_typing(self):
        if not self._typing_queue:
            self._typing_active = False
            return
        self._type_buffer = self._typing_queue.pop(0)
        self._type_index = 0
        self._typing_active = True
        self._typing_timer.start()

    def _type_step(self):
        if self._type_index >= len(self._type_buffer):
            self._typing_timer.stop()
            self._typing_active = False
            # small pause before next line (optional)
            QTimer.singleShot(50, self._start_typing)
            return
        self._append_now(self._type_buffer[self._type_index])
        self._type_index += 1

    # Commands
    def _cmd_clear(self):
        self.output.clear()

    def _simulate_hack(self, target):
        lines = [
            f"Connecting to {target}...",
            "Establishing secure channel...",
            "Bypassing firewall...",
            "Deploying exploits...",
            "Extracting data...",
            "Uploading rootkit...",
            "Cleaning traces...",
            f"Hack on {target} complete. Data saved to /tmp/{target}_dump.bin"
        ]
        self.progress.setVisible(True)
        self.progress.setValue(0)
        total = len(lines)

        def progress_tick(i):
            # update progress and queue line to output
            percent = int((i + 1) / total * 100)
            self.progress.setValue(percent)
            self._queue_output(lines[i] + "\n")
            if i + 1 == total:
                # hide progress after a short delay so user sees 100%
                QTimer.singleShot(400, lambda: self.progress.setVisible(False))

        for i in range(total):
            QTimer.singleShot(600 * i, lambda i=i: progress_tick(i))

    def _simulate_scan(self, target):
        n = random.randint(4, 10)
        out = [f"Scanning {target} ...\n"]
        for i in range(n):
            ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            port = random.choice([22, 80, 443, 3389, 8080, 3306])
            serv = random.choice(["ssh", "http", "https", "rdp", "mysql", "http-proxy"])
            out.append(f"{ip}:{port} - {serv}\n")
        self._queue_output("".join(out))

    def _simulate_ping(self, host):
        self._queue_output(f"Pinging {host} with 32 bytes of data:\n")
        for i in range(4):
            delay = random.randint(10, 120)
            self._queue_output(f"Reply from {host}: bytes=32 time={delay}ms TTL=64\n")
        self._queue_output("Ping statistics: 4 packets transmitted, 4 received, 0% loss\n")

# ASCIIPainterApp

class ASCIIPainterApp(QMainWindow):
    def __init__(self, cols=40, rows=20, cell_size=16):
        super().__init__()
        self.setWindowTitle("ASCII Painter")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(900, 600)

        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.grid = [[False]*cols for _ in range(rows)]

        central = QWidget()
        main_l = QVBoxLayout(central)
        top_l = QHBoxLayout()
        self.btn_save = QPushButton("Save ASCII")
        self.btn_clear = QPushButton("Clear")
        self.btn_invert = QPushButton("Invert")
        self.spin_cols = QSpinBox(); self.spin_cols.setRange(8,120); self.spin_cols.setValue(self.cols)
        self.spin_rows = QSpinBox(); self.spin_rows.setRange(4,80); self.spin_rows.setValue(self.rows)
        self.btn_resize = QPushButton("Resize Grid")
        top_l.addWidget(self.btn_save); top_l.addWidget(self.btn_clear); top_l.addWidget(self.btn_invert)
        top_l.addStretch()
        top_l.addWidget(QLabel("Cols:")); top_l.addWidget(self.spin_cols)
        top_l.addWidget(QLabel("Rows:")); top_l.addWidget(self.spin_rows)
        top_l.addWidget(self.btn_resize)

        self.canvas = QWidget()
        self.canvas_layout = QGridLayout(self.canvas)
        self.canvas_layout.setSpacing(1)
        self.canvas_layout.setContentsMargins(4,4,4,4)
        self._create_grid_widgets()

        main_l.addLayout(top_l)
        main_l.addWidget(self.canvas, 1)
        self.setCentralWidget(central)

        self.btn_save.clicked.connect(self.save_ascii)
        self.btn_clear.clicked.connect(self.clear_grid)
        self.btn_invert.clicked.connect(self.invert_grid)
        self.btn_resize.clicked.connect(self.resize_grid)

    def _create_grid_widgets(self):
        # clear layout
        for i in reversed(range(self.canvas_layout.count())):
            w = self.canvas_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.cell_widgets = []
        for r in range(self.rows):
            row_widgets = []
            for c in range(self.cols):
                b = QPushButton()
                b.setFixedSize(self.cell_size, self.cell_size)
                b.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                b.setStyleSheet("background: #ffffff; border: 1px solid #ddd;")
                b.clicked.connect(lambda _, rr=r, cc=c: self._toggle_cell(rr, cc))
                self.canvas_layout.addWidget(b, r, c)
                row_widgets.append(b)
            self.cell_widgets.append(row_widgets)
        self._refresh_grid_ui()

    def _toggle_cell(self, r, c):
        self.grid[r][c] = not self.grid[r][c]
        self._refresh_cell(r, c)

    def _refresh_cell(self, r, c):
        btn = self.cell_widgets[r][c]
        if self.grid[r][c]:
            btn.setStyleSheet("background: #000000; border: 1px solid #222;")
        else:
            btn.setStyleSheet("background: #ffffff; border: 1px solid #ddd;")

    def _refresh_grid_ui(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self._refresh_cell(r, c)

    def clear_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = False
        self._refresh_grid_ui()

    def invert_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = not self.grid[r][c]
        self._refresh_grid_ui()

    def resize_grid(self):
        self.cols = int(self.spin_cols.value())
        self.rows = int(self.spin_rows.value())
        # rebuild logical grid preserving as much as possible
        new_grid = [[False]*self.cols for _ in range(self.rows)]
        for r in range(min(self.rows, len(self.grid))):
            for c in range(min(self.cols, len(self.grid[0]) if self.grid else 0)):
                new_grid[r][c] = self.grid[r][c]
        self.grid = new_grid
        self._create_grid_widgets()

    def save_ascii(self):
        txt = []
        for r in range(self.rows):
            line = "".join("#" if self.grid[r][c] else "." for c in range(self.cols))
            txt.append(line)
        content = "\n".join(txt)
        path, _ = QFileDialog.getSaveFileName(self, "Save ASCII Art", "ascii_art.txt", "Text Files (*.txt);;All Files (*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                QMessageBox.information(self, "Saved", f"Saved to: {path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save: {e}")

# FortuneTellerApp

class FortuneTellerApp(QMainWindow):
    DEFAULT_FORTUNES = [
        "Today you will find a new idea. 🌟",
        "Take a short walk — it will clear your mind. 🚶",
        "You will solve a tricky bug soon. 🐛✅",
        "Reach out to a friend you haven't talked to in a while. 🤝",
        "Try something small that scares you a bit — growth follows. 🌱",
        "A surprise is coming — be open to it. 🎁",
        "Create one thing today, even if small. 🛠️",
        "Drink water. Simple, but effective. 💧",
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Fortune / Challenge")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(560, 360)

        central = QWidget()
        layout = QVBoxLayout(central)
        top = QHBoxLayout()
        self.lbl = QLabel("Press 'Generate' for a fortune or challenge")
        self.lbl.setWordWrap(True)
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_gen = QPushButton("Generate")
        self.btn_copy = QPushButton("Copy")
        self.btn_history = QPushButton("History")
        self.history = []
        top.addWidget(self.btn_gen)
        top.addWidget(self.btn_copy)
        top.addWidget(self.btn_history)

        layout.addWidget(self.lbl, 1)
        layout.addLayout(top)

        self.setCentralWidget(central)

        self.btn_gen.clicked.connect(self.generate)
        self.btn_copy.clicked.connect(self.copy_current)
        self.btn_history.clicked.connect(self.show_history)

        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(60)
        self._anim_text = ""
        self._anim_index = 0
        self._anim_timer.timeout.connect(self._anim_step)

    def generate(self):
        fortune = random.choice(self.DEFAULT_FORTUNES)
        # small animation: type it out
        self._anim_text = fortune
        self._anim_index = 0
        self.lbl.setText("")
        self._anim_timer.start()
        # record in history with timestamp
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.insert(0, f"[{ts}] {fortune}")
        if len(self.history) > 50:
            self.history = self.history[:50]

    def _anim_step(self):
        if self._anim_index >= len(self._anim_text):
            self._anim_timer.stop()
            return
        self.lbl.setText(self.lbl.text() + self._anim_text[self._anim_index])
        self._anim_index += 1

    def copy_current(self):
        text = self.lbl.text().strip()
        if not text:
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Fortune copied to clipboard.")

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "History", "No fortunes yet.")
            return
        # show a simple dialog with history
        dlg = QMainWindow(self)
        dlg.setWindowTitle("History")
        w = QWidget()
        l = QVBoxLayout(w)
        te = QTextEdit()
        te.setReadOnly(True)
        te.setPlainText("\n".join(self.history))
        l.addWidget(te)
        close = QPushButton("Close")
        close.clicked.connect(dlg.close)
        l.addWidget(close)
        dlg.setCentralWidget(w)
        dlg.resize(480, 320)
        dlg.show()