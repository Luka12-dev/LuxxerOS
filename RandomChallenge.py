import sys
import os
import json
import datetime
import random
import traceback

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QListWidget, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

# try to reuse global settings_utils if available
try:
    from settings_utils import save_state, load_state
except Exception:
    save_state = None
    load_state = None

STATE_FILE = "random_challenge_state.json"

def _save_local(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        traceback.print_exc()

def _load_local():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            traceback.print_exc()
    return {}

DEFAULT_CHALLENGES = [
    {"id": "open_new_app", "text": "Open an app you didn't use today.", "xp": 10},
    {"id": "screenshot_cool", "text": "Take a creative screenshot and save it.", "xp": 8},
    {"id": "clean_desktop", "text": "Hide/organize at least 3 icons on desktop.", "xp": 6},
    {"id": "try_app", "text": "Try a random app from the App Store section.", "xp": 12},
    {"id": "mini_script", "text": "Write a 5-line script that prints 'Hello Luxxer'.", "xp": 15},
    {"id": "learn_short", "text": "Read one short article or doc for 10 minutes.", "xp": 7},
    {"id": "screenshot_share", "text": "Share your desktop setup (save to file).", "xp": 5},
    {"id": "mini_challenge_code", "text": "Solve a short coding puzzle (10 minutes).", "xp": 20},
]

class RandomChallengeApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daily Challenge - Luxxer")
        self.resize(560, 420)

        # load state via settings_utils if available, else local file
        if callable(load_state):
            try:
                self.state = load_state() or {}
            except Exception:
                self.state = _load_local()
        else:
            self.state = _load_local()

        self.state.setdefault("challenges", {})
        self.state["challenges"].setdefault("xp", 0)
        self.state["challenges"].setdefault("history", {})  # date -> {id, done, xp}

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.info_label = QLabel("Daily challenge — earn XP and collect streaks!")
        layout.addWidget(self.info_label)

        self.challenge_text = QTextEdit()
        self.challenge_text.setReadOnly(True)
        self.challenge_text.setFixedHeight(120)
        layout.addWidget(self.challenge_text)

        btn_row = QHBoxLayout()
        self.btn_done = QPushButton("Mark as Done")
        self.btn_skip = QPushButton("Skip / Next")
        self.btn_details = QPushButton("Show History")
        btn_row.addWidget(self.btn_done)
        btn_row.addWidget(self.btn_skip)
        btn_row.addWidget(self.btn_details)
        layout.addLayout(btn_row)

        self.xp_label = QLabel(f"Total XP: {self.state['challenges']['xp']}")
        layout.addWidget(self.xp_label)

        self.history_list = QListWidget()
        self.history_list.setVisible(False)
        layout.addWidget(self.history_list, 1)

        # signals
        self.btn_done.clicked.connect(self.mark_done)
        self.btn_skip.clicked.connect(self.skip_challenge)
        self.btn_details.clicked.connect(self.toggle_history)

        # pick today's challenge deterministically (by date) but allow skip to change
        self.challenges = DEFAULT_CHALLENGES.copy()
        self.today = datetime.date.today().isoformat()
        self.current_idx = self._deterministic_index(self.today)
        # if already marked done today, show that
        self._refresh_ui()

    def _deterministic_index(self, date_str):
        # deterministic but pseudo-random index per date
        h = sum(ord(c) for c in date_str)
        return h % len(self.challenges)

    def _current_challenge(self):
        idx = self.current_idx % len(self.challenges)
        return self.challenges[idx]

    def _refresh_ui(self):
        chal = self._current_challenge()
        self.challenge_text.setPlainText(f"{chal['text']}\n\nReward: {chal['xp']} XP")
        done_today = self.state['challenges']['history'].get(self.today, {})
        if done_today.get("done") and done_today.get("id") == chal["id"]:
            self.btn_done.setEnabled(False)
            self.info_label.setText(f"Today's challenge already completed (+{done_today.get('xp', 0)} XP).")
        else:
            self.btn_done.setEnabled(True)
            self.info_label.setText("Complete today's challenge to earn XP.")
        self.xp_label.setText(f"Total XP: {self.state['challenges']['xp']}")
        # refresh history list
        self.history_list.clear()
        hist = self.state['challenges']['history']
        for date in sorted(hist.keys(), reverse=True)[:50]:
            e = hist[date]
            st = f"{date}: {e.get('id')} — {'Done' if e.get('done') else 'Skipped'} (+{e.get('xp',0)} XP)"
            self.history_list.addItem(st)

    def mark_done(self):
        chal = self._current_challenge()
        # avoid double awarding
        today_entry = self.state['challenges']['history'].get(self.today, {})
        if today_entry.get("done") and today_entry.get("id") == chal["id"]:
            QMessageBox.information(self, "Already done", "You already completed today's challenge.")
            return
        xp = chal.get("xp", 5)
        self.state['challenges']['xp'] += xp
        self.state['challenges']['history'][self.today] = {"id": chal["id"], "done": True, "xp": xp}
        self._persist_state()
        QMessageBox.information(self, "Nice!", f"Challenge completed — +{xp} XP awarded.")
        self._refresh_ui()

    def skip_challenge(self):
        # move to next available challenge for today (non-destructive)
        self.current_idx = (self.current_idx + 1) % len(self.challenges)
        self._refresh_ui()

    def toggle_history(self):
        self.history_list.setVisible(not self.history_list.isVisible())

    def _persist_state(self):
        if callable(save_state):
            try:
                save_state(self.state)
                return
            except Exception:
                traceback.print_exc()
        _save_local(self.state)