# JokeGenerator.py
import sys
import os
import json
import random
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt

try:
    from settings_utils import save_state, load_state
except Exception:
    save_state = None
    load_state = None

STATE_FILE = "jokes_state.json"

DEFAULT_JOKES = [
    "Why did the developer go broke? Because he used up all his cache.",
    "Why do Python programmers wear glasses? Because they can’t C.",
    "I told my computer I needed a break, and it said: 'No problem — I’ll go to sleep.'",
    "Why did the function return early? It had commitment issues.",
    "Why are assembly programmers always soaking wet? They work below C-level.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why don’t programmers like nature? Too many bugs."
]

def _load():
    if callable(load_state):
        try:
            return load_state() or {}
        except Exception:
            pass
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            traceback.print_exc()
    return {"last_index": -1, "favorites": []}

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

class JokeGeneratorApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jokes — Luxxer")
        self.resize(600, 380)
        self.state = _load()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.joke_view = QTextEdit()
        self.joke_view.setReadOnly(True)
        self.joke_view.setFixedHeight(140)
        layout.addWidget(self.joke_view)

        btn_row = QHBoxLayout()
        self.next_btn = QPushButton("Next Joke")
        self.fav_btn = QPushButton("★ Favorite")
        self.show_fav_btn = QPushButton("Show Favorites")
        btn_row.addWidget(self.next_btn)
        btn_row.addWidget(self.fav_btn)
        btn_row.addWidget(self.show_fav_btn)
        layout.addLayout(btn_row)

        self.fav_list = QListWidget()
        self.fav_list.setVisible(False)
        layout.addWidget(self.fav_list, 1)

        self.jokes = DEFAULT_JOKES.copy()
        self.last_index = self.state.get("last_index", -1)
        self.favorites = self.state.get("favorites", [])

        self.next_btn.clicked.connect(self.next_joke)
        self.fav_btn.clicked.connect(self.toggle_favorite)
        self.show_fav_btn.clicked.connect(self.toggle_fav_view)

        self.next_joke()

    def next_joke(self):
        # try to not repeat last one if possible
        idx = self.last_index
        if len(self.jokes) == 0:
            self.joke_view.setPlainText("No jokes available.")
            return
        attempts = 0
        while attempts < 10:
            new_idx = random.randrange(0, len(self.jokes))
            if new_idx != self.last_index or len(self.jokes) == 1:
                idx = new_idx
                break
            attempts += 1
        self.last_index = idx
        joke = self.jokes[idx]
        self.joke_view.setPlainText(joke)
        self.state['last_index'] = self.last_index
        _save(self.state)

    def toggle_favorite(self):
        if self.last_index < 0 or self.last_index >= len(self.jokes):
            return
        joke = self.jokes[self.last_index]
        if joke in self.favorites:
            self.favorites.remove(joke)
            QMessageBox.information(self, "Favorite", "Removed from favorites.")
        else:
            self.favorites.append(joke)
            QMessageBox.information(self, "Favorite", "Added to favorites.")
        self.state['favorites'] = self.favorites
        _save(self.state)
        self._refresh_favs()

    def toggle_fav_view(self):
        self.fav_list.setVisible(not self.fav_list.isVisible())
        self._refresh_favs()

    def _refresh_favs(self):
        self.fav_list.clear()
        for j in self.favorites:
            self.fav_list.addItem(j)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = JokeGeneratorApp()
    w.show()
    sys.exit(app.exec())