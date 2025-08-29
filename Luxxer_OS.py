import sys
import os
import re
import json
import csv
import math
import time
import shutil
import random
import string
import hashlib
import tempfile
import datetime
import traceback
import webbrowser
import platform
import subprocess
import itertools
import threading
import warnings
import secrets
import base64
import binascii
import zlib
from dataclasses import dataclass
from functools import partial
from typing import Any, Dict, Optional

# System info
import psutil

# PyQt6 Core/GUI
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QRegularExpression,
    QPropertyAnimation, QRect, QEasingCurve
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QPainter, QPen, QColor,
    QAction, QTextCharFormat, QFont, QSyntaxHighlighter, QCursor
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QLineEdit, QTreeWidget, QTreeWidgetItem,
    QColorDialog, QInputDialog, QProgressBar, QSplitter, QFrame, QMenu,
    QComboBox, QGridLayout, QDockWidget, QSpinBox, QCheckBox,
    QMdiArea, QMdiSubWindow, QScrollArea, QSizePolicy, QMenuBar, QTableWidget, QTableWidgetItem
)

# PyQt6 Multimedia / PDF
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPdf import QPdfDocument

# Third-party
import pyautogui
from moviepy.editor import VideoFileClip

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# CUSTOM MODULES
from start_menu_file import StartMenu
from Luxxer_OS_Start import StartScreen, apply_theme_global
from games_all import GamesApp
from applicationadder import ApplicationAdder
from RandomChallenge import RandomChallengeApp
from MotivationAIChat import MotivationAIChat
from JokeGenerator import JokeGeneratorApp

# Extra Apps
from apps_extra import HackerSimulatorApp, ASCIIPainterApp, FortuneTellerApp
from apps_extra2 import (
    HabitTrackerApp, PomodoroApp, RandomStoryApp, TravelTipsApp,
    QRCodeGeneratorApp, ColorPaletteApp, RecipeBoxApp, BudgetTrackerApp,
    TerminalGamesApp, AmbientSoundApp, ScreenOrganizerApp, ThemePreviewApp
)
import isAllFilesHere
if not isAllFilesHere.run_check():
    sys.exit(1)

# Safe VFS functions
def vfs_listdir_safe(path: str):
    try:
        parts = [p for p in path.strip('/').split('/') if p]
        node = APP_STATE.get('files', {})
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return []
        return list(node.keys()) if isinstance(node, dict) else []
    except Exception as e:
        print("VFS ListDir Error:", e)
        return []

def vfs_read_safe(path: str):
    try:
        parts = [p for p in path.strip('/').split('/') if p]
        node = APP_STATE.get('files', {})
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return None
        return node if isinstance(node, str) else None
    except Exception as e:
        print("VFS Read Error:", e)
        return None

def vfs_write_safe(path: str, content: str):
    try:
        parts = [p for p in path.strip('/').split('/') if p]
        node = APP_STATE.setdefault('files', {})
        for p in parts[:-1]:
            if p not in node or not isinstance(node[p], dict):
                node[p] = {}
            node = node[p]
        node[parts[-1]] = content
        return True
    except Exception as e:
        print("VFS Write Error:", e)
        return False

def vfs_delete_safe(path: str):
    try:
        parts = [p for p in path.strip('/').split('/') if p]
        node = APP_STATE.get('files', {})
        for p in parts[:-1]:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return False
        if isinstance(node, dict) and parts[-1] in node:
            del node[parts[-1]]
            return True
        return False
    except Exception as e:
        print("VFS Delete Error:", e)
        return False

# Worker threads for long ops

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(object)
    status = pyqtSignal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.fn(self.progress, self.status, *self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(e)

# App List
APPS_LIST = [
    'Notebook','Paint','Explorer','LuxxerWeb','Settings','WinRAR','Zer3 IDE','Calculator',
    'Cyber Tools','GuardianAV','CMD','RandomChallenge', 'MotivationAIChat', 'JokeGenerator',
    'TaskManager','FilePreview','Calendar', 'HackerSimulator', 'ASCIIPainter', 'FortuneTeller',
    'Mail','Contacts','Photos','MusicPlayer','VideoPlayer','PDFReader','OfficeWriter',
    'Spreadsheet','Presentation','StickyNotes','Screenshot','ScreenRecorder',
    'ImageEditorPro','VideoEditor','MediaConverter','TerminalEmulator','ShellX','GitClient',
    'DockerManager','PackageManager','AppStore','BackupRestore','DiskCleaner','DiskManager',
    'SystemInfo','DeviceManager','PrinterManager','NetworkMonitor','VPNClient','RemoteDesktop',
    'SSHClient','PortScanner','WiFiAnalyzer','ClipboardManager','Scheduler','VoiceRecorder',
    'GamesApp', 'ApplicationAdder', 'HabitTracker', 'Pomodoro', 'RandomStory', 'TravelTips',
    'QRCodeGenerator', 'ColorPalette', 'RecipeBox', 'BudgetTracker',
    'TerminalGames', 'AmbientSound', 'ScreenOrganizer', 'ThemePreview',
]

# Small utilities and dialogs

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MusicPlayer - Luxxer")
        self.resize(500, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Playlist
        self.playlist = QListWidget()
        self.layout.addWidget(self.playlist)

        # Buttons
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Track")
        self.load_btn.clicked.connect(self.load_track)
        btn_layout.addWidget(self.load_btn)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play)
        btn_layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause)
        btn_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)
        btn_layout.addWidget(self.stop_btn)

        self.layout.addLayout(btn_layout)

        # Status
        self.status = QLabel("No track loaded")
        self.layout.addWidget(self.status)

        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.current_track = None

        # Sample data
        self.tracks = []

    def load_track(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open audio", "", "Audio (*.mp3 *.wav *.ogg);;All Files (*)")
        if path:
            self.tracks.append(path)
            self.playlist.addItem(os.path.basename(path))
            self.status.setText(f"Loaded: {os.path.basename(path)}")

    def play(self):
        selected = self.playlist.currentRow()
        if selected >= 0:
            track = self.tracks[selected]
            if self.current_track != track:
                self.player.setSource(track)
                self.current_track = track
            self.player.play()
            self.status.setText(f"Playing: {os.path.basename(track)}")
        else:
            QMessageBox.warning(self, "No selection", "Select a track first.")

    def pause(self):
        self.player.pause()
        self.status.setText("Paused")

    def stop(self):
        self.player.stop()
        self.status.setText("Stopped")

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoPlayer - Luxxer")
        self.resize(800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Video widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open Video")
        self.open_btn.clicked.connect(self.open_video)
        btn_layout.addWidget(self.open_btn)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play)
        btn_layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause)
        btn_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)
        btn_layout.addWidget(self.stop_btn)

        self.layout.addLayout(btn_layout)

        # Status
        self.status = QLabel("No video loaded")
        self.layout.addWidget(self.status)

        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.current_video = None

    def open_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Video (*.mp4 *.mkv *.avi);;All Files (*)")
        if path:
            self.current_video = path
            self.player.setSource(path)
            self.status.setText(f"Loaded: {os.path.basename(path)}")

    def play(self):
        if self.current_video:
            self.player.play()
            self.status.setText(f"Playing: {os.path.basename(self.current_video)}")

    def pause(self):
        self.player.pause()
        self.status.setText("Paused")

    def stop(self):
        self.player.stop()
        self.status.setText("Stopped")

class PDFReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFReader - Luxxer")
        self.resize(700, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # PDF document and viewer
        self.pdf_doc = QPdfDocument()
        self.pdf_view = QPdfView()
        self.pdf_view.setDocument(self.pdf_doc)
        self.layout.addWidget(self.pdf_view)

        # Buttons
        self.open_btn = QPushButton("Open PDF")
        self.open_btn.clicked.connect(self.open_pdf)
        self.layout.addWidget(self.open_btn)

        self.status = QLabel("No PDF loaded")
        self.layout.addWidget(self.status)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if path:
            if self.pdf_doc.load(path) == QPdfDocument.Status.Ready:
                self.status.setText(f"Loaded: {os.path.basename(path)}")
            else:
                QMessageBox.warning(self, "Error", "Failed to load PDF.")

class OfficeWriterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OfficeWriter - Luxxer")
        self.resize(600, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.editor = QTextEdit()
        self.layout.addWidget(self.editor)

        btn_layout = QVBoxLayout()
        self.save_btn = QPushButton("Save Document")
        self.save_btn.clicked.connect(self.save_doc)
        btn_layout.addWidget(self.save_btn)

        self.open_btn = QPushButton("Open Document")
        self.open_btn.clicked.connect(self.open_doc)
        btn_layout.addWidget(self.open_btn)

        self.layout.addLayout(btn_layout)

        self.status = QLabel("Ready")
        self.layout.addWidget(self.status)

    def save_doc(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save document", "", "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.status.setText(f"Saved: {os.path.basename(path)}")

    def open_doc(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open document", "", "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setText(f.read())
            self.status.setText(f"Opened: {os.path.basename(path)}")

class SpreadsheetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spreadsheet - Luxxer")
        self.resize(800, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.table = QTableWidget(10, 5)  # default 10x5
        self.layout.addWidget(self.table)

        btn_layout = QVBoxLayout()
        self.load_btn = QPushButton("Load CSV")
        self.load_btn.clicked.connect(self.load_csv)
        btn_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("Save CSV")
        self.save_btn.clicked.connect(self.save_csv)
        btn_layout.addWidget(self.save_btn)

        self.layout.addLayout(btn_layout)

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv);;All Files (*)")
        if path:
            with open(path, newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)
            self.table.setRowCount(len(data))
            self.table.setColumnCount(max(len(r) for r in data))
            for r, row in enumerate(data):
                for c, val in enumerate(row):
                    self.table.setItem(r, c, QTableWidgetItem(val))

    def save_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)")
        if path:
            with open(path, 'w', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                for r in range(self.table.rowCount()):
                    row = [self.table.item(r, c).text() if self.table.item(r, c) else '' for c in range(self.table.columnCount())]
                    writer.writerow(row)

class PresentationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Presentation - Luxxer")
        self.resize(800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.slide_label = QLabel("No slides loaded")
        self.slide_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.slide_label)

        self.load_btn = QPushButton("Load Slides")
        self.load_btn.clicked.connect(self.load_slides)
        self.layout.addWidget(self.load_btn)

        self.current_slide = 0
        self.slides = []

        self.next_btn = QPushButton("Next Slide")
        self.next_btn.clicked.connect(self.next_slide)
        self.layout.addWidget(self.next_btn)

        self.prev_btn = QPushButton("Previous Slide")
        self.prev_btn.clicked.connect(self.prev_slide)
        self.layout.addWidget(self.prev_btn)

    def load_slides(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open slides", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if paths:
            self.slides = paths
            self.current_slide = 0
            self.show_slide()

    def show_slide(self):
        if self.slides:
            pix = QPixmap(self.slides[self.current_slide])
            self.slide_label.setPixmap(pix.scaled(self.slide_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def next_slide(self):
        if self.slides:
            self.current_slide = (self.current_slide + 1) % len(self.slides)
            self.show_slide()

    def prev_slide(self):
        if self.slides:
            self.current_slide = (self.current_slide - 1) % len(self.slides)
            self.show_slide()

class StickyNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sticky Notes - Luxxer")
        self.resize(400, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.note = QTextEdit()
        self.layout.addWidget(self.note)

        self.save_btn = QPushButton("Save note")
        self.save_btn.clicked.connect(self.save_note)
        self.layout.addWidget(self.save_btn)

        # Auto-load previous note
        self.path = os.path.join(tempfile.gettempdir(), "luxxer_sticky.txt")
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.note.setText(f.read())

    def save_note(self):
        txt = self.note.toPlainText()
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(txt)
        QMessageBox.information(self, "Saved", f"Saved to {self.path}")

class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot - Luxxer")
        self.resize(300, 200)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.layout.addWidget(QLabel("Takes full screen screenshot and saves to temp folder."))

        self.take_btn = QPushButton("Take screenshot")
        self.take_btn.clicked.connect(self.take)
        self.layout.addWidget(self.take_btn)

    def take(self):
        try:
            screen = QApplication.primaryScreen()
            if not screen:
                QMessageBox.warning(self, "Error", "No screen available")
                return
            img = screen.grabWindow(0)
            path = os.path.join(tempfile.gettempdir(), f"luxxer_screenshot_{int(datetime.datetime.now().timestamp())}.png")
            img.save(path)
            QMessageBox.information(self, "Saved", f"Screenshot saved: {path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed: {e}")

class ScreenRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreenRecorder - Luxxer")
        self.resize(300, 200)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.recording = False
        self.frames = []

        self.layout.addWidget(QLabel("Screen recording simple demo (saves PNG frames)."))

        self.btn = QPushButton("Start recording")
        self.btn.clicked.connect(self.toggle)
        self.layout.addWidget(self.btn)

    def toggle(self):
        self.recording = not self.recording
        self.btn.setText("Stop recording" if self.recording else "Start recording")
        if self.recording:
            threading.Thread(target=self.record_screen, daemon=True).start()
        else:
            self.save_frames()

    def record_screen(self):
        while self.recording:
            img = pyautogui.screenshot()
            self.frames.append(img)

    def save_frames(self):
        folder = os.path.join(tempfile.gettempdir(), f"luxxer_rec_{int(datetime.datetime.now().timestamp())}")
        os.makedirs(folder, exist_ok=True)
        for i, frame in enumerate(self.frames):
            frame.save(os.path.join(folder, f"frame_{i}.png"))
        self.frames = []
        QMessageBox.information(self, "Saved", f"Frames saved to {folder}")

class VideoEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoEditor - Luxxer")
        self.resize(600, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.label = QLabel("Video editor - load and trim (basic)")
        self.layout.addWidget(self.label)

        self.load_btn = QPushButton("Load Video")
        self.load_btn.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_btn)

        self.trim_btn = QPushButton("Trim first 5 seconds")
        self.trim_btn.clicked.connect(self.trim_video)
        self.layout.addWidget(self.trim_btn)

        self.clip = None
        self.video_path = ""

    def load_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Videos (*.mp4 *.mkv)")
        if path:
            self.video_path = path
            self.clip = VideoFileClip(path)
            self.label.setText(f"Loaded: {os.path.basename(path)}")

    def trim_video(self):
        if self.clip:
            trimmed = self.clip.subclip(0, min(5, self.clip.duration))
            save_path = os.path.join(os.path.dirname(self.video_path), f"trimmed_{os.path.basename(self.video_path)}")
            trimmed.write_videofile(save_path)
            QMessageBox.information(self, "Saved", f"Trimmed video saved: {save_path}")
        else:
            QMessageBox.warning(self, "Error", "Load a video first")

class ImageEditorProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageEditorPro - Luxxer")
        self.resize(600, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.img_label = QLabel("No image loaded")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.img_label)

        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("Save Image As")
        self.save_btn.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_btn)

        self.current_image = None

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.current_image = QPixmap(path)
            self.img_label.setPixmap(self.current_image.scaled(self.img_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def save_image(self):
        if self.current_image:
            path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPG (*.jpg)")
            if path:
                self.current_image.save(path)
                QMessageBox.information(self, "Saved", f"Image saved to {path}")

class MediaConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediaConverter - Luxxer")
        self.resize(400, 250)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Media converter: select a file and choose output format.")
        self.layout.addWidget(self.info_label)

        self.load_btn = QPushButton("Load Media")
        self.load_btn.clicked.connect(self.load_media)
        self.layout.addWidget(self.load_btn)

        self.convert_btn = QPushButton("Convert (demo)")
        self.convert_btn.clicked.connect(self.convert_media)
        self.layout.addWidget(self.convert_btn)

        self.media_path = None

    def load_media(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Media File", "",
                                              "All Media Files (*.mp4 *.mp3 *.wav *.avi *.mkv)")
        if path:
            self.media_path = path
            self.info_label.setText(f"Loaded: {os.path.basename(path)}")

    def convert_media(self):
        if self.media_path:
            # Placeholder: conversion not implemented yet
            QMessageBox.information(self, "Convert", f"Conversion would run on {os.path.basename(self.media_path)} (demo)")
        else:
            QMessageBox.warning(self, "Error", "No media loaded")

class TerminalEmulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TerminalEmulator - Luxxer")
        self.resize(600, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command (safe commands only)")
        self.layout.addWidget(self.cmd_input)

        self.run_btn = QPushButton("Run Command")
        self.run_btn.clicked.connect(self.run_command)
        self.layout.addWidget(self.run_btn)

        # Example of allowed commands
        self.whitelist = ["echo", "dir", "ls", "ping"]

    def run_command(self):
        cmd_text = self.cmd_input.text().strip()
        if not cmd_text:
            return
        cmd_name = cmd_text.split()[0]
        if cmd_name not in self.whitelist:
            QMessageBox.warning(self, "Blocked", "Command not allowed")
            return
        try:
            result = subprocess.run(cmd_text, shell=True, capture_output=True, text=True)
            self.output.append(f"> {cmd_text}\n{result.stdout}\n{result.stderr}")
        except Exception as e:
            self.output.append(f"Error: {e}")

class ShellXApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShellX - Luxxer")
        self.resize(600, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Safe shell wrapper: only whitelisted commands allowed.")
        self.layout.addWidget(self.info_label)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command")
        self.layout.addWidget(self.cmd_input)

        self.run_btn = QPushButton("Execute")
        self.run_btn.clicked.connect(self.run_command)
        self.layout.addWidget(self.run_btn)

        self.whitelist = ["echo", "dir", "ls", "ping", "whoami"]

    def run_command(self):
        cmd_text = self.cmd_input.text().strip()
        if not cmd_text:
            return
        cmd_name = cmd_text.split()[0]
        if cmd_name not in self.whitelist:
            QMessageBox.warning(self, "Blocked", "Command not allowed")
            return
        try:
            result = subprocess.run(cmd_text, shell=True, capture_output=True, text=True)
            self.output.append(f"> {cmd_text}\n{result.stdout}\n{result.stderr}")
        except Exception as e:
            self.output.append(f"Error: {e}")

class GitClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitClient - Luxxer")
        self.resize(500, 200)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.repo_path = QLineEdit()
        self.repo_path.setPlaceholderText("Enter repository path")
        self.layout.addWidget(QLabel("Repository Path:"))
        self.layout.addWidget(self.repo_path)

        self.status_btn = QPushButton("Status")
        self.status_btn.clicked.connect(self.status)
        self.layout.addWidget(self.status_btn)

        self.commit_btn = QPushButton("Commit (demo)")
        self.commit_btn.clicked.connect(self.commit_demo)
        self.layout.addWidget(self.commit_btn)

    def status(self):
        path = self.repo_path.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Invalid repository path")
            return
        try:
            result = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
            QMessageBox.information(self, "Status", result.stdout)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Git error: {e}")

    def commit_demo(self):
        QMessageBox.information(self, "Commit", "Commit action (demo, no actual commit)")

class DockerManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DockerManager - Luxxer")
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("DockerManager: list local containers and images (demo).")
        self.layout.addWidget(self.info_label)

        self.container_list = QListWidget()
        self.layout.addWidget(self.container_list)

        self.load_btn = QPushButton("Load Containers (demo)")
        self.load_btn.clicked.connect(self.load_containers)
        self.layout.addWidget(self.load_btn)

        self.start_btn = QPushButton("Start Selected (demo)")
        self.start_btn.clicked.connect(self.start_container)
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Selected (demo)")
        self.stop_btn.clicked.connect(self.stop_container)
        self.layout.addWidget(self.stop_btn)

    def load_containers(self):
        self.container_list.clear()
        # Demo container names
        demo_containers = ["web_server", "db_server", "cache"]
        self.container_list.addItems(demo_containers)
        QMessageBox.information(self, "Loaded", "Demo containers loaded")

    def start_container(self):
        selected = self.container_list.currentItem()
        if selected:
            QMessageBox.information(self, "Start", f"Started container: {selected.text()} (demo)")

    def stop_container(self):
        selected = self.container_list.currentItem()
        if selected:
            QMessageBox.information(self, "Stop", f"Stopped container: {selected.text()} (demo)")

class PackageManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PackageManager - Luxxer")
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Local Package Manager: install/update packages (demo).")
        self.layout.addWidget(self.info_label)

        self.pkg_list = QListWidget()
        self.pkg_list.addItems(["luxxer-core", "media-tools", "network-utils"])
        self.layout.addWidget(self.pkg_list)

        self.install_btn = QPushButton("Install (demo)")
        self.install_btn.clicked.connect(self.install_pkg)
        self.layout.addWidget(self.install_btn)

        self.update_btn = QPushButton("Update (demo)")
        self.update_btn.clicked.connect(self.update_pkg)
        self.layout.addWidget(self.update_btn)

    def install_pkg(self):
        selected = self.pkg_list.currentItem()
        if selected:
            QMessageBox.information(self, "Install", f"Installed {selected.text()} (demo)")

    def update_pkg(self):
        selected = self.pkg_list.currentItem()
        if selected:
            QMessageBox.information(self, "Update", f"Updated {selected.text()} (demo)")

class AppStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppStore - Luxxer")
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("App Store: browse and install apps (local demo).")
        self.layout.addWidget(self.info_label)

        self.app_list = QListWidget()
        self.app_list.addItems(["Mail", "Photos", "MusicPlayer", "VideoPlayer"])
        self.layout.addWidget(self.app_list)

        self.install_btn = QPushButton("Install App")
        self.install_btn.clicked.connect(self.install_app)
        self.layout.addWidget(self.install_btn)

    def install_app(self):
        selected = self.app_list.currentItem()
        if selected:
            QMessageBox.information(self, "Install", f"Installed {selected.text()} (demo)")

class BackupRestoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BackupRestore - Luxxer")
        self.resize(500, 250)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Backup and restore local files (demo).")
        self.layout.addWidget(self.info_label)

        self.backup_btn = QPushButton("Create Backup")
        self.backup_btn.clicked.connect(self.create_backup)
        self.layout.addWidget(self.backup_btn)

        self.restore_btn = QPushButton("Restore Backup")
        self.restore_btn.clicked.connect(self.restore_backup)
        self.layout.addWidget(self.restore_btn)

    def create_backup(self):
        path = os.path.join(tempfile.gettempdir(), f"luxxer_backup_{int(datetime.datetime.now().timestamp())}.tar")
        QMessageBox.information(self, "Backup", f"Created demo backup at {path}")

    def restore_backup(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select backup to restore", tempfile.gettempdir(), "Backup Files (*.tar)")
        if path:
            QMessageBox.information(self, "Restore", f"Restored demo backup from {path}")

class DiskCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiskCleaner - Luxxer")
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Safe Disk Cleaner: Shows temp files and suggests cleanup.")
        self.layout.addWidget(self.info_label)

        self.temp_list = QListWidget()
        self.layout.addWidget(self.temp_list)

        self.scan_btn = QPushButton("Scan Temp Files")
        self.scan_btn.clicked.connect(self.scan_temp)
        self.layout.addWidget(self.scan_btn)

        self.clean_btn = QPushButton("Clean Selected")
        self.clean_btn.clicked.connect(self.clean_temp)
        self.layout.addWidget(self.clean_btn)

    def scan_temp(self):
        self.temp_list.clear()
        temp_dir = tempfile.gettempdir()
        files = os.listdir(temp_dir)
        for f in files:
            self.temp_list.addItem(f)
        QMessageBox.information(self, "Scan Complete", f"Found {len(files)} temp files (demo).")

    def clean_temp(self):
        selected = self.temp_list.currentItem()
        if selected:
            QMessageBox.information(self, "Clean", f"Deleted {selected.text()} (demo, safe).")

class DiskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiskManager - Luxxer")
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Disk Partitions and Usage (read-only demo).")
        self.layout.addWidget(self.info_label)

        self.disk_list = QListWidget()
        self.layout.addWidget(self.disk_list)

        self.refresh_btn = QPushButton("Refresh Partitions")
        self.refresh_btn.clicked.connect(self.refresh_disks)
        self.layout.addWidget(self.refresh_btn)

        self.refresh_disks()

    def refresh_disks(self):
        self.disk_list.clear()
        try:
            partitions = [p for p in os.listdir('/') if os.path.isdir(p)]
            for p in partitions:
                self.disk_list.addItem(p)
            QMessageBox.information(self, "Refreshed", f"{len(partitions)} partitions listed (demo).")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not list partitions: {e}")

class SystemInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SystemInfo - Luxxer")
        self.resize(400, 250)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)

        info = []
        try:
            info.append(f"Platform: {platform.platform()}")
            info.append(f"Processor: {platform.processor()}")
            info.append(f"Python Version: {platform.python_version()}")
            import psutil
            info.append(f"CPU Cores: {psutil.cpu_count(logical=True)}")
            info.append(f"RAM: {round(psutil.virtual_memory().total / (1024*1024))} MB")
        except Exception:
            info.append("System info not available")

        for line in info:
            l.addWidget(QLabel(line))

        self.setCentralWidget(w)

class DeviceManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeviceManager - Luxxer")
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Attached Devices List (read-only demo)"))

        self.dev_list = QListWidget()
        l.addWidget(self.dev_list)

        self.refresh_btn = QPushButton("Refresh Devices")
        self.refresh_btn.clicked.connect(self.refresh_devices)
        l.addWidget(self.refresh_btn)

        self.refresh_devices()

    def refresh_devices(self):
        self.dev_list.clear()
        try:
            disks = psutil.disk_partitions()
            for d in disks:
                self.dev_list.addItem(f"{d.device} -> {d.mountpoint} ({d.fstype})")
            QMessageBox.information(self, "Refreshed", f"{len(disks)} devices listed (demo).")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not list devices: {e}")

class PrinterManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrinterManager - Luxxer")
        self.resize(450, 300)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.layout.addWidget(QLabel("Printer queue manager (demo, read-only)."))

        self.queue_list = QListWidget()
        self.layout.addWidget(self.queue_list)

        self.refresh_btn = QPushButton("Refresh Queue")
        self.refresh_btn.clicked.connect(self.refresh_queue)
        self.layout.addWidget(self.refresh_btn)

        self.print_btn = QPushButton("Print Selected")
        self.print_btn.clicked.connect(self.print_selected)
        self.layout.addWidget(self.print_btn)

        self.refresh_queue()

    def refresh_queue(self):
        self.queue_list.clear()
        jobs = ["Doc1.pdf", "Photo.png", "Report.docx"]  # demo jobs
        for job in jobs:
            self.queue_list.addItem(job)
        QMessageBox.information(self, "Queue Refreshed", f"{len(jobs)} jobs loaded (demo)")

    def print_selected(self):
        selected = self.queue_list.currentItem()
        if selected:
            QMessageBox.information(self, "Printing", f"Printed {selected.text()} (demo)")

class NetworkMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetworkMonitor - Luxxer")
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Network Monitor (demo, shows active interfaces)."))

        self.if_list = QListWidget()
        l.addWidget(self.if_list)

        self.refresh_btn = QPushButton("Refresh Interfaces")
        self.refresh_btn.clicked.connect(self.refresh_interfaces)
        l.addWidget(self.refresh_btn)

        self.refresh_interfaces()

    def refresh_interfaces(self):
        self.if_list.clear()
        try:
            interfaces = psutil.net_if_addrs()
            for iface in interfaces:
                self.if_list.addItem(iface)
            QMessageBox.information(self, "Refreshed", f"{len(interfaces)} interfaces listed (demo)")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot fetch interfaces: {e}")

class VPNClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPNClient - Luxxer")
        self.resize(400, 250)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("VPN Client (demo, safe UI only)"))

        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Enter VPN server address")
        l.addWidget(self.server_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_vpn)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_vpn)
        l.addWidget(self.disconnect_btn)

        self.status_label = QLabel("Status: Disconnected")
        l.addWidget(self.status_label)

    def connect_vpn(self):
        server = self.server_input.text().strip()
        if server:
            self.status_label.setText(f"Status: Connected to {server} (demo)")
            QMessageBox.information(self, "VPN", f"Connected to {server} (demo)")
        else:
            QMessageBox.warning(self, "VPN", "Enter server address first")

    def disconnect_vpn(self):
        self.status_label.setText("Status: Disconnected")
        QMessageBox.information(self, "VPN", "Disconnected (demo)")

class RemoteDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RemoteDesktop - Luxxer")
        self.resize(500, 300)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Remote desktop client (demo UI, safe)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter host IP")
        l.addWidget(self.host_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_host)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_host)
        l.addWidget(self.disconnect_btn)

        self.status_label = QLabel("Status: Disconnected")
        l.addWidget(self.status_label)

    def connect_host(self):
        host = self.host_input.text().strip()
        if host:
            self.status_label.setText(f"Connected to {host} (demo)")
            QMessageBox.information(self, "RemoteDesktop", f"Connected to {host} (demo)")
        else:
            QMessageBox.warning(self, "RemoteDesktop", "Enter host IP first")

    def disconnect_host(self):
        self.status_label.setText("Status: Disconnected")
        QMessageBox.information(self, "RemoteDesktop", "Disconnected (demo)")

class SSHClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSHClient - Luxxer")
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("SSH client (demo, safe terminal wrapper)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host IP")
        l.addWidget(self.host_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        l.addWidget(self.user_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_ssh)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_ssh)
        l.addWidget(self.disconnect_btn)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        l.addWidget(self.output_area)

    def connect_ssh(self):
        host = self.host_input.text().strip()
        user = self.user_input.text().strip()
        if host and user:
            self.output_area.append(f"Connected to {host} as {user} (demo)")
            QMessageBox.information(self, "SSHClient", f"Connected to {host} as {user} (demo)")
        else:
            QMessageBox.warning(self, "SSHClient", "Enter host and username")

    def disconnect_ssh(self):
        self.output_area.append("Disconnected (demo)")
        QMessageBox.information(self, "SSHClient", "Disconnected (demo)")

class PortScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PortScanner - Luxxer")
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Educational port scanner (local-only, demo)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter host IP (demo)")
        l.addWidget(self.host_input)

        self.scan_btn = QPushButton("Scan Ports")
        self.scan_btn.clicked.connect(self.scan_ports)
        l.addWidget(self.scan_btn)

        self.results_list = QListWidget()
        l.addWidget(self.results_list)

    def scan_ports(self):
        host = self.host_input.text().strip()
        if host:
            self.results_list.clear()
            # Demo data
            demo_ports = [22, 80, 443, 3306]
            for port in demo_ports:
                self.results_list.addItem(f"Port {port}: Open (demo)")
            QMessageBox.information(self, "PortScanner", f"Scan complete for {host} (demo)")
        else:
            QMessageBox.warning(self, "PortScanner", "Enter host IP first")

class WiFiAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFiAnalyzer - Luxxer (demo)")
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("WiFi analyzer (safe demo)"))

        self.scan_btn = QPushButton("Scan networks")
        self.scan_btn.clicked.connect(self.scan_networks)
        l.addWidget(self.scan_btn)

        self.network_list = QListWidget()
        l.addWidget(self.network_list)

    def scan_networks(self):
        self.network_list.clear()
        demo_networks = [
            ("HomeNetwork", -50),
            ("CoffeeShopWiFi", -70),
            ("PublicHotspot", -80),
            ("GuestNet", -60)
        ]
        for name, strength in demo_networks:
            self.network_list.addItem(f"{name} | Signal: {strength} dBm")
        QMessageBox.information(self, "WiFiAnalyzer", "Scan complete (demo)")

class ClipboardManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClipboardManager - Luxxer (demo)")
        self.resize(400, 300)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        self.clip_list = QListWidget()
        l.addWidget(self.clip_list)

        self.capture_btn = QPushButton("Capture clipboard")
        self.capture_btn.clicked.connect(self.capture_clipboard)
        l.addWidget(self.capture_btn)

        self.clear_btn = QPushButton("Clear list")
        self.clear_btn.clicked.connect(self.clear_list)
        l.addWidget(self.clear_btn)

    def capture_clipboard(self):
        cb = QApplication.clipboard()
        txt = cb.text()
        if txt:
            self.clip_list.addItem(txt[:200])
            QMessageBox.information(self, "ClipboardManager", "Clipboard captured (demo)")
        else:
            QMessageBox.warning(self, "ClipboardManager", "Clipboard empty")

    def clear_list(self):
        self.clip_list.clear()
        QMessageBox.information(self, "ClipboardManager", "List cleared")

class SchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduler - Luxxer (demo)")
        self.resize(400, 300)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        self.listw = QListWidget()
        l.addWidget(self.listw)

        self.add_btn = QPushButton("Add alarm (demo)")
        self.add_btn.clicked.connect(self.add_alarm)
        l.addWidget(self.add_btn)

    def add_alarm(self):
        # User-defined delay in seconds for demo
        secs, ok = QInputDialog.getInt(self, "Add Alarm", "Set alarm in seconds:", min=1, max=3600, value=10)
        if ok:
            ts = datetime.datetime.now() + datetime.timedelta(seconds=secs)
            self.listw.addItem(f"Alarm at {ts.strftime('%H:%M:%S')} (demo)")
            QTimer.singleShot(secs * 1000, lambda: QMessageBox.information(self, "Alarm", "Demo alarm fired"))

class VoiceRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceRecorder - Luxxer (demo)")
        self.resize(400, 250)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Voice recorder (demo, no actual audio capture)"))

        self.recording = False
        self.btn = QPushButton("Start recording")
        self.btn.clicked.connect(self.toggle)
        l.addWidget(self.btn)

        self.playback_btn = QPushButton("Playback last recording (demo)")
        self.playback_btn.clicked.connect(lambda: QMessageBox.information(self, "Playback", "Playback demo (no audio)"))
        l.addWidget(self.playback_btn)

    def toggle(self):
        self.recording = not self.recording
        self.btn.setText("Stop recording" if self.recording else "Start recording")
        QMessageBox.information(self, "VoiceRecorder", f"{'Started' if self.recording else 'Stopped'} (demo)")

class PasswordDialog(QInputDialog):
    def __init__(self, prompt="Enter password:"):
        super().__init__()
        self.setLabelText(prompt)
        self.setTextEchoMode(QLineEdit.EchoMode.Password)
        self.setOkButtonText('OK')
        self.setCancelButtonText('Cancel')

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        layout = QVBoxLayout()
        from PyQt6.QtWidgets import QCalendarWidget
        cal = QCalendarWidget()
        layout.addWidget(cal)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task Manager')
        layout = QVBoxLayout()
        self.listw = QListWidget()
        layout.addWidget(self.listw)
        btn_refresh = QPushButton('Refresh')
        btn_refresh.clicked.connect(self.refresh)
        layout.addWidget(btn_refresh)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.refresh()

    def refresh(self):
        self.listw.clear()
        import psutil
        for p in psutil.process_iter(['pid','name']):
            self.listw.addItem(f"{p.info['pid']}: {p.info['name']}")

class TerminalWidget(QWidget):
    command_entered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName('terminal')
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setObjectName('terminal')
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_enter)
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        self.setLayout(layout)
        self.write('Luxxer Terminal - type "help" for commands')

    def write(self, text: str):
        self.output.append(text)

    def on_enter(self):
        cmd = self.input.text().strip()
        if not cmd:
            return
        self.write(f'> {cmd}')
        self.input.clear()
        self.command_entered.emit(cmd)

# Paint application

class PaintCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('canvas')
        self.setMinimumSize(400, 300)
        self._pixmap = QPixmap(self.size())
        self._pixmap.fill(QColor('white'))
        self._last_pos = None
        self.pen_color = QColor('black')
        self.pen_width = 3

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0,0, self._pixmap)

    def resizeEvent(self, event):
        if self.width() > self._pixmap.width() or self.height() > self._pixmap.height():
            newpix = QPixmap(max(self.width(), self._pixmap.width()), max(self.height(), self._pixmap.height()))
            newpix.fill(QColor('white'))
            p = QPainter(newpix)
            p.drawPixmap(0,0,self._pixmap)
            p.end()
            self._pixmap = newpix
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._last_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self._last_pos is None:
            return
        p = QPainter(self._pixmap)
        pen = QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        p.drawLine(self._last_pos, event.position().toPoint())
        p.end()
        self._last_pos = event.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, event):
        self._last_pos = None

    def clear(self):
        self._pixmap.fill(QColor('white'))
        self.update()

    def save(self, path):
        self._pixmap.save(path)

class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Paint - Luxxer')
        self.canvas = PaintCanvas()
        central = QWidget()
        layout = QVBoxLayout()
        toolbar = QHBoxLayout()
        self.color_btn = QPushButton('Color')
        self.color_btn.clicked.connect(self.pick_color)
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.clicked.connect(self.canvas.clear)
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.save_image)
        toolbar.addWidget(self.color_btn)
        toolbar.addWidget(self.clear_btn)
        toolbar.addWidget(self.save_btn)
        layout.addLayout(toolbar)
        layout.addWidget(self.canvas)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def pick_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvas.pen_color = col

    def save_image(self):
        p = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG Files (*.png);;All Files (*)')
        if p and p[0]:
            self.canvas.save(p[0])
            QMessageBox.information(self, 'Saved', 'Image saved.')

class NotebookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Notebook - Luxxer')
        self.setMinimumSize(600, 400)

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.editor = QTextEdit()
        layout.addWidget(self.editor)

        hl = QHBoxLayout()
        self.save_btn = QPushButton('Save')
        self.load_btn = QPushButton('Load')
        self.delete_btn = QPushButton('Delete')

        hl.addWidget(self.save_btn)
        hl.addWidget(self.load_btn)
        hl.addWidget(self.delete_btn)
        layout.addLayout(hl)

        self.save_btn.clicked.connect(self.save)
        self.load_btn.clicked.connect(self.load)
        self.delete_btn.clicked.connect(self.delete)

        APP_STATE.setdefault('files', {})
        APP_STATE['files'].setdefault('Documents', {})

    def save(self):
        name, ok = QInputDialog.getText(self, 'Save note', 'File name:')
        if not ok or not name:
            return
        success = vfs_write_safe(f'Documents/{name}.txt', self.editor.toPlainText())
        if success:
            QMessageBox.information(self, 'Saved', f'Note "{name}" saved.')
        else:
            QMessageBox.warning(self, 'Error', f'Failed to save "{name}".')

    def load(self):
        files = vfs_listdir_safe('Documents')
        if not files:
            QMessageBox.information(self, 'Load', 'No documents found.')
            return
        item, ok = QInputDialog.getItem(self, 'Load note', 'Choose file:', files, 0, False)
        if ok and item:
            content = vfs_read_safe(f'Documents/{item}')
            if content is not None:
                self.editor.setPlainText(content)
            else:
                QMessageBox.warning(self, 'Error', f'Could not read "{item}".')

    def delete(self):
        files = vfs_listdir_safe('Documents')
        if not files:
            QMessageBox.information(self, 'Delete', 'No documents found.')
            return
        item, ok = QInputDialog.getItem(self, 'Delete note', 'Choose file to delete:', files, 0, False)
        if ok and item:
            confirm = QMessageBox.question(
                self, 'Delete',
                f'Are you sure you want to delete "{item}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                success = vfs_delete_safe(f'Documents/{item}')
                if success:
                    QMessageBox.information(self, 'Deleted', f'File "{item}" deleted.')
                    self.editor.clear()
                else:
                    QMessageBox.warning(self, 'Error', f'Could not delete "{item}".')

class ExplorerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Luxxer Explorer")
        self.setGeometry(200, 200, 800, 600)

        self.current_path = os.path.expanduser("~")
        self.locked_paths = {}  # {path: password}

        layout = QVBoxLayout()

        self.path_edit = QLineEdit(self.current_path)
        layout.addWidget(self.path_edit)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.open_item)
        btn_layout.addWidget(open_btn)

        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self.rename_item)
        btn_layout.addWidget(rename_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_item)
        btn_layout.addWidget(delete_btn)

        lock_btn = QPushButton("Lock")
        lock_btn.clicked.connect(self.lock_item)
        btn_layout.addWidget(lock_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.load_directory()

    def load_directory(self):
        self.list_widget.clear()
        try:
            for item in os.listdir(self.current_path):
                full_path = os.path.join(self.current_path, item)
                if full_path in self.locked_paths:
                    item_name = f"[LOCKED] {item}"
                else:
                    item_name = item
                self.list_widget.addItem(item_name)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_item(self):
        selected = self.list_widget.currentItem()
        if not selected:
            return
        name = selected.text().replace("[LOCKED] ", "")
        full_path = os.path.join(self.current_path, name)

        if full_path in self.locked_paths:
            pw, ok = QInputDialog.getText(self, "Locked", "Enter password:", QLineEdit.EchoMode.Password)
            if not ok or pw != self.locked_paths[full_path]:
                QMessageBox.warning(self, "Error", "Wrong password!")
                return

        if os.path.isdir(full_path):
            self.current_path = full_path
            self.path_edit.setText(self.current_path)
            self.load_directory()
        else:
            try:
                os.startfile(full_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def rename_item(self):
        selected = self.list_widget.currentItem()
        if not selected:
            return
        old_name = selected.text().replace("[LOCKED] ", "")
        old_path = os.path.join(self.current_path, old_name)

        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:")
        if ok and new_name:
            new_path = os.path.join(self.current_path, new_name)
            try:
                os.rename(old_path, new_path)
                if old_path in self.locked_paths:
                    self.locked_paths[new_path] = self.locked_paths.pop(old_path)
                self.load_directory()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def delete_item(self):
        selected = self.list_widget.currentItem()
        if not selected:
            return
        name = selected.text().replace("[LOCKED] ", "")
        full_path = os.path.join(self.current_path, name)

        confirm = QMessageBox.question(self, "Delete", f"Delete {name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(full_path):
                    os.rmdir(full_path)
                else:
                    os.remove(full_path)
                self.load_directory()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def lock_item(self):
        selected = self.list_widget.currentItem()
        if not selected:
            return
        name = selected.text().replace("[LOCKED] ", "")
        full_path = os.path.join(self.current_path, name)

        if full_path in self.locked_paths:
            QMessageBox.information(self, "Info", "This item is already locked.")
            return

        pw, ok = QInputDialog.getText(self, "Set Password", "Enter password:", QLineEdit.EchoMode.Password)
        if ok and pw:
            self.locked_paths[full_path] = pw
            self.load_directory()

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator - Luxxer')
        central = QWidget()
        layout = QVBoxLayout()
        self.display = QLineEdit()
        layout.addWidget(self.display)
        grid = QGridLayout() if False else QHBoxLayout()
        # simple implementation: user enters expression and presses evaluate
        eval_btn = QPushButton('Evaluate')
        eval_btn.clicked.connect(self.evaluate)
        layout.addWidget(eval_btn)
        central.setLayout(layout)
        layout.addWidget(self.display)
        self.setCentralWidget(central)

    def evaluate(self):
        expr = self.display.text()
        try:
            # safe eval environment
            allowed = {"abs": abs, "round": round, "min": min, "max": max}
            val = eval(expr, {"__builtins__": {}}, allowed)
            self.display.setText(str(val))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not evaluate: {e}')

# Zer3 small language + IDE

# ---

# Zer3 Interpreter

class Zer3Interpreter:
    def __init__(self, timeout: float = 5.0):
        self.vars: Dict[str, Any] = {}
        self.timeout = timeout
        self.python_exec = shutil.which("python") or shutil.which("python3") or sys.executable
        # safe builtins
        self.safe_builtins = {
            "abs": abs, "all": all, "any": any, "ascii": ascii, "bin": bin, "bool": bool,
            "bytearray": bytearray, "bytes": bytes, "callable": callable, "chr": chr,
            "classmethod": classmethod, "compile": compile, "complex": complex,
            "dict": dict, "dir": dir, "divmod": divmod, "enumerate": enumerate,
            "filter": filter, "float": float, "format": format, "frozenset": frozenset,
            "getattr": getattr, "hasattr": hasattr, "hash": hash, "hex": hex, "id": id,
            "int": int, "isinstance": isinstance, "issubclass": issubclass, "iter": iter,
            "len": len, "list": list, "locals": locals, "map": map, "max": max, "memoryview": memoryview,
            "min": min, "next": next, "object": object, "oct": oct, "ord": ord, "pow": pow,
            "print": print, "range": range, "repr": repr, "reversed": reversed, "round": round,
            "set": set, "slice": slice, "sorted": sorted, "staticmethod": staticmethod,
            "str": str, "sum": sum, "super": super, "tuple": tuple, "type": type, "vars": vars,
            "zip": zip, "input": lambda prompt="": "<input disabled in Zer3Interpreter>"
        }

    def run(self, code: str) -> str:
        code = code or ""
        # Prefer running in a clean subprocess
        if self.python_exec:
            try:
                proc = subprocess.run(
                    [self.python_exec, "-u", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
                out = proc.stdout or ""
                err = proc.stderr or ""
                if err:
                    return (out + "\n" + err).strip()
                return out.strip()
            except subprocess.TimeoutExpired:
                return f"<error: execution timed out after {self.timeout} seconds>"
            except Exception as e:
                fallback_msg = f"<warning: python subprocess failed, using Zer3 fallback: {e}>"
                fb = self._run_fallback(code)
                return f"{fallback_msg}\n{fb}"
        else:
            return self._run_fallback(code)

    def _run_fallback(self, code: str) -> str:
        f = io.StringIO()
        try:
            with contextlib.redirect_stdout(f):
                exec(code, {"__builtins__": self.safe_builtins}, self.vars)
        except Exception as e:
            f.write(f"<error: {e}>\n")
        return f.getvalue().strip()

# ----------------------------
# Zer3 Highlighter
# ----------------------------
class Zer3Highlighter(QSyntaxHighlighter):
    """
    Python-like syntax highlighter (~300 keywords/builtins).
    """

    def __init__(self, parent):
        super().__init__(parent)

        # format definitions
        self._fmt_keyword = QTextCharFormat()
        self._fmt_keyword.setForeground(QColor("#0000CC"))
        self._fmt_keyword.setFontWeight(QFont.Weight.DemiBold)

        self._fmt_builtin = QTextCharFormat()
        self._fmt_builtin.setForeground(QColor("#0033AA"))

        self._fmt_string = QTextCharFormat()
        self._fmt_string.setForeground(QColor("#008000"))

        self._fmt_comment = QTextCharFormat()
        self._fmt_comment.setForeground(QColor("#888888"))
        self._fmt_comment.setFontItalic(True)

        self._fmt_number = QTextCharFormat()
        self._fmt_number.setForeground(QColor("#AA00AA"))

        # 40+ keywords
        keywords = [
            "False","None","True","and","as","assert","async","await","break","class",
            "continue","def","del","elif","else","except","finally","for","from","global",
            "if","import","in","is","lambda","nonlocal","not","or","pass","raise",
            "return","try","while","with","yield"
        ]

        # 60+ builtins
        builtins = [
            "abs","all","any","ascii","bin","bool","bytearray","bytes","callable","chr",
            "classmethod","compile","complex","delattr","dict","dir","divmod","enumerate",
            "eval","exec","filter","float","format","frozenset","getattr","globals",
            "hasattr","hash","help","hex","id","input","int","isinstance","issubclass",
            "iter","len","list","locals","map","max","memoryview","min","next","object",
            "oct","open","ord","pow","print","property","range","repr","reversed","round",
            "set","setattr","slice","sorted","staticmethod","str","sum","super","tuple",
            "type","vars","zip"
        ]

        self.rules = []
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        self.rules.append((QRegularExpression(kw_pattern), self._fmt_keyword))
        bi_pattern = r"\b(" + "|".join(builtins) + r")\b"
        self.rules.append((QRegularExpression(bi_pattern), self._fmt_builtin))

        # numbers
        self.rules.append((QRegularExpression(r"\b[0-9]+(?:\.[0-9]+)?\b"), self._fmt_number))
        # strings
        self.rules.append((QRegularExpression(r'"[^"\n]*"'), self._fmt_string))
        self.rules.append((QRegularExpression(r"'[^'\n]*'"), self._fmt_string))
        # comments
        self.rule_comment = (QRegularExpression(r"#.*"), self._fmt_comment)
        # multi-line strings
        self.triple_double = QRegularExpression('"""')
        self.triple_single = QRegularExpression("'''")

    def highlightBlock(self, text: str):
        self.setCurrentBlockState(0)
        in_multiline = self.previousBlockState() != 0

        # multi-line strings
        if in_multiline:
            start_expr = self.triple_double if getattr(self, "_ml_is_double", True) else self.triple_single
            match_iter = start_expr.globalMatch(text)
            if match_iter.hasNext():
                m = match_iter.next()
                end_index = m.capturedStart()
                self.setFormat(0, end_index + 3, self._fmt_string)
                self.setCurrentBlockState(0)
            else:
                self.setFormat(0, len(text), self._fmt_string)
                self.setCurrentBlockState(1)
                return
        else:
            for triple, is_double in [(self.triple_double, True), (self.triple_single, False)]:
                m_iter = triple.globalMatch(text)
                while m_iter.hasNext():
                    m = m_iter.next()
                    start = m.capturedStart()
                    rest = text[start+3:]
                    end_pos = rest.find('"""' if is_double else "'''")
                    if end_pos == -1:
                        self.setFormat(start, len(text)-start, self._fmt_string)
                        self.setCurrentBlockState(1)
                        self._ml_is_double = is_double
                    else:
                        self.setFormat(start, end_pos+6, self._fmt_string)

        # inline comments
        cm_iter = self.rule_comment[0].globalMatch(text)
        while cm_iter.hasNext():
            m = cm_iter.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self._fmt_comment)

        # inline strings, keywords, numbers, builtins
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

    def set_keywords(self, keywords_list):
        kw_pattern = r"\b(" + "|".join(keywords_list) + r")\b"
        self.rules[0] = (QRegularExpression(kw_pattern), self._fmt_keyword)
        self.rehighlight()

class Zer3IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zer3 IDE - Luxxer")
        self.resize(900, 600)

        # Central widget and layout
        central = QWidget()
        layout = QVBoxLayout(central)

        # Code editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your Zer3 code here...")
        self.highlighter = Zer3Highlighter(self.editor.document())
        layout.addWidget(self.editor)

        # Run button
        run_btn = QPushButton("Run Code")
        run_btn.clicked.connect(self.run_code)
        layout.addWidget(run_btn)

        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Output will be displayed here...")
        layout.addWidget(self.output)

        self.setCentralWidget(central)

        # Interpreter instance
        self.interpreter = Zer3Interpreter()

    def run_code(self):
        """Executes the code written in the editor using Zer3Interpreter."""
        code = self.editor.toPlainText().strip()
        if not code:
            self.output.setPlainText("⚠️ No code to run.")
            return
        try:
            result = self.interpreter.run(code)
            self.output.setPlainText(str(result))
        except Exception as e:
            self.output.setPlainText(f"❌ Error: {e}")

# -----------------------------
# Cybersecurity toolkit (educational)
# -----------------------------

class BruteForceThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, target_hash: str, charset: str, max_len: int, hash_algo='sha256'):
        super().__init__()
        self.target_hash = target_hash
        self.charset = charset
        self.max_len = max_len
        self.hash_algo = hash_algo
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self, __generate_combinations=None):
        # WARNING: This is a local educational simulation only.
        # We only attempt very short passwords; this is deliberately constrained.
        tried = 0
        for L in range(1, self.max_len+1):
            if self._stop:
                self.finished.emit('Stopped')
                return
            for combo in __generate_combinations(self.charset, L):
                tried += 1
                if tried % 1000 == 0:
                    self.progress.emit(int(100 * tried / (len(self.charset) ** self.max_len)))
                h = hashlib.new(self.hash_algo, combo.encode()).hexdigest()
                if h == self.target_hash:
                    self.finished.emit(combo)
                    return
        self.finished.emit('NOTFOUND')


def __generate_combinations(chars, length):
    if length == 1:
        for c in chars:
            yield c
    else:
        for c in chars:
            for suf in __generate_combinations(chars, length-1):
                yield c + suf


class HashGenerator:
    @staticmethod
    def generate(text: str, algo='sha256') -> str:
        h = hashlib.new(algo, text.encode())
        return h.hexdigest()

class LuxxerWebApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LuxxerWeb - Browser Launcher")
        w = QWidget()
        l = QVBoxLayout(w)

        l.addWidget(QLabel("LuxxerWeb safe browser launcher demo."))
        l.addWidget(QLabel("Enter URL to open:"))

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        l.addWidget(self.url_input)

        open_btn = QPushButton("Open in default browser")
        open_btn.clicked.connect(self.open_url)
        l.addWidget(open_btn)

        self.setCentralWidget(w)

    def open_url(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        webbrowser.open(url)

class MailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mail - Luxxer")
        self.resize(800, 600)

        # Central widget
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Header
        header_layout = QHBoxLayout()
        self.layout.addLayout(header_layout)
        header_layout.addWidget(QLabel("Inbox"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_inbox)
        header_layout.addWidget(self.refresh_btn)
        self.compose_btn = QPushButton("Compose")
        self.compose_btn.clicked.connect(self.compose)
        header_layout.addWidget(self.compose_btn)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search mails...")
        self.search_bar.textChanged.connect(self.filter_inbox)
        self.layout.addWidget(self.search_bar)

        # Inbox list
        self.inbox_list = QListWidget()
        self.layout.addWidget(self.inbox_list)
        self.inbox = []
        self.generate_demo_mails()
        self.update_inbox_list()

        # Draft storage
        self.drafts = []

    def generate_demo_mails(self):
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        subjects = ["Meeting Update", "Project Deadline", "Invoice", "Greetings", "Newsletter"]
        for _ in range(15):
            sender = random.choice(names)
            subject = random.choice(subjects)
            time = datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 72))
            self.inbox.append({
                "sender": sender,
                "subject": subject,
                "time": time.strftime("%Y-%m-%d %H:%M"),
                "content": f"This is a demo content from {sender} about {subject}."
            })

    def update_inbox_list(self):
        self.inbox_list.clear()
        for mail in self.inbox:
            self.inbox_list.addItem(f"{mail['time']} | {mail['sender']} | {mail['subject']}")

    def refresh_inbox(self):
        self.generate_demo_mails()
        self.update_inbox_list()
        QMessageBox.information(self, "Mail", "Inbox refreshed!")

    def filter_inbox(self, text):
        self.inbox_list.clear()
        for mail in self.inbox:
            if text.lower() in mail['subject'].lower() or text.lower() in mail['sender'].lower():
                self.inbox_list.addItem(f"{mail['time']} | {mail['sender']} | {mail['subject']}")

    def compose(self):
        dlg = QTextEdit()
        dlg.setWindowTitle("Compose Mail")
        dlg.resize(600, 400)
        dlg.show()

def open_draft_dialog(self):
    dlg = QDialog(self)
    dlg.setWindowTitle("Edit Draft")

    # Example editor; replace with your actual widget
    editor = QTextEdit(dlg)
    editor.setPlainText("")  # or load existing text
    dlg.resize(400, 300)

    # Keep a reference to the dialog’s original closeEvent
    original_close = dlg.closeEvent

    def on_close(event):
        content = editor.toPlainText()
        if content.strip():
            self.drafts.append(content)
            QMessageBox.information(dlg, "Draft Saved", "Your draft has been saved.")
        # Call Qt’s built-in cleanup
        original_close(event)

    # Override closeEvent before showing the dialog
    dlg.closeEvent = on_close

    dlg.exec_()

class CmdApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CMD - Luxxer')
        central = QWidget()
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_enter)
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.cwd = os.path.expanduser('~')
        self.write(f'Luxxer CMD (cwd={self.cwd}). Type help for commands.')
        self.whitelist = ['dir','ls','echo','type','cat'] if os.name != 'nt' else ['dir','echo','type']

    def write(self, text: str):
        self.output.append(text)

    def safe_execute(self, cmd: list[str]) -> str:
        """Execute only whitelisted commands if real-cmds enabled. Returns combined output."""
        enabled = APP_STATE['settings'].get('enable_real_cmds', False)
        if not enabled:
            return 'Real command execution is DISABLED in settings.You can simulate commands instead.'
        # check whitelist
        base = cmd[0]
        if base not in self.whitelist:
            return f'Command "{base}" is not permitted in real-exec mode.'
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return res.stdout + res.stderr
        except Exception as e:
            return f'Execution error: {e}'

    def on_enter(self):
        line = self.input.text().strip()
        self.input.clear()
        if not line:
            return
        self.write(f'> {line}')
        if line == 'help':
            self.write('Commands: help, pwd, ls/dir, cd <path>, echo <text>, run <whitelisted cmd...>')
            return
        parts = line.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd in ('pwd', 'cd'):
            if cmd == 'pwd':
                self.write(self.cwd)
            else:
                if args:
                    new = os.path.abspath(os.path.join(self.cwd, args[0]))
                    if os.path.isdir(new):
                        self.cwd = new
                        self.write(f'cwd -> {self.cwd}')
                    else:
                        self.write('Directory not found')
                else:
                    self.write('cd requires a path')
            return
        if cmd in ('ls','dir'):
            try:
                items = os.listdir(self.cwd)
                self.write(''.join(items))
            except Exception as e:
                self.write(f'ls error: {e}')
            return
        if cmd == 'echo':
            self.write(' '.join(args))
            return
        if cmd == 'run':
            if not args:
                self.write('Usage: run <command> <args>...')
                return
            out = self.safe_execute(args)
            self.write(out)
            return
        # otherwise simulate
        self.write(f'Simulated: {line}')

# Try to import translation/state helpers from your project; if missing, provide fallback.
try:
    from Luxxer_OS_helpers import tr, APP_STATE
except Exception:
    APP_STATE = {}
    def tr(k): return k  # fallback: identity


# Utilities
class HashGenerator:
    @staticmethod
    def generate(text: str, algo: str = "sha256") -> str:
        algo = algo.lower()
        if algo in ("md5", "sha1", "sha224", "sha256", "sha384", "sha512"):
            h = hashlib.new(algo)
            h.update(text.encode("utf-8"))
            return h.hexdigest()
        # fallback: try to create algorithm
        try:
            h = hashlib.new(algo)
            h.update(text.encode("utf-8"))
            return h.hexdigest()
        except Exception as e:
            raise ValueError(f"Unsupported algorithm: {algo}") from e

    @staticmethod
    def crc32(text: str) -> str:
        return format(zlib.crc32(text.encode("utf-8")) & 0xFFFFFFFF, '08x')


# ---- Brute-force thread (local demo only, limited length to avoid runaway) ----
class BruteForceThread(QThread):
    progress = pyqtSignal(int)       # 0-100
    finished = pyqtSignal(str)       # found candidate / "Not found" / "Stopped"
    status = pyqtSignal(str)         # textual status updates

    def __init__(self, target_hash: str, chars: str, maxlen: int, algo: str = "sha256"):
        super().__init__()
        self.target_hash = target_hash.strip().lower()
        self.chars = chars
        self.maxlen = maxlen
        self.algo = algo.lower()
        self._running = True

    def run(self):
        # Validate algo
        try:
            hashlib.new(self.algo)
        except Exception:
            self.finished.emit("Invalid algorithm")
            return

        if not self.chars:
            self.finished.emit("No charset")
            return
        # enforce safety absolute cap
        safe_cap = 5  # absolute max; GUI may enforce smaller
        if self.maxlen > safe_cap:
            self.maxlen = safe_cap

        total = 0
        for l in range(1, self.maxlen + 1):
            total += len(self.chars) ** l
        if total == 0:
            self.finished.emit("Nothing to try")
            return

        tried = 0
        self.status.emit(f"Starting bruteforce: total combos approx {total}")
        for length in range(1, self.maxlen + 1):
            for combo in itertools.product(self.chars, repeat=length):
                if not self._running:
                    self.finished.emit("Stopped")
                    return
                candidate = ''.join(combo)
                h = hashlib.new(self.algo, candidate.encode("utf-8")).hexdigest()
                tried += 1
                pct = int((tried / total) * 100)
                self.progress.emit(pct)
                # occasional status
                if tried % 1000 == 0:
                    self.status.emit(f"Tried {tried}/{total} combos (len {length})")
                if h == self.target_hash:
                    self.finished.emit(candidate)
                    return
        self.finished.emit("Not found")

    def stop(self):
        self._running = False

# Main CyberToolsApp

class CyberToolsApp(QMainWindow):
    """
    CyberToolsApp - educational, local-only cybersecurity toolbox.
    Contains many small utilities (hash, base64, encoders, brute-force simulator, password generator, etc.)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{tr('tools')} - Luxxer (educational)")
        self.resize(900, 600)

        self._brute_thread: Optional[BruteForceThread] = None

        # main layout: left list of tools, right stacked area
        central = QWidget()
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # tool list
        self.tool_list = QListWidget()
        self.tool_names = [
            "Hash Generator",
            "Hash Compare",
            "Brute Force (demo)",
            "Base64 Encode/Decode",
            "Hex Encode/Decode",
            "Password Generator",
            "Entropy Calculator",
            "HMAC Generator",
            "PBKDF2 Derive",
            "CRC32",
            "ROT13 / Caesar",
            "XOR Cipher",
            "Regex Tester",
            "JWT Decoder (header/payload only)",
            "UUID Generator",
            "Random Bytes",
            "Binary/Text converter",
            "URL Encode/Decode",
            "Common Weakpassword Check",
            "Simple Cipher Suite (Caesar + XOR)",
            "Entropy Visualizer"
        ]
        for name in self.tool_names:
            QListWidgetItem(tr(name), self.tool_list)

        self.tool_list.currentRowChanged.connect(self._on_tool_changed)
        main_layout.addWidget(self.tool_list, 1)

        # stacked area (we'll create panels dictionary)
        self.panels = {}
        self.panel_container = QWidget()
        self.panel_layout = QVBoxLayout()
        self.panel_container.setLayout(self.panel_layout)
        main_layout.addWidget(self.panel_container, 3)

        # build panels
        self._build_hash_panel()
        self._build_hash_compare_panel()
        self._build_bruteforce_panel()
        self._build_base64_panel()
        self._build_hex_panel()
        self._build_password_gen_panel()
        self._build_entropy_panel()
        self._build_hmac_panel()
        self._build_pbkdf2_panel()
        self._build_crc_panel()
        self._build_rot13_panel()
        self._build_xor_panel()
        self._build_regex_panel()
        self._build_jwt_panel()
        self._build_uuid_panel()
        self._build_random_bytes_panel()
        self._build_bintext_panel()
        self._build_url_panel()
        self._build_commonpw_panel()
        self._build_cipher_suite_panel()
        self._build_entropy_vis_panel()

        # show first
        self.tool_list.setCurrentRow(0)

    # helpers for panel switching
    def _clear_panel(self):
        for i in reversed(range(self.panel_layout.count())):
            w = self.panel_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

    def _show_panel(self, widget: QWidget):
        self._clear_panel()
        self.panel_layout.addWidget(widget)

    def _on_tool_changed(self, idx: int):
        name = self.tool_names[idx]
        panel = self.panels.get(name)
        if panel:
            self._show_panel(panel)

    # panel builders
    def _build_hash_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        hl = QHBoxLayout()
        hl.addWidget(QLabel(tr("open_file") + ":") )  # reusing key as label
        self.hash_text_input = QLineEdit()
        hl.addWidget(self.hash_text_input)
        hl.addWidget(QLabel(tr("language") + ":"))
        self.hash_algo = QLineEdit("sha256")
        hl.addWidget(self.hash_algo)
        self.hash_btn = QPushButton(tr("run"))
        self.hash_btn.clicked.connect(self._hash_run)
        hl.addWidget(self.hash_btn)
        l.addLayout(hl)
        l.addWidget(QLabel(tr("about") + ":"))
        self.hash_out = QLineEdit()
        self.hash_out.setReadOnly(True)
        l.addWidget(self.hash_out)
        self.panels["Hash Generator"] = p

    def _hash_run(self):
        txt = self.hash_text_input.text()
        algo = self.hash_algo.text() or "sha256"
        try:
            h = HashGenerator.generate(txt, algo)
            self.hash_out.setText(h)
        except Exception as e:
            QMessageBox.warning(self, "Hash error", str(e))

    def _build_hash_compare_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.hashcmp_text = QLineEdit()
        row.addWidget(self.hashcmp_text)
        row.addWidget(QLabel("Algo:"))
        self.hashcmp_algo = QLineEdit("sha256")
        row.addWidget(self.hashcmp_algo)
        row.addWidget(QLabel("Hash:"))
        self.hashcmp_hash = QLineEdit()
        row.addWidget(self.hashcmp_hash)
        self.hashcmp_btn = QPushButton("Compare")
        self.hashcmp_btn.clicked.connect(self._hash_compare)
        row.addWidget(self.hashcmp_btn)
        l.addLayout(row)
        l.addWidget(QLabel("Result:"))
        self.hashcmp_out = QLabel("")
        l.addWidget(self.hashcmp_out)
        self.panels["Hash Compare"] = p

    def _hash_compare(self):
        txt = self.hashcmp_text.text()
        algo = self.hashcmp_algo.text() or "sha256"
        target = self.hashcmp_hash.text().strip().lower()
        try:
            h = HashGenerator.generate(txt, algo).lower()
            ok = h == target
            self.hashcmp_out.setText("MATCH" if ok else "NO MATCH")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_bruteforce_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Brute-force simulator (local-only, educational)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Target hash:"))
        self.bf_target = QLineEdit()
        row.addWidget(self.bf_target)
        row.addWidget(QLabel("Algo:"))
        self.bf_algo = QLineEdit("sha256")
        row.addWidget(self.bf_algo)
        l.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Charset:"))
        self.bf_charset = QLineEdit("abc123")
        row2.addWidget(self.bf_charset)
        row2.addWidget(QLabel("Max len (<=5):"))
        self.bf_maxlen_spin = QSpinBox()
        self.bf_maxlen_spin.setMinimum(1)
        self.bf_maxlen_spin.setMaximum(5)
        self.bf_maxlen_spin.setValue(3)
        row2.addWidget(self.bf_maxlen_spin)
        self.bf_start_btn = QPushButton("Start Brute")
        self.bf_start_btn.clicked.connect(self._start_brute)
        row2.addWidget(self.bf_start_btn)
        self.bf_stop_btn = QPushButton("Stop")
        self.bf_stop_btn.clicked.connect(self._stop_brute)
        row2.addWidget(self.bf_stop_btn)
        l.addLayout(row2)

        self.bf_progress = QProgressBar()
        l.addWidget(self.bf_progress)
        self.bf_status = QLabel("")
        l.addWidget(self.bf_status)

        self.panels["Brute Force (demo)"] = p

    def _start_brute(self):
        if self._brute_thread and self._brute_thread.isRunning():
            QMessageBox.information(self, "Info", "Brute already running")
            return
        target = self.bf_target.text().strip().lower()
        if not target:
            QMessageBox.warning(self, "Error", "Target hash required")
            return
        algo = self.bf_algo.text().strip() or "sha256"
        chars = self.bf_charset.text()
        maxlen = int(self.bf_maxlen_spin.value())
        # safety limit
        if maxlen > 5:
            QMessageBox.warning(self, "Limit", "Max len limited to 5 for safety.")
            maxlen = 5
        # create thread
        self._brute_thread = BruteForceThread(target, chars, maxlen, algo)
        self._brute_thread.progress.connect(self.bf_progress.setValue)
        self._brute_thread.status.connect(self.bf_status.setText)
        self._brute_thread.finished.connect(self._brute_finished)
        self._brute_thread.start()
        self.bf_status.setText("Started")

    def _stop_brute(self):
        if self._brute_thread:
            self._brute_thread.stop()
            self.bf_status.setText("Stopping...")

    def _brute_finished(self, result):
        self.bf_status.setText(f"Finished: {result}")
        QMessageBox.information(self, "Brute result", f"Result: {result}")
        self.bf_progress.setValue(0)
        self._brute_thread = None

    def _build_base64_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Base64 Encode / Decode"))
        row = QHBoxLayout()
        self.b64_input = QLineEdit()
        row.addWidget(self.b64_input)
        self.b64_encode_btn = QPushButton("Encode")
        self.b64_encode_btn.clicked.connect(self._b64_encode)
        row.addWidget(self.b64_encode_btn)
        self.b64_decode_btn = QPushButton("Decode")
        self.b64_decode_btn.clicked.connect(self._b64_decode)
        row.addWidget(self.b64_decode_btn)
        l.addLayout(row)
        self.b64_out = QTextEdit()
        self.b64_out.setReadOnly(True)
        l.addWidget(self.b64_out)
        self.panels["Base64 Encode/Decode"] = p

    def _b64_encode(self):
        try:
            data = self.b64_input.text().encode("utf-8")
            b = base64.b64encode(data).decode()
            self.b64_out.setPlainText(b)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _b64_decode(self):
        try:
            s = self.b64_input.text().strip()
            data = base64.b64decode(s)
            self.b64_out.setPlainText(data.decode("utf-8", errors="replace"))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_hex_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Hex Encode / Decode"))
        row = QHBoxLayout()
        self.hex_input = QLineEdit()
        row.addWidget(self.hex_input)
        self.hex_enc_btn = QPushButton("To Hex")
        self.hex_enc_btn.clicked.connect(self._hex_encode)
        row.addWidget(self.hex_enc_btn)
        self.hex_dec_btn = QPushButton("From Hex")
        self.hex_dec_btn.clicked.connect(self._hex_decode)
        row.addWidget(self.hex_dec_btn)
        l.addLayout(row)
        self.hex_out = QTextEdit(); self.hex_out.setReadOnly(True)
        l.addWidget(self.hex_out)
        self.panels["Hex Encode/Decode"] = p

    def _hex_encode(self):
        try:
            b = self.hex_input.text().encode("utf-8")
            self.hex_out.setPlainText(binascii.hexlify(b).decode())
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _hex_decode(self):
        try:
            s = self.hex_input.text().strip()
            b = binascii.unhexlify(s)
            self.hex_out.setPlainText(b.decode("utf-8", errors="replace"))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_password_gen_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Password Generator"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Length:"))
        self.pw_len_spin = QSpinBox(); self.pw_len_spin.setMinimum(4); self.pw_len_spin.setMaximum(128); self.pw_len_spin.setValue(12)
        row.addWidget(self.pw_len_spin)
        self.pw_symbols_chk = QCheckBox("Include symbols")
        row.addWidget(self.pw_symbols_chk)
        self.pw_gen_btn = QPushButton("Generate")
        self.pw_gen_btn.clicked.connect(self._gen_password)
        row.addWidget(self.pw_gen_btn)
        l.addLayout(row)
        self.pw_out = QLineEdit(); self.pw_out.setReadOnly(True)
        l.addWidget(self.pw_out)
        self.panels["Password Generator"] = p

    def _gen_password(self):
        length = int(self.pw_len_spin.value())
        alphabet = string.ascii_letters + string.digits
        if self.pw_symbols_chk.isChecked():
            alphabet += "!@#$%^&*()-_=+[]{};:,.<>/?"
        pw = ''.join(secrets.choice(alphabet) for _ in range(length))
        self.pw_out.setText(pw)

    def _build_entropy_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Entropy Calculator"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.ent_input = QLineEdit()
        row.addWidget(self.ent_input)
        self.ent_calc_btn = QPushButton("Calc")
        self.ent_calc_btn.clicked.connect(self._calc_entropy)
        row.addWidget(self.ent_calc_btn)
        l.addLayout(row)
        self.ent_out = QLabel("")
        l.addWidget(self.ent_out)
        self.panels["Entropy Calculator"] = p

    def _calc_entropy(self):
        s = self.ent_input.text()
        if not s:
            self.ent_out.setText("0")
            return
        # Shannon entropy
        from math import log2
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1
        l = len(s)
        ent = -sum((count / l) * (log2(count / l)) for count in freq.values())
        self.ent_out.setText(f"{ent:.4f} bits/char (total {ent * l:.2f} bits)")

    def _build_hmac_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("HMAC Generator"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Key:"))
        self.hmac_key = QLineEdit()
        row.addWidget(self.hmac_key)
        row.addWidget(QLabel("Message:"))
        self.hmac_msg = QLineEdit()
        row.addWidget(self.hmac_msg)
        row.addWidget(QLabel("Algo:"))
        self.hmac_algo = QLineEdit("sha256")
        row.addWidget(self.hmac_algo)
        self.hmac_btn = QPushButton("Compute")
        self.hmac_btn.clicked.connect(self._compute_hmac)
        row.addWidget(self.hmac_btn)
        l.addLayout(row)
        self.hmac_out = QLineEdit(); self.hmac_out.setReadOnly(True)
        l.addWidget(self.hmac_out)
        self.panels["HMAC Generator"] = p

    def _compute_hmac(self):
        try:
            import hmac
            key = self.hmac_key.text().encode("utf-8")
            msg = self.hmac_msg.text().encode("utf-8")
            algo = self.hmac_algo.text() or "sha256"
            h = hmac.new(key, msg, algo).hexdigest()
            self.hmac_out.setText(h)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_pbkdf2_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("PBKDF2 Derive (demo)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Password:"))
        self.pbk_pwd = QLineEdit()
        row.addWidget(self.pbk_pwd)
        row.addWidget(QLabel("Salt:"))
        self.pbk_salt = QLineEdit("salt")
        row.addWidget(self.pbk_salt)
        row.addWidget(QLabel("Iterations:"))
        self.pbk_iter = QSpinBox(); self.pbk_iter.setMinimum(100); self.pbk_iter.setMaximum(1000000); self.pbk_iter.setValue(10000)
        row.addWidget(self.pbk_iter)
        row.addWidget(QLabel("KeyLen:"))
        self.pbk_keylen = QSpinBox(); self.pbk_keylen.setMinimum(16); self.pbk_keylen.setMaximum(64); self.pbk_keylen.setValue(32)
        row.addWidget(self.pbk_keylen)
        self.pbk_btn = QPushButton("Derive")
        self.pbk_btn.clicked.connect(self._pbkdf2)
        row.addWidget(self.pbk_btn)
        l.addLayout(row)
        self.pbk_out = QLineEdit(); self.pbk_out.setReadOnly(True)
        l.addWidget(self.pbk_out)
        self.panels["PBKDF2 Derive"] = p

    def _pbkdf2(self):
        try:
            pwd = self.pbk_pwd.text().encode("utf-8")
            salt = self.pbk_salt.text().encode("utf-8")
            it = int(self.pbk_iter.value())
            keylen = int(self.pbk_keylen.value())
            dk = hashlib.pbkdf2_hmac('sha256', pwd, salt, it, dklen=keylen)
            self.pbk_out.setText(binascii.hexlify(dk).decode())
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_crc_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("CRC32"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.crc_input = QLineEdit()
        row.addWidget(self.crc_input)
        self.crc_btn = QPushButton("Compute")
        self.crc_btn.clicked.connect(self._crc32)
        row.addWidget(self.crc_btn)
        l.addLayout(row)
        self.crc_out = QLineEdit(); self.crc_out.setReadOnly(True)
        l.addWidget(self.crc_out)
        self.panels["CRC32"] = p

    def _crc32(self):
        try:
            s = self.crc_input.text()
            self.crc_out.setText(HashGenerator.crc32(s))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_rot13_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("ROT13 / Caesar cipher"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.rot_input = QLineEdit()
        row.addWidget(self.rot_input)
        row.addWidget(QLabel("Shift (Caesar):"))
        self.rot_shift = QSpinBox(); self.rot_shift.setRange(0,25); self.rot_shift.setValue(13)
        row.addWidget(self.rot_shift)
        self.rot_btn = QPushButton("Apply")
        self.rot_btn.clicked.connect(self._rot_apply)
        row.addWidget(self.rot_btn)
        l.addLayout(row)
        self.rot_out = QLineEdit(); self.rot_out.setReadOnly(True)
        l.addWidget(self.rot_out)
        self.panels["ROT13 / Caesar"] = p

    def _rot_apply(self):
        s = self.rot_input.text()
        shift = int(self.rot_shift.value())
        def caesar(ch):
            if 'a' <= ch <= 'z':
                return chr((ord(ch)-97 + shift) % 26 + 97)
            if 'A' <= ch <= 'Z':
                return chr((ord(ch)-65 + shift) % 26 + 65)
            return ch
        res = ''.join(caesar(c) for c in s)
        self.rot_out.setText(res)

    def _build_xor_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("XOR Cipher (single-byte key)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.xor_input = QLineEdit()
        row.addWidget(self.xor_input)
        row.addWidget(QLabel("Key byte (0-255):"))
        self.xor_key = QSpinBox(); self.xor_key.setRange(0,255); self.xor_key.setValue(42)
        row.addWidget(self.xor_key)
        self.xor_btn = QPushButton("Apply")
        self.xor_btn.clicked.connect(self._xor_apply)
        row.addWidget(self.xor_btn)
        l.addLayout(row)
        self.xor_out = QLineEdit(); self.xor_out.setReadOnly(True)
        l.addWidget(self.xor_out)
        self.panels["XOR Cipher"] = p

    def _xor_apply(self):
        try:
            key = int(self.xor_key.value())
            data = self.xor_input.text().encode("utf-8")
            res = bytes([b ^ key for b in data])
            self.xor_out.setText(binascii.hexlify(res).decode())
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_regex_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Regex Tester"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Pattern:"))
        self.re_pattern = QLineEdit()
        row.addWidget(self.re_pattern)
        row.addWidget(QLabel("Text:"))
        self.re_text = QLineEdit()
        row.addWidget(self.re_text)
        self.re_btn = QPushButton("Test")
        self.re_btn.clicked.connect(self._regex_test)
        row.addWidget(self.re_btn)
        l.addLayout(row)
        self.re_out = QLabel("")
        l.addWidget(self.re_out)
        self.panels["Regex Tester"] = p

    def _regex_test(self):
        import re
        try:
            patt = re.compile(self.re_pattern.text())
            m = patt.search(self.re_text.text())
            self.re_out.setText("Match" if m else "No match")
        except Exception as e:
            QMessageBox.warning(self, "Regex error", str(e))

    def _build_jwt_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("JWT Decoder (header/payload only, no verification)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("JWT:"))
        self.jwt_input = QLineEdit()
        row.addWidget(self.jwt_input)
        self.jwt_btn = QPushButton("Decode")
        self.jwt_btn.clicked.connect(self._jwt_decode)
        row.addWidget(self.jwt_btn)
        l.addLayout(row)
        self.jwt_out = QTextEdit(); self.jwt_out.setReadOnly(True)
        l.addWidget(self.jwt_out)
        self.panels["JWT Decoder (header/payload only)"] = p

    def _jwt_decode(self):
        try:
            token = self.jwt_input.text().strip()
            parts = token.split('.')
            if len(parts) < 2:
                raise ValueError("Not a JWT")
            def _b64d(s):
                s += '=' * (-len(s) % 4)
                return base64.urlsafe_b64decode(s.encode())
            header = json.loads(_b64d(parts[0]))
            payload = json.loads(_b64d(parts[1]))
            pretty = json.dumps({"header": header, "payload": payload}, indent=2, ensure_ascii=False)
            self.jwt_out.setPlainText(pretty)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_uuid_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("UUID Generator"))
        row = QHBoxLayout()
        self.uuid_btn = QPushButton("Generate UUID4")
        self.uuid_btn.clicked.connect(self._uuid_gen)
        row.addWidget(self.uuid_btn)
        l.addLayout(row)
        self.uuid_out = QLineEdit(); self.uuid_out.setReadOnly(True)
        l.addWidget(self.uuid_out)
        self.panels["UUID Generator"] = p

    def _uuid_gen(self):
        import uuid
        self.uuid_out.setText(str(uuid.uuid4()))

    def _build_random_bytes_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Random Bytes Generator"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Length:"))
        self.rb_len = QSpinBox(); self.rb_len.setMinimum(1); self.rb_len.setMaximum(1024); self.rb_len.setValue(16)
        row.addWidget(self.rb_len)
        self.rb_btn = QPushButton("Generate")
        self.rb_btn.clicked.connect(self._rb_gen)
        row.addWidget(self.rb_btn)
        l.addLayout(row)
        self.rb_out = QLineEdit(); self.rb_out.setReadOnly(True)
        l.addWidget(self.rb_out)
        self.panels["Random Bytes"] = p

    def _rb_gen(self):
        n = int(self.rb_len.value())
        b = secrets.token_bytes(n)
        self.rb_out.setText(binascii.hexlify(b).decode())

    def _build_bintext_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Binary / Text converter"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.bt_input = QLineEdit()
        row.addWidget(self.bt_input)
        self.bt_to_bin = QPushButton("To Binary")
        self.bt_to_bin.clicked.connect(self._to_binary)
        row.addWidget(self.bt_to_bin)
        self.bt_from_bin = QPushButton("From Binary")
        self.bt_from_bin.clicked.connect(self._from_binary)
        row.addWidget(self.bt_from_bin)
        l.addLayout(row)
        self.bt_out = QTextEdit(); self.bt_out.setReadOnly(True)
        l.addWidget(self.bt_out)
        self.panels["Binary/Text converter"] = p

    def _to_binary(self):
        s = self.bt_input.text()
        self.bt_out.setPlainText(' '.join(format(ord(c), '08b') for c in s))

    def _from_binary(self):
        try:
            parts = self.bt_input.text().strip().split()
            chars = [chr(int(p, 2)) for p in parts]
            self.bt_out.setPlainText(''.join(chars))
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def _build_url_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("URL Encode / Decode"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.url_input = QLineEdit()
        row.addWidget(self.url_input)
        self.url_enc_btn = QPushButton("Encode")
        self.url_enc_btn.clicked.connect(self._url_encode)
        row.addWidget(self.url_enc_btn)
        self.url_dec_btn = QPushButton("Decode")
        self.url_dec_btn.clicked.connect(self._url_decode)
        row.addWidget(self.url_dec_btn)
        l.addLayout(row)
        self.url_out = QTextEdit(); self.url_out.setReadOnly(True)
        l.addWidget(self.url_out)
        self.panels["URL Encode/Decode"] = p

    def _url_encode(self):
        from urllib.parse import quote
        self.url_out.setPlainText(quote(self.url_input.text()))

    def _url_decode(self):
        from urllib.parse import unquote
        self.url_out.setPlainText(unquote(self.url_input.text()))

    def _build_commonpw_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Common Weak Password Check (local dictionary)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Password:"))
        self.cpw_input = QLineEdit()
        row.addWidget(self.cpw_input)
        self.cpw_btn = QPushButton("Check")
        self.cpw_btn.clicked.connect(self._check_common_pw)
        row.addWidget(self.cpw_btn)
        l.addLayout(row)
        self.cpw_out = QLabel("")
        l.addWidget(self.cpw_out)
        self.panels["Common Weakpassword Check"] = p
        # local small dictionary
        self._common_passwords = {"123456","password","qwerty","abc123","letmein","admin","login","welcome"}

    def _check_common_pw(self):
        pw = self.cpw_input.text().strip()
        if not pw:
            self.cpw_out.setText("Enter password")
            return
        if pw in self._common_passwords:
            self.cpw_out.setText("Very weak (found in local common list)")
        else:
            self.cpw_out.setText("Not found in small local list (does not mean strong)")

    def _build_cipher_suite_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Simple Cipher Suite"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.cs_input = QLineEdit()
        row.addWidget(self.cs_input)
        row.addWidget(QLabel("Caesar shift:"))
        self.cs_shift = QSpinBox(); self.cs_shift.setRange(0,25); self.cs_shift.setValue(3)
        row.addWidget(self.cs_shift)
        row.addWidget(QLabel("XOR key (0-255):"))
        self.cs_xorkey = QSpinBox(); self.cs_xorkey.setRange(0,255); self.cs_xorkey.setValue(7)
        row.addWidget(self.cs_xorkey)
        self.cs_apply_btn = QPushButton("Apply Caesar+XOR")
        self.cs_apply_btn.clicked.connect(self._cs_apply)
        row.addWidget(self.cs_apply_btn)
        l.addLayout(row)
        self.cs_out = QLineEdit(); self.cs_out.setReadOnly(True)
        l.addWidget(self.cs_out)
        self.panels["Simple Cipher Suite (Caesar + XOR)"] = p

    def _cs_apply(self):
        text = self.cs_input.text()
        shift = int(self.cs_shift.value())
        key = int(self.cs_xorkey.value())
        # Caesar
        def caesar_char(ch):
            if 'a' <= ch <= 'z':
                return chr((ord(ch)-97 + shift)%26 + 97)
            if 'A' <= ch <= 'Z':
                return chr((ord(ch)-65 + shift)%26 + 65)
            return ch
        c = ''.join(caesar_char(ch) for ch in text)
        xb = bytes([b ^ key for b in c.encode("utf-8")])
        self.cs_out.setText(binascii.hexlify(xb).decode())

    def _build_entropy_vis_panel(self):
        p = QWidget(); l = QVBoxLayout(); p.setLayout(l)
        l.addWidget(QLabel("Entropy Visualizer (basic)"))
        row = QHBoxLayout()
        row.addWidget(QLabel("Text:"))
        self.ev_input = QLineEdit()
        row.addWidget(self.ev_input)
        self.ev_btn = QPushButton("Visualize")
        self.ev_btn.clicked.connect(self._ev_visualize)
        row.addWidget(self.ev_btn)
        l.addLayout(row)
        self.ev_out = QTextEdit(); self.ev_out.setReadOnly(True)
        l.addWidget(self.ev_out)
        self.panels["Entropy Visualizer"] = p

    def _ev_visualize(self):
        s = self.ev_input.text()
        if not s:
            self.ev_out.setPlainText("No data")
            return
        from math import log2
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1
        l = len(s)
        ent = -sum((count / l) * (log2(count / l)) for count in freq.values())
        lines = [f"Char '{repr(ch)}': count {cnt}, freq {cnt/l:.3f}" for ch,cnt in freq.items()]
        lines.append(f"\nEntropy per char: {ent:.4f} bits, total {ent*l:.2f} bits")
        self.ev_out.setPlainText("\n".join(lines))

    # update_texts for translations (called by app refresh)
    def update_texts(self):
        # Update window title and tool names; labels in panels are not all dynamic here,
        # but frequently-used buttons/titles are updated.
        self.setWindowTitle(f"{tr('tools')} - Luxxer (educational)")
        # update list
        for i, name in enumerate(self.tool_names):
            item = self.tool_list.item(i)
            if item:
                item.setText(tr(name))
        self.hash_btn.setText(tr("run"))

# GuardianAV (scanner)

class GuardianAVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GuardianAV - Luxxer')
        central = QWidget()
        layout = QVBoxLayout()
        self.scan_btn = QPushButton('Scan Virtual FS')
        self.scan_btn.clicked.connect(self.scan)
        self.progress = QProgressBar()
        self.out = QTextEdit()
        self.out.setReadOnly(True)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.out)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def scan(self):
        self.progress.setValue(0)
        self.out.clear()
        signatures = ['BAD_SIGNATURE', 'MALWARE', 'EICAR']
        # simulate scanning virtual fs
        entries = []
        def rec(node, path=''):
            for k,v in node.items():
                if isinstance(v, dict):
                    rec(v, f'{path}/{k}')
                else:
                    entries.append((f'{path}/{k}', v))
        rec(APP_STATE['files'])
        total = len(entries) or 1
        found = []
        for i, (p, content) in enumerate(entries):
            self.progress.setValue(int(100*(i+1)/total))
            self.out.append(f'Scanning {p}...')
            time.sleep(0.15)
            for sig in signatures:
                if sig in str(content):
                    self.out.append(f'Found signature {sig} in {p}!')
                    found.append((p,sig))
        if not found:
            self.out.append('No threats found in Virtual FS (mock scan).')
        else:
            self.out.append('Mock scan found items:')
            for p,sig in found:
                self.out.append(f' - {p}: {sig}')



# WinRAR (fake archiver)

class WinRarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WinRAR - Luxxer (fake)')
        central = QWidget()
        layout = QVBoxLayout()
        self.file_sel = QLineEdit()
        sel_btn = QPushButton('Select file')
        sel_btn.clicked.connect(self.select_file)
        arch_btn = QPushButton('Create Archive')
        arch_btn.clicked.connect(self.create_archive)
        layout.addWidget(self.file_sel)
        layout.addWidget(sel_btn)
        layout.addWidget(arch_btn)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def select_file(self):
        p, _ = QFileDialog.getOpenFileName(self, 'Select file')
        if p:
            self.file_sel.setText(p)

    def create_archive(self):
        src = self.file_sel.text().strip()
        if not src or not os.path.exists(src):
            QMessageBox.warning(self, 'Error', 'Select a valid local file to archive (this uses real filesystem).')
            return
        dest, _ = QFileDialog.getSaveFileName(self, 'Save archive', '', 'Zip Files (*.zip)')
        if not dest:
            return
        base = os.path.splitext(dest)[0]
        shutil.make_archive(base, 'zip', os.path.dirname(src), os.path.basename(src))
        QMessageBox.information(self, 'Done', 'Archive created (zip)')


# global state
APP_STATE = {}
APP_STATE.setdefault('settings', {'lang': 'en', 'username': 'user'})

class FilePreviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Preview')
        layout = QVBoxLayout()
        self.label = QLabel('Select a file from Explorer')
        layout.addWidget(self.label)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def preview_file(self, path: str):
        try:
            with open(path,'r',encoding='utf-8') as f:
                text = f.read(5000)  # limit preview size
            self.label.setText(text)
        except Exception as e:
            self.label.setText(f'Cannot preview: {e}')

# Main Desktop / Shell

try:
    from settings_utils import save_state
except Exception:
    save_state = None
try:
    APP_STATE
except NameError:
    APP_STATE = {'settings': {}}

def apply_theme_global(theme: str):
    qapp = QApplication.instance()
    if qapp is None:
        return
    theme = (theme or 'transparent').lower()
    if theme == 'dark':
        style = """
            QMainWindow { background-color: #121212; color: #fff; }
            QMdiSubWindow { background-color: #1e1e1e; color: #fff; border: 1px solid #444; }
            QPushButton, QToolButton { background-color: #2c2c2c; border-radius: 6px; color: #fff; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: #3c3c3c; }
        """
    elif theme == 'white':
        style = """
            QMainWindow { background-color: #ffffff; color: #000; }
            QMdiSubWindow { background-color: #ffffff; color: #000; border: 1px solid #e6e6e6; }
            QPushButton, QToolButton { background-color: #f0f0f0; border-radius: 6px; color: #000; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: #e8e8e8; }
        """
    else:
        style = """
            QMainWindow { background-color: transparent; color: #fff; }
            QMdiSubWindow { background-color: rgba(255,255,255,0.02); color: #fff; border: 1px solid rgba(255,255,255,0.04); }
            QPushButton, QToolButton { background-color: rgba(0,0,0,0.55); border-radius: 6px; color: #fff; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: rgba(0,0,0,0.65); }
        """
    qapp.setStyleSheet(style)


class SettingsApp(QMainWindow):
    def __init__(self, main_ref=None):
        super().__init__()
        self.main_ref = main_ref

        self.setWindowTitle("Settings - Luxxer")
        self.resize(480, 260)

        central = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Username
        self.label_username = QLabel("Username")
        self.username = QLineEdit(APP_STATE.get('settings', {}).get('username', 'user'))
        self.username.editingFinished.connect(self._on_username_change)

        # Theme selector
        self.label_theme = QLabel("Theme")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['transparent', 'white', 'dark'])
        current = APP_STATE.get('settings', {}).get('theme', 'transparent')
        if current in ['transparent', 'white', 'dark']:
            self.theme_combo.setCurrentText(current)
        self.theme_combo.currentTextChanged.connect(self._on_theme_change)

        # Save
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)
        btn_row.addWidget(self.save_btn)

        # assemble
        layout.addWidget(self.label_username)
        layout.addWidget(self.username)
        layout.addWidget(self.label_theme)
        layout.addWidget(self.theme_combo)
        layout.addStretch()
        layout.addLayout(btn_row)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # ensure defaults
        APP_STATE.setdefault('settings', {})
        APP_STATE['settings'].setdefault('theme', current)
        APP_STATE['settings'].setdefault('username', self.username.text().strip())

    def _on_username_change(self):
        APP_STATE.setdefault('settings', {})['username'] = self.username.text().strip()
        self._silent_save()

    def _on_theme_change(self, txt):
        APP_STATE.setdefault('settings', {})['theme'] = txt
        # apply immediately
        apply_theme_global(txt)
        self._silent_save()
        # if main_ref exposes helpers (e.g., to refresh wallpapers, etc.) call them:
        if self.main_ref is not None:
            try:
                if hasattr(self.main_ref, 'on_theme_changed'):
                    self.main_ref.on_theme_changed(txt)
            except Exception:
                pass

    def save(self):
        APP_STATE.setdefault('settings', {})['username'] = self.username.text().strip()
        APP_STATE.setdefault('settings', {})['theme'] = self.theme_combo.currentText()
        try:
            if save_state:
                save_state(APP_STATE)
            else:
                # fallback file write
                with open('app_state.json', 'w', encoding='utf-8') as f:
                    json.dump(APP_STATE, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Error saving state:", e)
        QMessageBox.information(self, "Settings saved", "Settings have been applied.")

    def _silent_save(self):
        try:
            if save_state:
                save_state(APP_STATE)
            else:
                with open('app_state.json', 'w', encoding='utf-8') as f:
                    json.dump(APP_STATE, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def update_texts(self):
        self.setWindowTitle("Settings - Luxxer")
        self.label_username.setText("Username")
        self.label_theme.setText("Theme")
        self.save_btn.setText("Save")

class Taskbar(QWidget):
    def __init__(self, main_ref):
        super().__init__()
        self.setObjectName('taskbar')
        self.main_ref = main_ref
        h = QHBoxLayout()
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.main_ref.toggle_start)
        h.addWidget(self.start_btn)
        h.addStretch()
        self.time_label = QLabel(time.strftime('%H:%M'))
        h.addWidget(self.time_label)
        self.setLayout(h)

    def update_time(self):
        self.time_label.setText(time.strftime('%H:%M'))

class ContactsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contacts - Luxxer")
        self.resize(500, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Header search
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search contacts...")
        self.search_bar.textChanged.connect(self.filter_contacts)
        self.layout.addWidget(self.search_bar)

        # Contacts list
        self.listw = QListWidget()
        self.layout.addWidget(self.listw)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add contact")
        self.add_btn.clicked.connect(self.add_contact)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete contact")
        self.delete_btn.clicked.connect(self.delete_contact)
        btn_layout.addWidget(self.delete_btn)

        self.layout.addLayout(btn_layout)

        # Sample contacts
        self.contacts = ["Alice <alice@example.local>", "Bob <bob@example.local>"]
        self.update_list()

    def update_list(self):
        self.listw.clear()
        for contact in self.contacts:
            self.listw.addItem(contact)

    def add_contact(self):
        name, ok = QInputDialog.getText(self, "Add Contact", "Name & Email:")
        if ok and name:
            self.contacts.append(name)
            self.update_list()

    def delete_contact(self):
        selected = self.listw.currentRow()
        if selected >= 0:
            confirm = QMessageBox.question(self, "Delete", f"Delete contact {self.contacts[selected]}?")
            if confirm == QMessageBox.StandardButton.Yes:
                self.contacts.pop(selected)
                self.update_list()

    def filter_contacts(self, text):
        self.listw.clear()
        for contact in self.contacts:
            if text.lower() in contact.lower():
                self.listw.addItem(contact)

class PhotosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photos - Luxxer")
        self.resize(800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Image display with scroll
        self.scroll_area = QScrollArea()
        self.label = QLabel("Photo gallery")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)
        self.layout.addWidget(self.scroll_area)

        # Buttons
        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open Image")
        self.open_btn.clicked.connect(self.open_image)
        btn_layout.addWidget(self.open_btn)

        self.clear_btn = QPushButton("Clear Image")
        self.clear_btn.clicked.connect(lambda: self.label.clear())
        btn_layout.addWidget(self.clear_btn)

        self.layout.addLayout(btn_layout)

        # Keep track of last opened image
        self.current_pixmap = None

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open image", "", "Images (*.png *.jpg *.bmp);;All Files (*)")
        if path:
            try:
                pix = QPixmap(path)
                self.current_pixmap = pix
                self.label.setPixmap(pix.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Cannot open image: {e}")


# Helper to create widget from arbitrary class safely

def instantiate_app_widget(app_class):
    """
    Given a class, try to instantiate and return a QWidget suitable
    for insertion into a QMdiSubWindow.
    If app_class is a QMainWindow subclass, try to take its centralWidget().
    If fails, wrap fallback content into a QWidget to avoid crash.
    """
    try:
        inst = app_class()
    except Exception as e:
        print(f"[instantiate_app_widget] Failed to instantiate {app_class}: {e}")
        traceback.print_exc()
        # fallback placeholder widget
        w = QWidget()
        l = QVBoxLayout(w)
        l.addWidget(QLabel(f"Failed to start {getattr(app_class, '__name__', str(app_class))}\nCheck logs."))
        return w

    # If it's a QMainWindow, try to extract centralWidget
    if isinstance(inst, QMainWindow):
        central = inst.centralWidget()
        if central is None:
            # wrap the QMainWindow contents into a QWidget placeholder (avoid adding QMainWindow into QMdiSubWindow)
            w = QWidget()
            l = QVBoxLayout(w)
            title = inst.windowTitle() or getattr(app_class, '__name__', 'App')
            l.addWidget(QLabel(f"{title}\n(MainWindow wrapper)"))
            return w
        else:
            # central widget exists -> reparent it safely
            # ensure it has no parent (setParent(None)) and return
            central.setParent(None)
            return central
    # If already a QWidget subclass, return it directly
    if isinstance(inst, QWidget):
        return inst

    # Otherwise wrap into QWidget
    w = QWidget()
    l = QVBoxLayout(w)
    l.addWidget(QLabel(str(inst)))
    return w

def create_placeholders(app_names):
    for name in app_names:
        # derive candidate class name (remove spaces/punct)
        class_base = ''.join(ch for ch in name if ch.isalnum())
        class_name = f"{class_base}App"

        if class_name in globals() and isinstance(globals()[class_name], type):
            # real class provided elsewhere — keep it
            continue

        # create placeholder widget class
        def make_init(disp):
            def __init__(self):
                super().__init__()
                self.setWindowTitle(disp)
                layout = QVBoxLayout(self)
                lbl = QLabel(f"{disp}\n(placeholder)")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setWordWrap(True)
                layout.addWidget(lbl)
                self.setMinimumSize(480, 320)
            return __init__

        new_cls = type(class_name, (QWidget,), {"__init__": make_init(name)})
        globals()[class_name] = new_cls
        print(f"[placeholder] Created {class_name} for '{name}'")

# create placeholder classes now (won't override real ones if present)
create_placeholders(APPS_LIST)

try:
    import screeninfo
except Exception:
    screeninfo = None


# ----------------- Helpers: save and run -----------------
def safe_save_text(parent, title: str, default_name: str, text: str):
    """
    Show save dialog and write text to file. Show message boxes on success/failure.
    """
    try:
        path, _ = QFileDialog.getSaveFileName(parent, title, default_name, "Text Files (*.txt);;All Files (*)")
        if not path:
            return None
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        QMessageBox.information(parent, "Saved", f"Saved to: {path}")
        return path
    except Exception as e:
        traceback.print_exc()
        QMessageBox.warning(parent, "Save failed", f"Failed to save: {e}")
        return None


def safe_run_command(parent, command: str, callback_stdout=None, shell=False):
    """
    Run an external command in a background thread and collect output.
    - command: string (will be shlex.split unless shell=True)
    - callback_stdout: optional callable(str) called with output (on finish)
    - shell: whether to run via shell (False recommended)
    Note: This will run arbitrary local commands. Use carefully.
    """

    def runner(cmd):
        try:
            if isinstance(cmd, str) and not shell:
                parts = shlex.split(cmd)
            else:
                parts = cmd
            # Popen with text mode to get str output
            proc = subprocess.Popen(parts, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=shell)
            out_lines = []
            # stream output while running
            for line in proc.stdout:
                out_lines.append(line)
            proc.wait()
            output = "".join(out_lines)
            if callback_stdout:
                try:
                    # call back on main thread via Qt: show via simple invocation
                    callback_stdout(output)
                except Exception:
                    print("[safe_run_command] callback failed")
            else:
                # fallback: show message box on main thread using queued call
                def show_result():
                    QMessageBox.information(parent, f"Command finished", output or "(no output)")
                try:
                    # if parent is a QWidget, use its thread to schedule; simple call is OK here
                    show_result()
                except Exception:
                    print("[safe_run_command] could not show result")
        except Exception as e:
            traceback.print_exc()
            try:
                QMessageBox.warning(parent, "Run failed", f"Failed to run command: {e}")
            except Exception:
                print("[safe_run_command] failed to report:", e)

    t = threading.Thread(target=runner, args=(command,), daemon=True)
    t.start()

# SafeApp

class SafeApp(QWidget):
    def __init__(self, app_name: str = "Unknown App"):
        try:
            super().__init__()
            self.app_name = app_name
            self.setWindowTitle(app_name)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)

            # Main label
            label = QLabel(f"{app_name}\n(Placeholder / SafeApp)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            layout.addWidget(label)

            info_label = QLabel("This application has not yet been implemented.\nAll SafeApp functions work safely.")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setWordWrap(True)
            layout.addWidget(info_label)

            self.setMinimumSize(480, 320)
        except Exception as e:
            print(f"[SafeApp] ERROR initializing SafeApp for '{app_name}': {e}")
            traceback.print_exc()
            try:
                fallback = QLabel(f"SafeApp failed to init for {app_name}")
                fallback.setAlignment(Qt.AlignmentFlag.AlignCenter)
                fallback.setWordWrap(True)
                fallback.setParent(self)
            except Exception:
                pass

# DockButton

class DockButton(QPushButton):
    def __init__(self, name, base_size=56):
        super().__init__(name[0].upper() if name else '?')
        self.full_name = name
        self.base_size = base_size
        self.current_size = self.base_size
        self.setFixedSize(base_size, base_size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setToolTip(name)
        self._apply_style(self.base_size)

    def _apply_style(self, size):
        font_px = max(10, int(size * 0.32))
        border_radius = int(size * 0.18)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #000;
                color: #fff;
                font-weight: 700;
                font-size: {font_px}px;
                border-radius: {border_radius}px;
                border: 0px;
            }}
            QPushButton:hover {{
                background-color: #222;
            }}
            QPushButton:pressed {{
                background-color: #111;
            }}
        """)

    def update_size(self, target_size, smooth=0.35):
        ns = int(self.current_size + (target_size - self.current_size) * smooth)
        if ns != self.current_size:
            self.current_size = ns
            self.setFixedSize(ns, ns)
            self._apply_style(ns)

# Bottom Dock

class BottomDock(QScrollArea):
    def __init__(self, main_ref, apps_list, base_btn_size=56, max_scale=1.8, influence=140, spacing=8):
        super().__init__()
        self.setObjectName('bottom_dock')

        self.main_ref = main_ref
        self.base_btn_size = base_btn_size
        self.max_scale = max_scale
        self.influence = influence
        self.spacing = spacing

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedHeight(self.base_btn_size + 20)

        self.container = QWidget()
        self.layout = QHBoxLayout(self.container)
        self.layout.setContentsMargins(10,6,10,6)
        self.layout.setSpacing(self.spacing)
        self.setWidget(self.container)

        self.buttons = []
        for name in apps_list:
            btn = DockButton(name, self.base_btn_size)
            btn.clicked.connect(lambda _, n=name: self._launch_safe(n))
            self.layout.addWidget(btn)
            btn.setMouseTracking(True)
            self.buttons.append(btn)

        self.setMouseTracking(True)
        self.container.setMouseTracking(True)
        self._last_pos = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start(16)

    def _launch_safe(self, name):
        try:
            if hasattr(self.main_ref, 'launch_app'):
                self.main_ref.launch_app(name)
        except Exception as e:
            print("[BottomDock] Launch exception:", e)
            traceback.print_exc()

    def enterEvent(self, ev):
        self._last_pos = self.mapFromGlobal(QCursor.pos())
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        self._last_pos = None
        super().leaveEvent(ev)

    def mouseMoveEvent(self, ev):
        try:
            gp = QCursor.pos()
            local = self.mapFromGlobal(gp)
            if 0 <= local.y() <= self.height() + self.influence:
                self._last_pos = local
            else:
                self._last_pos = None
        except Exception:
            self._last_pos = None
        super().mouseMoveEvent(ev)

    def wheelEvent(self, ev):
        delta = ev.angleDelta().y()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta)
        ev.accept()

    def _on_timer(self):
        if not self.buttons:
            return
        if self._last_pos is None:
            for b in self.buttons:
                b.update_size(self.base_btn_size, smooth=0.25)
            return

        px = self._last_pos.x()
        centers = [b.geometry().left() + b.width()//2 for b in self.buttons]
        two_sigma_sq = 2 * ((self.influence / 3) ** 2)

        for i, b in enumerate(self.buttons):
            dist = abs(px - centers[i])
            factor = math.exp(-(dist**2)/two_sigma_sq) if dist < self.influence*1.5 else 0.0
            factor = max(0.0, min(1.0, factor))
            target = int(self.base_btn_size + (self.base_btn_size*(self.max_scale-1)*factor))
            b.update_size(target, smooth=0.35)

# RealMain: main window hosting QMdiArea + Dock

class RealMain(QMainWindow):
    def __init__(self, apps_list=APPS_LIST):
        super().__init__()
        self.setWindowTitle("Luxxer OS")
        self.setWindowIcon(QIcon("MainIco.ico") if os.path.exists("MainIco.ico") else QIcon())
        self.resize(1200, 800)

        # QMdiArea (multitasking area)
        self.mdi = QMdiArea()
        self.mdi.setViewMode(QMdiArea.ViewMode.SubWindowView)
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # set background image on mdi if exists
        self._background_path = "MainScreenFinal.png"
        self._apply_mdi_background()

        # central layout: mdi above, dock below
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.mdi, 1)

        # create dock
        self.dock = BottomDock(self, apps_list)
        main_layout.addWidget(self.dock, 0)

        self.setCentralWidget(central)

        # build app_map using global classes or placeholders created earlier
        self.app_map = {}
        for name in apps_list:
            key = ''.join(ch for ch in name if ch.isalnum()) + "App"
            cls = globals().get(key)
            if isinstance(cls, type):
                self.app_map[name] = cls
            else:
                # fallback to placeholder Safe label wrapper (shouldn't happen because create_placeholders ran)
                self.app_map[name] = globals().get(key)  # may be None; instantiate_app_widget will handle
        self.open_apps = []

    def _apply_mdi_background(self):
        if not hasattr(self, "mdi"):
            return
        palette = self.mdi.palette()
        if os.path.exists(self._background_path):
            pixmap = QPixmap(self._background_path).scaled(
                self.mdi.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            brush = QBrush(pixmap)
            palette.setBrush(self.mdi.backgroundRole(), brush)
        self.mdi.setPalette(palette)
        self.mdi.setAutoFillBackground(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_mdi_background()

    def launch_app(self, name: str):
        name = name.strip()
        if name not in self.app_map:
            print(f"[RealMain] App '{name}' not in app_map, showing message.")
            QMessageBox.information(self, "Launch", f"App not implemented: {name}")
            return

        app_cls = self.app_map.get(name)
        if app_cls is None:
            # fallback safe widget
            app_widget = QLabel(f"{name} (missing class)"); app_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            try:
                # instantiate safely
                app_widget = instantiate_app_widget(app_cls)
            except Exception as e:
                print(f"[RealMain] Exception while instantiating {name}: {e}")
                traceback.print_exc()
                app_widget = QLabel(f"{name} (failed to instantiate)")
                app_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # now embed into MDI subwindow
        try:
            sub = QMdiSubWindow()
            sub.setWidget(app_widget)
            sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            sub.setWindowTitle(name)
            self.mdi.addSubWindow(sub)
            sub.show()
            self.open_apps.append(sub)
            print(f"[RealMain] Launched {name}")
        except Exception as e:
            print(f"[RealMain] Failed adding {name} to MDI: {e}")
            traceback.print_exc()
            QMessageBox.warning(self, "Launch error", f"Failed to launch {name}: {e}")

def animate_window_show(window: QMainWindow):
    window.setWindowOpacity(0.0)
    window.show()
    anim = QPropertyAnimation(window, b'windowOpacity')
    anim.setDuration(300)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    anim.start()
    # keep reference to prevent GC
    window._anim = anim

# simple placeholder app for rapid registration
class PlaceholderApp(QMainWindow):
    def __init__(self, title: str, desc: str = ""):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(640, 360)
        w = QWidget()
        l = QVBoxLayout()
        lbl = QLabel(f"<h2>{title}</h2><p>{desc}</p>")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(lbl)
        w.setLayout(l)
        self.setCentralWidget(w)

APP_MAPPING = {
    'Notebook': NotebookApp,
    'Paint': PaintApp,
    'Explorer': ExplorerApp,
    'LuxxerWeb': LuxxerWebApp,
    'Settings': lambda: SettingsApp(main_win) if 'main_win' in globals() else SettingsApp(None),
    "GamesApp": GamesApp,
    "ApplicationAdder": ApplicationAdder,
    'WinRAR': WinRarApp,
    'Zer3 IDE': Zer3IDE,
    'Calculator': CalculatorApp,
    'JokeGenerator': JokeGeneratorApp,
    'MotivationAIChat': MotivationAIChat,
    'RandomChallenge': RandomChallengeApp,
    'Cyber Tools': CyberToolsApp,
    'GuardianAV': GuardianAVApp,
    'CMD': CmdApp,
    'TaskManager': TaskManagerApp,
    'FilePreview': FilePreviewApp,
    'Calendar': CalendarApp,
    "Mail": MailApp,
    "Contacts": ContactsApp,
    "HackerSimulator": HackerSimulatorApp,
    "ASCIIPainter": ASCIIPainterApp,
    "FortuneTeller": FortuneTellerApp,
    "Photos": PhotosApp,
    "MusicPlayer": MusicPlayerApp,
    "VideoPlayer": VideoPlayerApp,
    "PDFReader": PDFReaderApp,
    "OfficeWriter": OfficeWriterApp,
    "Spreadsheet": SpreadsheetApp,
    "Presentation": PresentationApp,
    "StickyNotes": StickyNotesApp,
    "Screenshot": ScreenshotApp,
    "ScreenRecorder": ScreenRecorderApp,
    "ImageEditorPro": ImageEditorProApp,
    "VideoEditor": VideoEditorApp,
    "MediaConverter": MediaConverterApp,
    "TerminalEmulator": TerminalEmulatorApp,
    "ShellX": ShellXApp,
    "GitClient": GitClientApp,
    "DockerManager": DockerManagerApp,
    "PackageManager": PackageManagerApp,
    "AppStore": AppStoreApp,
    "BackupRestore": BackupRestoreApp,
    "DiskCleaner": DiskCleanerApp,
    "DiskManager": DiskManagerApp,
    "SystemInfo": SystemInfoApp,
    "DeviceManager": DeviceManagerApp,
    "PrinterManager": PrinterManagerApp,
    "NetworkMonitor": NetworkMonitorApp,
    "VPNClient": VPNClientApp,
    "RemoteDesktop": RemoteDesktopApp,
    "SSHClient": SSHClientApp,
    "PortScanner": PortScannerApp,
    "WiFiAnalyzer": WiFiAnalyzerApp,
    "ClipboardManager": ClipboardManagerApp,
    "Scheduler": SchedulerApp,
    "VoiceRecorder": VoiceRecorderApp,
    "HabitTracker": HabitTrackerApp,
    "Pomodoro": PomodoroApp,
    "RandomStory": RandomStoryApp,
    "TravelTips": TravelTipsApp,
    "QRCodeGenerator": QRCodeGeneratorApp,
    "ColorPalette": ColorPaletteApp,
    "RecipeBox": RecipeBoxApp,
    "BudgetTracker": BudgetTrackerApp,
    "TerminalGames": TerminalGamesApp,
    "AmbientSound": AmbientSoundApp,
    "ScreenOrganizer": ScreenOrganizerApp,
    "ThemePreview": ThemePreviewApp,
}

# Main Window

class MainWindow(QMainWindow):
    def __init__(self, APPS_LIST):
        super().__init__()
        self.setWindowTitle("Luxxer OS")
        self.resize(1280, 800)

        # MDI Area
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.wallpaper = QPixmap("MainScreenFinal.png")
        self.mdi.paintEvent = self._paint_background

        # BottomDock
        self.dock = BottomDock(self, APPS_LIST)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.mdi)
        layout.addWidget(self.dock)
        self.setCentralWidget(central)

        # Apps mapping (placeholder)
        self.app_map = {}
        for name in APPS_LIST:
            self.app_map[name] = lambda n=name: QLabel(f"{n} (Placeholder)")

        self.open_apps = []

    def _paint_background(self, event):
        painter = QPainter(self.mdi.viewport())
        if not self.wallpaper.isNull():
            painter.drawPixmap(self.mdi.rect(), self.wallpaper)

    def launch_app(self, app_name: str):
        if app_name in APP_MAPPING:
            app_class = APP_MAPPING[app_name]
            try:
                app_widget = app_class()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"I can't start it. '{app_name}': {e}")
                return

            sub = QMdiSubWindow()
            sub.setWidget(app_widget)
            sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            sub.setWindowTitle(app_name)

            self.mdi.addSubWindow(sub)
            sub.show()
        else:
            QMessageBox.warning(self, "Error", f"App '{app_name}' does not exist!")


    # Animation
    def animate_window_show(self, sub):
        sub.setMinimumSize(0, 0)
        geom = sub.geometry()
        start_geom = QRect(geom.center().x(), geom.center().y(), 0, 0)

        anim = QPropertyAnimation(sub, b"geometry")
        anim.setDuration(400)
        anim.setStartValue(start_geom)
        anim.setEndValue(geom)
        anim.setEasingCurve(QEasingCurve.Type.OutBack)

        sub.setGeometry(start_geom)
        anim.start()
        sub._anim = anim


# MAIN
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QDialog
    from Luxxer_OS_Start import StartScreen, apply_theme_global
    from settings_utils import load_state

    APP_STATE = load_state() or {}
    APP_STATE.setdefault('settings', {})

    app = QApplication(sys.argv)

    apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))

    start = StartScreen(app, APP_STATE)
    if start.exec() == QDialog.DialogCode.Accepted:
        main_win = MainWindow(APPS_LIST)
        apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))
        main_win.showFullScreen()
        sys.exit(app.exec())
    else:
        sys.exit(0)