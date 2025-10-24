import sys
import os
import json
import random
import traceback
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout, QLabel, QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QIcon

# Persistence
try:
    BASE_DIR = os.path.dirname(__file__) or os.getcwd()
except Exception:
    BASE_DIR = os.getcwd()
STATE_FILE = os.path.join(BASE_DIR, "motivation_chat_state.json")


def _load_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        traceback.print_exc()
    return {"history": []}


def _save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        traceback.print_exc()

# Chat logic
ENCOURAGEMENTS = [
    "You're doing great — keep going!",
    "Small steps add up. One step at a time.",
    "Remember: progress, not perfection.",
    "You've handled hard things before. You can do this too.",
    "Breathe. Focus on the next tiny task.",
    "Every effort counts — proud of you for trying."
]

REFLECT_PROMPTS = [
    "What is the one small thing you can do right now?",
    "What's a tiny win from today?",
    "If you could remove one distraction, what would it be?"
]

class MotivationAIChat(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Motivation — Luxxer (safe)")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(640, 480)

        # load state
        self.state = _load_state()
        if not isinstance(self.state, dict):
            self.state = {"history": []}

        # UI
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QLabel("Motivation Chat — quick pep talks & prompts")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-weight:600; padding:6px 0;")
        layout.addWidget(header)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.chat_view, 1)

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type how you're feeling or ask for advice...")
        self.send_btn = QPushButton("Send")
        self.boost_btn = QPushButton("Motivation Boost")
        row.addWidget(self.input, 1)
        row.addWidget(self.send_btn)
        row.addWidget(self.boost_btn)
        layout.addLayout(row)

        ctrl_row = QHBoxLayout()
        self.clear_btn = QPushButton("Clear History")
        self.export_btn = QPushButton("Export")
        self.import_btn = QPushButton("Import")
        ctrl_row.addWidget(self.clear_btn)
        ctrl_row.addWidget(self.export_btn)
        ctrl_row.addWidget(self.import_btn)
        ctrl_row.addStretch()
        layout.addLayout(ctrl_row)

        # signals
        self.send_btn.clicked.connect(self.on_send)
        self.boost_btn.clicked.connect(self.on_boost)
        self.input.returnPressed.connect(self.on_send)
        self.clear_btn.clicked.connect(self.on_clear_history)
        self.export_btn.clicked.connect(self.on_export)
        self.import_btn.clicked.connect(self.on_import)

        self._render_history()

    def closeEvent(self, ev):
        try:
            _save_state(self.state)
        except Exception:
            traceback.print_exc()
        try:
            QMainWindow.closeEvent(self, ev)
        except Exception:
            ev.accept()

    def _render_history(self):
        try:
            self.chat_view.clear()
            hist = self.state.get("history", [])[-200:]
            for entry in hist:
                t = entry.get("time", "")
                who = entry.get("who", "bot")
                label = "you" if who == "you" else "bot"
                text = entry.get("text", "")
                self.chat_view.append(f"[{t}] {label}: {text}\n")
            self.chat_view.moveCursor(QTextCursor.MoveOperation.End)
        except Exception:
            traceback.print_exc()

    def _append_entry(self, who, text):
        try:
            entry = {"who": who, "text": text, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            self.state.setdefault("history", []).append(entry)
            if len(self.state["history"]) > 2000:
                self.state["history"] = self.state["history"][-2000:]
            _save_state(self.state)
            self._render_history()
        except Exception:
            traceback.print_exc()

    def on_send(self):
        try:
            txt = (self.input.text() or "").strip()
            if not txt:
                return
            self.input.clear()
            self._append_entry("you", txt)
            resp = self._generate_response(txt)
            self._append_entry("bot", resp)
        except Exception:
            traceback.print_exc()

    def on_boost(self):
        try:
            resp = random.choice(ENCOURAGEMENTS)
            self._append_entry("bot", resp)
        except Exception:
            traceback.print_exc()

    def on_clear_history(self):
        try:
            choice = QMessageBox.question(self, "Clear history", "Are you sure you want to clear chat history?")
            if choice == QMessageBox.StandardButton.Yes:
                self.state["history"] = []
                _save_state(self.state)
                self._render_history()
        except Exception:
            traceback.print_exc()

    def on_export(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Export history", "motivation_history.json", "JSON Files (*.json);;All Files (*)")
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.state.get("history", []), f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Export", "Exported to: " + str(path))
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Export failed", "Could not export history.")

    def on_import(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Import history", "", "JSON Files (*.json);;All Files (*)")
            if path:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for it in data:
                        if isinstance(it, dict) and "text" in it:
                            self.state.setdefault("history", []).append(it)
                    _save_state(self.state)
                    self._render_history()
                    QMessageBox.information(self, "Import", "Import complete.")
                else:
                    QMessageBox.warning(self, "Import", "File doesn't look like exported history.")
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Import failed", "Could not import history.")

    def _generate_response(self, text: str) -> str:
        try:
            t = (text or "").lower()
            if any(w in t for w in ("sad", "depress", "down", "unhappy", "lonely")):
                return "I'm sorry you're feeling down. It's okay to take a short break. What would help right now?"
            if any(w in t for w in ("tired", "exhaust", "sleep", "sleepy")):
                return "Maybe a short rest or a glass of water could help. What if you try 10 minutes of rest and then one small task?"
            if any(w in t for w in ('stuck', 'blocked', "can't", 'cannot', 'stagnant')):
                return "Try breaking the task into a tiny first step. What's one simple thing you can do right now?"
            if "help" in t or "advice" in t:
                return random.choice(REFLECT_PROMPTS)
            if any(w in t for w in ("done", "finished", "completed", "yay", "hooray")):
                return "Amazing — celebrate that win! Small wins stack into big ones."
            return random.choice(ENCOURAGEMENTS) + " What is one small next step?"
        except Exception:
            traceback.print_exc()
            return random.choice(ENCOURAGEMENTS)