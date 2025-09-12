import os
import json
import random
import math
import shutil
from pathlib import Path
from datetime import date, datetime, timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QLineEdit, QTextEdit, QFileDialog, QMessageBox,
    QSpinBox, QComboBox, QColorDialog, QListWidgetItem, QFormLayout, QInputDialog
)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage, QIcon
from PyQt6.QtCore import Qt, QTimer, QSize

# Optional imports detection
try:
    import qrcode
    QR_AVAILABLE = True
except Exception:
    QR_AVAILABLE = False

try:
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
    MULTIMEDIA_AVAILABLE = True
except Exception:
    MULTIMEDIA_AVAILABLE = False

# Data dir
DATA_DIR = Path.cwd() / "luxxer_extra_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# HabitTrackerApp

class HabitTrackerApp(QMainWindow):
    FILE = DATA_DIR / "habit_tracker.json"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(480, 520)
        self.store = {}
        self._load()

        central = QWidget()
        v = QVBoxLayout(central)

        add_row = QHBoxLayout()
        self.habit_input = QLineEdit()
        self.habit_input.setPlaceholderText("New habit (e.g. 'Meditate')")
        self.btn_add = QPushButton("Add Habit")
        add_row.addWidget(self.habit_input); add_row.addWidget(self.btn_add)
        v.addLayout(add_row)

        self.listw = QListWidget()
        v.addWidget(self.listw, 1)

        btn_row = QHBoxLayout()
        self.btn_check = QPushButton("Mark Today Done")
        self.btn_uncheck = QPushButton("Unmark Today")
        self.btn_remove = QPushButton("Remove Habit")
        btn_row.addWidget(self.btn_check); btn_row.addWidget(self.btn_uncheck); btn_row.addWidget(self.btn_remove)
        v.addLayout(btn_row)

        self.stats = QLabel("Select a habit to see streak info.")
        v.addWidget(self.stats)

        self.setCentralWidget(central)

        self.btn_add.clicked.connect(self.add_habit)
        self.btn_check.clicked.connect(lambda: self.toggle_today(True))
        self.btn_uncheck.clicked.connect(lambda: self.toggle_today(False))
        self.btn_remove.clicked.connect(self.remove_habit)
        self.listw.currentItemChanged.connect(self.update_stats)

        self._refresh_list()

    def _load(self):
        try:
            if self.FILE.exists():
                self.store = json.loads(self.FILE.read_text(encoding="utf-8"))
            else:
                self.store = {}
        except Exception:
            self.store = {}

    def _save(self):
        try:
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self.store, f, indent=2)
        except Exception:
            pass

    def add_habit(self):
        name = self.habit_input.text().strip()
        if not name: return
        if name in self.store:
            QMessageBox.information(self, "Exists", "Habit already exists.")
            return
        self.store[name] = []  # list of ISO dates as strings
        self.habit_input.clear()
        self._save()
        self._refresh_list()

    def _refresh_list(self):
        self.listw.clear()
        for h in sorted(self.store.keys()):
            item = QListWidgetItem(h)
            self.listw.addItem(item)
        self.update_stats()

    def toggle_today(self, mark=True):
        it = self.listw.currentItem()
        if not it: return
        name = it.text()
        today_s = date.today().isoformat()
        lst = set(self.store.get(name, []))
        if mark:
            lst.add(today_s)
        else:
            lst.discard(today_s)
        self.store[name] = sorted(lst)
        self._save()
        self.update_stats()

    def remove_habit(self):
        it = self.listw.currentItem()
        if not it: return
        name = it.text()
        if QMessageBox.question(self, "Remove", f"Remove habit '{name}'?") != QMessageBox.StandardButton.Yes:
            return
        self.store.pop(name, None)
        self._save()
        self._refresh_list()

    def update_stats(self):
        it = self.listw.currentItem()
        if not it:
            self.stats.setText("Select a habit to see streak info.")
            return
        name = it.text()
        dates = [date.fromisoformat(s) for s in self.store.get(name, [])]
        dates = sorted(dates)
        today = date.today()
        # current streak
        streak = 0
        d = today
        while d in dates:
            streak += 1
            d = d - timedelta(days=1)
        # longest streak
        longest = 0
        current = 0
        last = None
        for dt in dates:
            if last is None or (dt - last).days == 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 1
            last = dt
        longest = max(longest, current)
        self.stats.setText(f"Habit: {name}\nToday done: {'Yes' if today in dates else 'No'}\nStreak: {streak}\nLongest: {longest}\nTotal days: {len(dates)}")

# PomodoroApp

class PomodoroApp(QMainWindow):
    FILE = DATA_DIR / "pomodoro.json"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(360, 220)
        self.state = {"work":25, "short":5, "long":15, "cycles":4}
        self._load()

        central = QWidget()
        v = QVBoxLayout(central)

        cfg = QHBoxLayout()
        self.spin_work = QSpinBox(); self.spin_work.setRange(5, 90); self.spin_work.setValue(self.state["work"]); self.spin_work.setSuffix(" min")
        self.spin_short = QSpinBox(); self.spin_short.setRange(1, 30); self.spin_short.setValue(self.state["short"]); self.spin_short.setSuffix(" min")
        cfg.addWidget(QLabel("Work:")); cfg.addWidget(self.spin_work); cfg.addWidget(QLabel("Break:")); cfg.addWidget(self.spin_short)
        v.addLayout(cfg)

        self.lbl_timer = QLabel("25:00")
        self.lbl_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_timer.setStyleSheet("font-size:28px;")
        v.addWidget(self.lbl_timer)

        row = QHBoxLayout()
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_reset = QPushButton("Reset")
        row.addWidget(self.btn_start); row.addWidget(self.btn_stop); row.addWidget(self.btn_reset)
        v.addLayout(row)

        self.setCentralWidget(central)

        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_reset.clicked.connect(self.reset)

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._running = False
        self._mode = "work"  # work/short/long
        self._remaining = int(self.state["work"]*60)
        self._update_label()

    def _load(self):
        try:
            p = self.FILE
            if p.exists():
                self.state.update(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f)
        except Exception:
            pass

    def _update_label(self):
        m = self._remaining // 60
        s = self._remaining % 60
        self.lbl_timer.setText(f"{m:02d}:{s:02d}")

    def start(self):
        self.state["work"] = self.spin_work.value()
        self.state["short"] = self.spin_short.value()
        self._save()
        if self._running: return
        self._running = True
        if self._mode == "work":
            self._remaining = int(self.state["work"]*60)
        self._timer.start()

    def stop(self):
        self._running = False
        self._timer.stop()

    def reset(self):
        self.stop()
        self._remaining = int(self.state["work"]*60)
        self._mode = "work"
        self._update_label()

    def _tick(self):
        if not self._running: return
        self._remaining -= 1
        if self._remaining <= 0:
            # toggle
            if self._mode == "work":
                self._mode = "short"
                self._remaining = int(self.state["short"]*60)
            else:
                self._mode = "work"
                self._remaining = int(self.state["work"]*60)
            QMessageBox.information(self, "Pomodoro", f"Switch to {self._mode} period.")
        self._update_label()

class RandomStoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Story Generator")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        central = QWidget()
        v = QVBoxLayout(central)

        self.label = QLabel("Click 'Generate' to get a random story ✨")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        v.addWidget(self.text, 1)

        self.btn = QPushButton("Generate Story")
        v.addWidget(self.btn)

        self.setCentralWidget(central)

        self.btn.clicked.connect(self.generate_story)

        # story components
        self.characters = [
            "a lonely knight", "an AI gone rogue", "a time traveler",
            "a young witch", "a cyberpunk hacker", "an alien explorer"
        ]
        self.places = [
            "in a forgotten castle", "inside a virtual reality",
            "on Mars", "deep in the forest", "in a neon city", "under the ocean"
        ]
        self.goals = [
            "searching for a lost artifact", "trying to escape",
            "seeking forbidden knowledge", "protecting a secret",
            "chasing immortality", "fighting for freedom"
        ]
        self.twists = [
            "but everything was a dream.",
            "when suddenly their best friend betrayed them.",
            "but the enemy turned out to be their sibling.",
            "yet the treasure was cursed.",
            "and the future depended on their choice."
        ]

    def generate_story(self):
        c = random.choice(self.characters)
        p = random.choice(self.places)
        g = random.choice(self.goals)
        t = random.choice(self.twists)
        story = f"Once upon a time, {c} found themselves {p}, {g}... {t}"
        self.text.setText(story)

class TravelTipsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Tips Generator")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        central = QWidget()
        v = QVBoxLayout(central)

        self.label = QLabel("Click 'Generate' to get a travel tip 🌍")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        v.addWidget(self.text, 1)

        self.btn = QPushButton("Generate Travel Tip")
        v.addWidget(self.btn)

        self.setCentralWidget(central)

        self.btn.clicked.connect(self.generate_tip)

        # travel tips pool
        self.tips = [
            "Always keep a copy of your passport and ID in your email.",
            "Learn a few basic phrases in the local language – it helps a lot.",
            "Pack light: you never need as much as you think.",
            "Try at least one traditional meal wherever you go.",
            "Wake up early to see tourist spots without the crowd.",
            "Bring a reusable water bottle – saves money and is eco-friendly.",
            "Download offline maps before your trip.",
            "Talk to locals – they know the best hidden gems.",
            "Always have some emergency cash in small bills.",
            "If possible, travel off-season: cheaper and less crowded."
        ]

    def generate_tip(self):
        tip = random.choice(self.tips)
        self.text.setText(tip)

# QRCodeGeneratorApp

class QRCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(520, 420)
        central = QWidget()
        v = QVBoxLayout(central)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Text, URL or data to encode")
        v.addWidget(self.input)
        row = QHBoxLayout()
        self.btn_gen = QPushButton("Generate")
        self.btn_save = QPushButton("Save image")
        row.addWidget(self.btn_gen); row.addWidget(self.btn_save)
        v.addLayout(row)
        self.preview = QLabel("Preview")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.preview, 1)
        self.setCentralWidget(central)

        self.btn_gen.clicked.connect(self.generate)
        self.btn_save.clicked.connect(self.save)
        self._last_img = None

        if not QR_AVAILABLE:
            QMessageBox.information(self, "qrcode library missing", "Install 'qrcode' to generate images. The app will still copy text.")

    def generate(self):
        txt = self.input.text().strip()
        if not txt:
            QMessageBox.information(self, "Empty", "Enter something to encode.")
            return
        if QR_AVAILABLE:
            img = qrcode.make(txt)
            # convert PIL image to QPixmap
            try:
                import io
                from PIL.ImageQt import ImageQt
                qimg = ImageQt(img.convert("RGB"))
                pix = QPixmap.fromImage(qimg).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
                self.preview.setPixmap(pix)
                self._last_img = img
            except Exception:
                self.preview.setText("Generated (preview unavailable).")
                self._last_img = img
        else:
            self.preview.setText("qrcode not installed — copying text to clipboard.")
            QApplication.clipboard().setText(txt)

    def save(self):
        if self._last_img is None:
            QMessageBox.information(self, "No image", "Generate QR code first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save QR", str(DATA_DIR / "qrcode.png"), "PNG (*.png)")
        if path:
            try:
                self._last_img.save(path)
                QMessageBox.information(self, "Saved", f"Saved to {path}")
            except Exception as e:
                QMessageBox.warning(self, "Save failed", str(e))

class ColorPaletteApp(QMainWindow):
    FILE = DATA_DIR / "palettes.json"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Palette")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(420, 360)
        central = QWidget()
        v = QVBoxLayout(central)
        self.listw = QListWidget()
        v.addWidget(self.listw)
        row = QHBoxLayout()
        self.btn_new = QPushButton("New Palette")
        self.btn_export = QPushButton("Export JSON")
        self.btn_delete = QPushButton("Delete")
        row.addWidget(self.btn_new); row.addWidget(self.btn_export); row.addWidget(self.btn_delete)
        v.addLayout(row)
        self.preview = QLabel()
        self.preview.setFixedHeight(80)
        v.addWidget(self.preview)
        self.setCentralWidget(central)

        self.btn_new.clicked.connect(self.new_palette)
        self.btn_export.clicked.connect(self.export_json)
        self.btn_delete.clicked.connect(self.delete_palette)
        self.listw.currentItemChanged.connect(self.update_preview)

        self.palettes = {}
        self._load()
        self._refresh_list()

    def _load(self):
        try:
            if self.FILE.exists():
                self.palettes = json.loads(self.FILE.read_text(encoding="utf-8"))
            else:
                self.palettes = {}
        except Exception:
            self.palettes = {}

    def _save(self):
        try:
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self.palettes, f, indent=2)
        except Exception:
            pass

    def new_palette(self):
        name, ok = QInputDialog.getText(self, "Name palette", "Palette name:")
        if not ok or not name.strip(): return
        colors = []
        for i in range(5):
            col = QColorDialog.getColor(QColor("#ffffff"), self, f"Pick color {i+1}")
            if col.isValid():
                colors.append(col.name())
        self.palettes[name] = colors
        self._save()
        self._refresh_list()

    def _refresh_list(self):
        self.listw.clear()
        for k in self.palettes.keys():
            self.listw.addItem(k)
        self.update_preview()

    def update_preview(self):
        it = self.listw.currentItem()
        if not it:
            self.preview.setText("Select a palette")
            return
        name = it.text()
        cols = self.palettes.get(name, [])
        img = QImage(self.preview.width(), self.preview.height(), QImage.Format.Format_RGB32)
        painter = QPainter(img)
        w = max(1, self.preview.width() // max(1, len(cols)))
        x = 0
        for c in cols:
            painter.fillRect(x, 0, w, self.preview.height(), QColor(c))
            x += w
        painter.end()
        self.preview.setPixmap(QPixmap.fromImage(img))

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export palettes", str(DATA_DIR / "palettes.json"), "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.palettes, f, indent=2)
            QMessageBox.information(self, "Exported", f"Exported to {path}")

    def delete_palette(self):
        it = self.listw.currentItem()
        if not it: return
        name = it.text()
        if QMessageBox.question(self, "Delete", f"Delete palette '{name}'?") != QMessageBox.StandardButton.Yes:
            return
        self.palettes.pop(name, None)
        self._save()
        self._refresh_list()

# RecipeBoxApp

class RecipeBoxApp(QMainWindow):
    FILE = DATA_DIR / "recipes.json"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Box")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(720, 520)
        central = QWidget()
        v = QVBoxLayout(central)
        top = QHBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText("Search by title or ingredient")
        self.btn_add = QPushButton("Add Recipe"); top.addWidget(self.input); top.addWidget(self.btn_add)
        v.addLayout(top)
        self.listw = QListWidget()
        self.view = QTextEdit(); self.view.setReadOnly(True)
        inner = QHBoxLayout(); inner.addWidget(self.listw, 1); inner.addWidget(self.view, 2)
        v.addLayout(inner)
        self.setCentralWidget(central)

        self.btn_add.clicked.connect(self.add_recipe)
        self.input.textChanged.connect(self.search)
        self.listw.currentItemChanged.connect(self.show_recipe)

        self.recipes = {}
        self._load()
        self._refresh_list()

    def _load(self):
        try:
            if self.FILE.exists():
                self.recipes = json.loads(self.FILE.read_text(encoding="utf-8"))
            else:
                self.recipes = {}
        except Exception:
            self.recipes = {}

    def _save(self):
        try:
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self.recipes, f, indent=2)
        except Exception:
            pass

    def add_recipe(self):
        title, ok = QInputDialog.getText(self, "Title", "Recipe title:")
        if not ok or not title.strip(): return
        ingredients, ok = QInputDialog.getMultiLineText(self, "Ingredients", "List ingredients (one per line):")
        if not ok: return
        steps, ok = QInputDialog.getMultiLineText(self, "Steps", "Steps / instructions:")
        if not ok: return
        self.recipes[title] = {"ingredients": ingredients.splitlines(), "steps": steps}
        self._save()
        self._refresh_list()

    def _refresh_list(self):
        self.listw.clear()
        for t in sorted(self.recipes.keys()):
            self.listw.addItem(t)
        self.show_recipe()

    def show_recipe(self):
        it = self.listw.currentItem()
        if not it:
            self.view.setPlainText("")
            return
        r = self.recipes.get(it.text(), {})
        text = f"Ingredients:\n" + "\n".join(r.get("ingredients", [])) + "\n\nSteps:\n" + r.get("steps", "")
        self.view.setPlainText(text)

    def search(self, txt=None):
        q = (txt or self.input.text() or "").lower().strip()
        self.listw.clear()
        for t, r in self.recipes.items():
            hay = t.lower() + "\n" + "\n".join(r.get("ingredients", [])).lower()
            if not q or q in hay:
                self.listw.addItem(t)

class BudgetTrackerApp(QMainWindow):
    FILE = DATA_DIR / "budget.json"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(620, 420)
        central = QWidget()
        v = QVBoxLayout(central)

        form = QHBoxLayout()
        self.input_amount = QLineEdit(); self.input_amount.setPlaceholderText("Amount")
        self.input_cat = QLineEdit(); self.input_cat.setPlaceholderText("Category")
        self.btn_add = QPushButton("Add")
        form.addWidget(self.input_amount); form.addWidget(self.input_cat); form.addWidget(self.btn_add)
        v.addLayout(form)

        self.listw = QListWidget()
        v.addWidget(self.listw, 1)
        self.stat = QLabel("Total: 0")
        v.addWidget(self.stat)
        self.setCentralWidget(central)

        self.btn_add.clicked.connect(self.add)
        self.listw.itemDoubleClicked.connect(self.remove_item)

        self.records = []
        self._load()
        self._refresh()

    def _load(self):
        try:
            if self.FILE.exists():
                self.records = json.loads(self.FILE.read_text(encoding="utf-8"))
            else:
                self.records = []
        except Exception:
            self.records = []

    def _save(self):
        try:
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2)
        except Exception:
            pass

    def add(self):
        try:
            amt = float(self.input_amount.text())
        except Exception:
            QMessageBox.warning(self, "Invalid", "Enter a numeric amount.")
            return
        cat = self.input_cat.text().strip() or "Misc"
        rec = {"amount": amt, "category": cat, "time": datetime.now().isoformat()}
        self.records.append(rec)
        self._save()
        self.input_amount.clear(); self.input_cat.clear()
        self._refresh()

    def _refresh(self):
        self.listw.clear()
        total = 0.0
        for r in reversed(self.records):
            total += float(r["amount"])
            self.listw.addItem(f"{r['time'][:19]} | {r['category']} | {r['amount']}")
        self.stat.setText(f"Total: {total:.2f}")

    def remove_item(self, item):
        row = self.listw.row(item)
        actual_index = len(self.records) - 1 - row
        if 0 <= actual_index < len(self.records):
            del self.records[actual_index]
            self._save()
            self._refresh()

#  TerminalGamesApp

class TerminalGamesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal Games")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(520, 420)
        central = QWidget()
        v = QVBoxLayout(central)
        row = QHBoxLayout()
        self.btn_guess = QPushButton("Guess Number")
        self.btn_hang = QPushButton("Hangman")
        row.addWidget(self.btn_guess); row.addWidget(self.btn_hang)
        v.addLayout(row)
        self.console = QTextEdit()
        self.console.setReadOnly(False)
        v.addWidget(self.console, 1)
        self.setCentralWidget(central)

        self.btn_guess.clicked.connect(self.start_guess)
        self.btn_hang.clicked.connect(self.start_hang)
        self._game = None

    # Guess number
    def start_guess(self):
        self._target = random.randint(1, 100)
        self.console.clear(); self.console.append("Guess Number (1-100). Type a guess and press Enter.")
        self.console.returnPressed = False
        self.console.keyPressEvent = self._guess_keypress

    def _guess_keypress(self, ev):
        if ev.key() == Qt.Key.Key_Return or ev.key() == Qt.Key.Key_Enter:
            text = self.console.toPlainText().splitlines()[-1].strip()
            try:
                n = int(text)
            except:
                self.console.append("Enter a number.")
                return
            if n < self._target: self.console.append("Too low.")
            elif n > self._target: self.console.append("Too high.")
            else:
                self.console.append("Correct! 🎉")
        else:
            QTextEdit.keyPressEvent(self.console, ev)

    # Hangman (very small)
    def start_hang(self):
        words = ["python","luxxer","desktop","widget","window","keyboard","mouse"]
        self._word = random.choice(words)
        self._masked = ["_" for _ in self._word]
        self._tries = 6
        self.console.clear()
        self.console.append(f"Hangman. Guess letters. Word: {' '.join(self._masked)}. Tries left: {self._tries}")
        self.console.keyPressEvent = self._hang_keypress

    def _hang_keypress(self, ev):
        if ev.key() == Qt.Key.Key_Return or ev.key() == Qt.Key.Key_Enter:
            text = self.console.toPlainText().splitlines()[-1].strip()
            if not text: return
            ch = text[-1].lower()
            if ch in self._word:
                for i,c in enumerate(self._word):
                    if c == ch:
                        self._masked[i] = ch
                self.console.append(f"Good: {' '.join(self._masked)}")
                if "_" not in self._masked:
                    self.console.append("You won!")
            else:
                self._tries -= 1
                self.console.append(f"Wrong. Tries left: {self._tries}")
                if self._tries <= 0:
                    self.console.append(f"You lost. Word was: {self._word}")
        else:
            QTextEdit.keyPressEvent(self.console, ev)

class AmbientSoundApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ambient Sounds")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(420, 300)
        central = QWidget()
        v = QVBoxLayout(central)
        self.listw = QListWidget()
        self.btn_add = QPushButton("Add sound files")
        self.btn_play = QPushButton("Play/Stop")
        v.addWidget(self.listw); v.addWidget(self.btn_add); v.addWidget(self.btn_play)
        self.setCentralWidget(central)

        self.btn_add.clicked.connect(self.add_files)
        self.btn_play.clicked.connect(self.toggle_play)

        self.player = None
        self.audio_out = None
        self.current_files = []

        if not MULTIMEDIA_AVAILABLE:
            QMessageBox.information(self, "Multimedia missing", "PyQt6.QtMultimedia not available — playback disabled.")
            self.btn_play.setEnabled(False)

    def add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Add sounds", "", "Audio (*.mp3 *.wav *.ogg)")
        for p in paths:
            self.current_files.append(p)
            self.listw.addItem(p)

    def toggle_play(self):
        if not MULTIMEDIA_AVAILABLE: return
        if self.player and self.player.playbackState():
            try:
                self.player.stop()
            except Exception:
                pass
            self.player = None
            QMessageBox.information(self, "Stopped", "Playback stopped.")
            return
        if not self.current_files:
            QMessageBox.information(self, "No files", "Add audio files first")
            return
        # play the first file in loop
        from PyQt6.QtCore import QUrl
        self.audio_out = QAudioOutput()
        player = QMediaPlayer()
        player.setAudioOutput(self.audio_out)
        player.setSource(QUrl.fromLocalFile(self.current_files[0]))
        player.setLoops(-1)  # infinite loop
        player.play()
        self.player = player
        QMessageBox.information(self, "Playing", f"Playing {self.current_files[0]} (looping)")

# ScreenOrganizerApp

class ScreenOrganizerApp(QMainWindow):
    def __init__(self, main_ref=None):
        super().__init__()
        self.setWindowTitle("Screen Organizer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(360, 220)
        central = QWidget()
        v = QVBoxLayout(central)
        self.btn_tile_h = QPushButton("Tile horizontally")
        self.btn_tile_v = QPushButton("Tile vertically")
        self.btn_cascade = QPushButton("Cascade")
        v.addWidget(self.btn_tile_h); v.addWidget(self.btn_tile_v); v.addWidget(self.btn_cascade)
        self.setCentralWidget(central)
        self.main_ref = main_ref
        self.btn_tile_h.clicked.connect(self.tile_h)
        self.btn_tile_v.clicked.connect(self.tile_v)
        self.btn_cascade.clicked.connect(self.cascade)

    def _subwindows(self):
        if not self.main_ref: return []
        mdi = getattr(self.main_ref, "mdi", None)
        if mdi is None: return []
        return [s for s in mdi.subWindowList() if s.isVisible()]

    def tile_h(self):
        subs = self._subwindows()
        if not subs: return
        w = self.main_ref.mdi.width() // len(subs)
        h = self.main_ref.mdi.height()
        x = 0
        for s in subs:
            s.setGeometry(x, 0, w, h)
            x += w

    def tile_v(self):
        subs = self._subwindows()
        if not subs: return
        w = self.main_ref.mdi.width()
        h = self.main_ref.mdi.height() // len(subs)
        y = 0
        for s in subs:
            s.setGeometry(0, y, w, h)
            y += h

    def cascade(self):
        subs = self._subwindows()
        if not subs: return
        x = y = 0
        for s in subs:
            s.setGeometry(x, y, int(self.main_ref.mdi.width()*0.6), int(self.main_ref.mdi.height()*0.6))
            x += 30; y += 30

class ThemePreviewApp(QMainWindow):
    FILE = DATA_DIR / "theme_preview.qss"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Preview")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(720, 520)
        central = QWidget()
        v = QVBoxLayout(central)
        row = QHBoxLayout()
        self.btn_load = QPushButton("Load")
        self.btn_save = QPushButton("Save")
        self.btn_apply = QPushButton("Apply to app")
        row.addWidget(self.btn_load); row.addWidget(self.btn_save); row.addWidget(self.btn_apply)
        v.addLayout(row)
        self.editor = QTextEdit()
        v.addWidget(self.editor, 1)
        self.setCentralWidget(central)
        self.btn_load.clicked.connect(self.load)
        self.btn_save.clicked.connect(self.save)
        self.btn_apply.clicked.connect(self.apply_theme)
        self.load()

    def load(self):
        try:
            if Path(self.FILE).exists():
                self.editor.setPlainText(Path(self.FILE).read_text(encoding="utf-8"))
            else:
                # default small template
                self.editor.setPlainText("QMainWindow { background-color: #121212; color: #fff; }\nQPushButton { padding: 6px; }")
        except Exception:
            pass

    def save(self):
        try:
            Path(self.FILE).write_text(self.editor.toPlainText(), encoding="utf-8")
            QMessageBox.information(self, "Saved", f"Saved to {self.FILE}")
        except Exception as e:
            QMessageBox.warning(self, "Save failed", str(e))

    def apply_theme(self):
        qapp = QApplication.instance()
        if qapp:
            qapp.setStyleSheet(self.editor.toPlainText())
            QMessageBox.information(self, "Applied", "Stylesheet applied to application.")