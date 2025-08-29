# MotivationAIChat.py
import sys
import os
import json
import random
import traceback
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt

# persistence fallback
try:
    from settings_utils import save_state, load_state
except Exception:
    save_state = None
    load_state = None

STATE_FILE = "motivation_chat_state.json"

def _load():
    if callable(load_state):
        try:
            return load_state()
        except Exception:
            pass
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            traceback.print_exc()
    return {"history": []}

def _save(state):
    if callable(save_state):
        try:
            save_state(state)
            return
        except Exception:
            pass
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        traceback.print_exc()

# Simple local "motivator" responses (no network)
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
    """Local motivational chat — no external AI calls."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Motivation — Luxxer")
        self.resize(620, 480)

        self.state = _load()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.header = QLabel("Motivation Chat — quick pep talks & prompts")
        layout.addWidget(self.header)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        layout.addWidget(self.chat_view, 1)

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.send_btn = QPushButton("Send")
        self.boost_btn = QPushButton("Motivation Boost")
        row.addWidget(self.input, 1)
        row.addWidget(self.send_btn)
        row.addWidget(self.boost_btn)
        layout.addLayout(row)

        # load history
        self._render_history()

        # signals
        self.send_btn.clicked.connect(self.on_send)
        self.boost_btn.clicked.connect(self.on_boost)
        self.input.returnPressed.connect(self.on_send)

    def _render_history(self):
        self.chat_view.clear()
        for entry in self.state.get("history", [])[-200:]:
            t = entry.get("time", "")
            who = entry.get("who", "bot" if entry.get("who")=="bot" else "you")
            self.chat_view.append(f"[{t}] {who}: {entry['text']}\n")

    def _append(self, who, text):
        entry = {"who": who, "text": text, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.state.setdefault("history", []).append(entry)
        _save(self.state)
        self._render_history()

    def on_send(self):
        txt = self.input.text().strip()
        if not txt:
            return
        self._append("you", txt)
        self.input.clear()
        # generate a simple local response
        response = self._generate_response(txt)
        self._append("bot", response)

    def on_boost(self):
        response = random.choice(ENCOURAGEMENTS)
        self._append("bot", response)

    def _generate_response(self, text: str) -> str:
        """Very small rule-based motivator: reflection, empathy, short pep talk."""
        t = text.lower()
        if any(w in t for w in ("sad", "depress", "down", "unhappy")):
            return "I'm sorry you're feeling down. It's okay to take a short break. What would help right now?"
        if any(w in t for w in ("tired", "exhaust", "sleep")):
            return "Maybe a short rest or a glass of water could help. What if you try 10 minutes of rest and then one small task?"
        if any(w in t for w in ("stuck", "blocked", "can't", "cannot", "stuck")):
            return "Try breaking the task into a tiny first step. What's one simple thing you can do right now?"
        if "help" in t or "advice" in t:
            return random.choice(REFLECT_PROMPTS)
        # if it's a celebration
        if any(w in t for w in ("done", "finished", "completed", "yay")):
            return "Amazing — celebrate that win! Small wins stack into big ones."
        # otherwise short encouragement and a question
        return random.choice(ENCOURAGEMENTS) + " What is one small next step?"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MotivationAIChat()
    w.show()
    sys.exit(app.exec())