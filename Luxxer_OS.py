import sys
import os
import io
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
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple

import urllib.request

try:
    import psutil
except Exception:
    psutil = None

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    from moviepy.editor import VideoFileClip
except Exception:
    VideoFileClip = None

warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QRegularExpression, QPropertyAnimation,
    QRect, QEasingCurve, QPoint, QSize, QMimeData, QUrl
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QPainter, QPen, QColor, QAction, QTextCharFormat,
    QFont, QSyntaxHighlighter, QCursor, QGuiApplication, QMouseEvent, QImage, QDrag
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QLineEdit,
    QTreeWidget, QTreeWidgetItem, QColorDialog, QInputDialog, QProgressBar, QSplitter,
    QFrame, QMenu, QComboBox, QGridLayout, QDockWidget, QSpinBox, QCheckBox,
    QMdiArea, QMdiSubWindow, QScrollArea, QSizePolicy, QMenuBar, QTableWidget,
    QTableWidgetItem, QSlider, QDialog, QTabWidget, QToolBar, QPlainTextEdit, QCalendarWidget,
)
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

try:
    from PyQt6.QtPdfWidgets import QPdfView
    from PyQt6.QtPdf import QPdfDocument
    QT_PDF_AVAILABLE = True
except Exception:
    QPdfView = None
    QPdfDocument = None
    QT_PDF_AVAILABLE = False

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineProfile
    WEBENGINE_AVAILABLE = True
except Exception:
    QWebEngineView = None
    QWebEngineProfile = None
    WEBENGINE_AVAILABLE = False

try:
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
    MEDIA_AVAILABLE = True
except Exception:
    MEDIA_AVAILABLE = False

try:
    from cryptography.fernet import Fernet, InvalidToken
    CRYPTO_AVAILABLE = True
except Exception:
    Fernet = None
    CRYPTO_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except Exception:
    pytesseract = None
    Image = None
    OCR_AVAILABLE = False

from iconadderonmainscreen import IconAdderAreaMarquee
from BSOD import run_with_bsod, install_global_handlers

try:
    from start_menu_file import StartMenu
except Exception:
    StartMenu = None

try:
    from Luxxer_OS_Start import StartScreen, apply_theme_global
except Exception:
    StartScreen = None
    apply_theme_global = None

try:
    from games_all import GamesApp
except Exception:
    GamesApp = None

try:
    from applicationadder import ApplicationAdder
except Exception:
    ApplicationAdder = None

def _safe_import(name):
    try:
        module = __import__(name)
        return module
    except Exception:
        return None

RandomChallengeApp = _safe_import("RandomChallenge").RandomChallengeApp if _safe_import("RandomChallenge") else None
MotivationAIChat = _safe_import("MotivationAIChat").MotivationAIChat if _safe_import("MotivationAIChat") else None
JokeGeneratorApp = _safe_import("JokeGenerator").JokeGeneratorApp if _safe_import("JokeGenerator") else None

try:
    from apps_extra3 import (
        WebBrowserApp, BrowserTab, TabbedBrowserApp, IncognitoBrowserApp, ReaderModeBrowserApp,
        RSSFeedReaderApp, LocalNotesApp, SecureVaultLiteApp, ImageGalleryApp,
        BatchImageResizerApp, AudioPlayerProApp, VideoStreamPlayerApp, JSONInspectorApp,
        CSVEditorProApp, SQLiteBrowserApp, APIRequesterApp, AutomationScriptApp, OCRToolApp,
        PodcastManagerApp, EpubReaderApp, ColorGradingApp, FontPreviewerApp, IconSetManagerApp,
        ClipStackApp, WindowTilerApp, DesktopSpacesApp, NetworkSpeedTesterApp, FocusTimerApp,
        PasswordGeneratorApp, WallpapersManagerApp
    )
except Exception:
    WebBrowserApp = TabbedBrowserApp = IncognitoBrowserApp = ReaderModeBrowserApp = None
    RSSFeedReaderApp = LocalNotesApp = SecureVaultLiteApp = ImageGalleryApp = None
    BatchImageResizerApp = AudioPlayerProApp = VideoStreamPlayerApp = JSONInspectorApp = None
    CSVEditorProApp = SQLiteBrowserApp = APIRequesterApp = AutomationScriptApp = None
    OCRToolApp = PodcastManagerApp = EpubReaderApp = ColorGradingApp = None
    FontPreviewerApp = IconSetManagerApp = ClipStackApp = WindowTilerApp = None
    DesktopSpacesApp = NetworkSpeedTesterApp = FocusTimerApp = None
    PasswordGeneratorApp = WallpapersManagerApp = None

try:
    from apps_extra import HackerSimulatorApp, ASCIIPainterApp, FortuneTellerApp
except Exception:
    HackerSimulatorApp = ASCIIPainterApp = FortuneTellerApp = None

try:
    from apps_extra2 import (
        HabitTrackerApp, PomodoroApp, RandomStoryApp, TravelTipsApp,
        QRCodeGeneratorApp, ColorPaletteApp, RecipeBoxApp, BudgetTrackerApp,
        TerminalGamesApp, AmbientSoundApp, ScreenOrganizerApp, ThemePreviewApp
    )
except Exception:
    HabitTrackerApp = PomodoroApp = RandomStoryApp = TravelTipsApp = None
    QRCodeGeneratorApp = ColorPaletteApp = RecipeBoxApp = None
    BudgetTrackerApp = TerminalGamesApp = AmbientSoundApp = None
    ScreenOrganizerApp = ThemePreviewApp = None

try:
    from settings_utils import save_state, load_state
except Exception:
    save_state = load_state = None

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

APPS_LIST = [
    'Notebook','Paint','Explorer','WebBrowser','Settings','WinRAR','Zer3 IDE','Calculator',
    'Cyber Tools','GuardianAV','CMD','RandomChallenge', 'MotivationAIChat', 'JokeGenerator',
    'TaskManager','FilePreview','Calendar', 'HackerSimulator', 'ASCIIPainter', 'FortuneTeller',
    'Mail','Contacts','Photos','MusicPlayer','VideoPlayer','PDFReader','OfficeWriter',
    'Spreadsheet','Presentation','StickyNotes','Screenshot','ScreenRecorder',
    'ImageEditorPro','VideoEditor','MediaConverter','TerminalEmulator','ShellX','GitClient',
    'DockerManager','PackageManager','AppStore','BackupRestore','DiskCleaner','DiskManager',
    'SystemInfo','DeviceManager','PrinterManager','LuxxerWeb', 'NetworkMonitor','VPNClient','RemoteDesktop',
    'SSHClient','PortScanner','WiFiAnalyzer','ClipboardManager','Scheduler','VoiceRecorder',
    'GamesApp', 'ApplicationAdder', 'HabitTracker', 'Pomodoro', 'RandomStory', 'TravelTips',
    'QRCodeGenerator', 'ColorPalette', 'RecipeBox', 'BudgetTracker',
    'TerminalGames', 'AmbientSound', 'ScreenOrganizer', 'ThemePreview',
    'WebBrowser','TabbedBrowser','IncognitoBrowser','ReaderModeBrowser',
    'RSSFeedReader','LocalNotes','SecureVaultLite','ImageGallery','BatchImageResizer',
    'AudioPlayerPro','VideoStreamPlayer','JSONInspector','CSVEditorPro','SQLiteBrowser',
    'APIRequester','AutomationScript','OCRTool','PodcastManager','EpubReader','ColorGrading',
    'FontPreviewer','IconSetManager','ClipStack','WindowTiler','DesktopSpaces',
    'NetworkSpeedTester','FocusTimer','PasswordGenerator','WallpapersManager',
]

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MusicPlayer - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.player = QMediaPlayer(parent=self)
        self.audio_output = QAudioOutput(parent=self)
        self.player.setAudioOutput(self.audio_output)
        try:
            self.player.setVideoOutput(self.video_widget)
        except Exception:
            pass

        self.current_video = None

        try:
            self.player.playbackStateChanged.connect(self._on_playback_state_changed)
        except Exception:
            pass
        try:
            self.player.mediaStatusChanged.connect(self._on_media_status_changed)
        except Exception:
            pass
        try:
            self.player.errorOccurred.connect(self._on_error)
        except Exception:
            pass

    def open_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Video (*.mp4 *.mkv *.avi *.mov *.webm);;All Files (*)")
        if not path:
            return
        if not os.path.exists(path):
            QMessageBox.warning(self, "Open video", "Selected file does not exist.")
            return

        url = QUrl.fromLocalFile(path)
        try:
            self.player.setSource(url)
            self.current_video = path
            self.player.stop()
            self.status.setText(f"Loaded: {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Open video", f"Failed to load video:\n{e}")
            self.current_video = None

    def play(self):
        if not self.current_video:
            QMessageBox.information(self, "Play", "No video loaded. Use 'Open Video' first.")
            return
        try:
            self.player.play()
            self.status.setText(f"Playing: {os.path.basename(self.current_video)}")
        except Exception as e:
            QMessageBox.critical(self, "Play", f"Failed to play:\n{e}")

    def pause(self):
        try:
            self.player.pause()
            self.status.setText("Paused")
        except Exception as e:
            QMessageBox.critical(self, "Pause", f"Failed to pause:\n{e}")

    def stop(self):
        try:
            self.player.stop()
            self.status.setText("Stopped")
        except Exception as e:
            QMessageBox.critical(self, "Stop", f"Failed to stop:\n{e}")

    def _on_playback_state_changed(self, state):
        # QMediaPlayer.PlaybackState enum: PlayingState, PausedState, StoppedState
        try:
            if state == QMediaPlayer.PlaybackState.PlayingState:
                if self.current_video:
                    self.status.setText(f"Playing: {os.path.basename(self.current_video)}")
                else:
                    self.status.setText("Playing")
            elif state == QMediaPlayer.PlaybackState.PausedState:
                self.status.setText("Paused")
            else:
                self.status.setText("Stopped")
        except Exception:
            pass

    def _on_media_status_changed(self, status):
        try:
            if status == QMediaPlayer.MediaStatus.LoadedMedia:
                if self.current_video:
                    self.status.setText(f"Loaded: {os.path.basename(self.current_video)}")
                else:
                    self.status.setText("Loaded")
            elif status == QMediaPlayer.MediaStatus.InvalidMedia:
                self.status.setText("Invalid media")
        except Exception:
            pass

    def _on_error(self, err, msg=""):
        try:
            text = msg or (getattr(self.player, "errorString", lambda: "")() or "Unknown error")
            QMessageBox.critical(self, "Playback error", f"Error: {text}")
            self.status.setText("Error")
        except Exception:
            pass

class PDFReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFReader - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(700, 500)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # status label
        self.status = QLabel("No PDF loaded")
        self.layout.addWidget(self.status)

        if not QT_PDF_AVAILABLE:
            warn = QLabel(
                "QtPdf module is not available in this environment.\n"
                "Install PyQt6 with QtPdf support (or platform codecs) to enable PDF viewing."
            )
            warn.setWordWrap(True)
            self.layout.addWidget(warn)

            self.open_btn = QPushButton("Open PDF (will check availability)")
            self.open_btn.clicked.connect(self._open_pdf_check)
            self.layout.addWidget(self.open_btn)
            self.pdf_doc = None
            self.pdf_view = None
            self.current_path: Optional[str] = None
            return

        self.pdf_doc = QPdfDocument(self)
        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.pdf_doc)
        self.layout.addWidget(self.pdf_view)

        # controls: open + navigation + zoom
        ctrl_row = QHBoxLayout()
        self.open_btn = QPushButton("Open PDF")
        self.open_btn.clicked.connect(self.open_pdf)
        ctrl_row.addWidget(self.open_btn)

        self.prev_btn = QPushButton("Prev")
        self.prev_btn.clicked.connect(self.prev_page)
        ctrl_row.addWidget(self.prev_btn)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_page)
        ctrl_row.addWidget(self.next_btn)

        ctrl_row.addStretch()

        self.zoom_label = QLabel("Zoom:")
        ctrl_row.addWidget(self.zoom_label)

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(10, 400)  # percent
        self.zoom_slider.setValue(100)
        self.zoom_slider.setSingleStep(10)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        ctrl_row.addWidget(self.zoom_slider)

        self.layout.addLayout(ctrl_row)

        # state
        self.current_path: Optional[str] = None
        self.current_page = 0
        self._apply_zoom_percent(100)

        try:
            self.pdf_doc.statusChanged.connect(self._on_doc_status_changed)
        except Exception:
            pass
        try:
            self.pdf_doc.errorOccurred.connect(self._on_doc_error)
        except Exception:
            pass

    # Fallback open (samo info)
    def _open_pdf_check(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if not path:
            return
        QMessageBox.warning(self, "QtPdf missing",
                            "QtPdf module is not available in this Python build.\n"
                            f"Selected file: {os.path.basename(path)}\n"
                            "Install PyQt6 with QtPdf support (or use a platform build with Qt Pdf) to view it.")

    # Public open used when QtPdf
    def open_pdf(self):
        if not QT_PDF_AVAILABLE:
            self._open_pdf_check()
            return

        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if not path:
            return

        if not os.path.exists(path):
            QMessageBox.warning(self, "Open PDF", "Selected file does not exist.")
            return

        try:
            load_result = self.pdf_doc.load(path)
            self.current_path = path
            status = getattr(self.pdf_doc, "status", lambda: None)()
            page_count = self.pdf_doc.pageCount()
            if page_count <= 0:
                QMessageBox.warning(self, "Open PDF", "Failed to load PDF or document has zero pages.")
                self.status.setText("Failed to load PDF")
                self.current_path = None
                return

            self.current_page = 0
            self.pdf_view.setPage(self.current_page)
            self.status.setText(f"Loaded: {os.path.basename(path)} ({page_count} pages)")
        except Exception as e:
            QMessageBox.critical(self, "Open PDF", f"Failed to load PDF:\n{e}")
            self.current_path = None

    def prev_page(self):
        if not QT_PDF_AVAILABLE or not self.pdf_doc:
            return
        if self.pdf_doc.pageCount() <= 0:
            return
        if self.current_page > 0:
            self.current_page -= 1
            self.pdf_view.setPage(self.current_page)
            self._update_status_page_info()

    def next_page(self):
        if not QT_PDF_AVAILABLE or not self.pdf_doc:
            return
        cnt = self.pdf_doc.pageCount()
        if cnt <= 0:
            return
        if self.current_page < cnt - 1:
            self.current_page += 1
            self.pdf_view.setPage(self.current_page)
            self._update_status_page_info()

    def _update_status_page_info(self):
        cnt = self.pdf_doc.pageCount() if QT_PDF_AVAILABLE and self.pdf_doc else 0
        self.status.setText(f"Loaded: {os.path.basename(self.current_path) if self.current_path else '—'} "
                            f" (page {self.current_page+1}/{cnt})" if cnt else "No PDF loaded")

    def _on_zoom_changed(self, val: int):
        # val je percent
        self._apply_zoom_percent(val)

    def _apply_zoom_percent(self, percent: int):
        try:
            # zoom factor: 1.0 == 100%
            factor = percent / 100.0
            if hasattr(self.pdf_view, "setZoomFactor"):
                self.pdf_view.setZoomFactor(factor)
            else:
                pass
        except Exception:
            pass

    # doc signals
    def _on_doc_status_changed(self, status):
        try:
            cnt = self.pdf_doc.pageCount()
            if cnt > 0:
                self.current_page = 0
                self.pdf_view.setPage(self.current_page)
                self.status.setText(f"Loaded: {os.path.basename(self.current_path)} ({cnt} pages)")
        except Exception:
            pass

    def _on_doc_error(self, err):
        try:
            QMessageBox.critical(self, "PDF error", f"Document error: {err}")
            self.status.setText("Error loading PDF")
        except Exception:
            pass

class OfficeWriterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OfficeWriter - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(700, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.label = QLabel("Video Editor - Load and Trim")
        self.layout.addWidget(self.label)

        self.load_btn = QPushButton("Load Video")
        self.load_btn.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_btn)

        trim_layout = QHBoxLayout()
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 9999)
        self.start_spin.setPrefix("Start: ")
        self.end_spin = QSpinBox()
        self.end_spin.setRange(0, 9999)
        self.end_spin.setPrefix("End: ")

        trim_layout.addWidget(self.start_spin)
        trim_layout.addWidget(self.end_spin)

        self.layout.addLayout(trim_layout)

        self.trim_btn = QPushButton("Trim and Save")
        self.trim_btn.clicked.connect(self.trim_video)
        self.layout.addWidget(self.trim_btn)

        self.clip = None
        self.video_path = ""

    def load_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Videos (*.mp4 *.mkv *.avi *.mov)")
        if path:
            self.video_path = path
            self.clip = VideoFileClip(path)
            self.start_spin.setMaximum(int(self.clip.duration))
            self.end_spin.setMaximum(int(self.clip.duration))
            self.label.setText(f"Loaded: {os.path.basename(path)} | Duration: {int(self.clip.duration)}s")

    def trim_video(self):
        if self.clip:
            start = self.start_spin.value()
            end = self.end_spin.value()

            if start >= end or end > self.clip.duration:
                QMessageBox.warning(self, "Error", "Invalid trim range.")
                return

            trimmed = self.clip.subclip(start, end)

            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save trimmed video", os.path.join(os.path.dirname(self.video_path), "trimmed.mp4"),
                "Videos (*.mp4)"
            )

            if save_path:
                trimmed.write_videofile(save_path)
                QMessageBox.information(self, "Saved", f"Trimmed video saved:\n{save_path}")
        else:
            QMessageBox.warning(self, "Error", "Load a video first.")

class ImageEditorProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageEditorPro - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.img_label = QLabel("No image loaded")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.img_label)

        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        btn_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("Save Image As")
        self.save_btn.clicked.connect(self.save_image)
        btn_layout.addWidget(self.save_btn)

        self.layout.addLayout(btn_layout)

        edit_layout = QHBoxLayout()

        self.rotate_left_btn = QPushButton("Rotate Left")
        self.rotate_left_btn.clicked.connect(lambda: self.rotate(-90))
        edit_layout.addWidget(self.rotate_left_btn)

        self.rotate_right_btn = QPushButton("Rotate Right")
        self.rotate_right_btn.clicked.connect(lambda: self.rotate(90))
        edit_layout.addWidget(self.rotate_right_btn)

        self.grayscale_btn = QPushButton("Grayscale")
        self.grayscale_btn.clicked.connect(self.to_grayscale)
        edit_layout.addWidget(self.grayscale_btn)

        self.resize_btn = QPushButton("Resize (50%)")
        self.resize_btn.clicked.connect(self.resize_half)
        edit_layout.addWidget(self.resize_btn)

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo)
        edit_layout.addWidget(self.undo_btn)

        self.layout.addLayout(edit_layout)

        self.current_image = None
        self.history = []  # lista za undo

    def push_history(self):
        if self.current_image:
            self.history.append(self.current_image.copy())

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.current_image = QPixmap(path)
            self.history.clear()
            self.update_preview()

    def save_image(self):
        if self.current_image:
            path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPG (*.jpg)")
            if path:
                self.current_image.save(path)
                QMessageBox.information(self, "Saved", f"Image saved to {path}")

    def update_preview(self):
        if self.current_image:
            self.img_label.setPixmap(self.current_image.scaled(
                self.img_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def rotate(self, angle):
        if self.current_image:
            self.push_history()
            transform = self.current_image.transformed(
                QtGui.QTransform().rotate(angle)
            )
            self.current_image = transform
            self.update_preview()

    def to_grayscale(self):
        if self.current_image:
            self.push_history()
            image = self.current_image.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
            self.current_image = QPixmap.fromImage(image)
            self.update_preview()

    def resize_half(self):
        if self.current_image:
            self.push_history()
            w = self.current_image.width() // 2
            h = self.current_image.height() // 2
            self.current_image = self.current_image.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
            self.update_preview()

    def undo(self):
        if self.history:
            self.current_image = self.history.pop()
            self.update_preview()

class MediaConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediaConverter - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Media File",
            "",
            "All Media Files (*.mp4 *.mp3 *.wav *.avi *.mkv)"
        )
        if path:
            self.media_path = path
            self.info_label.setText(f"Loaded: {os.path.basename(path)}")

    def convert_media(self):
        if self.media_path:
            QMessageBox.information(
                self,
                "Convert",
                f"Conversion would run on {os.path.basename(self.media_path)} (demo)"
            )
        else:
            QMessageBox.warning(self, "Error", "No media loaded")

class TerminalEmulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TerminalEmulator - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 250)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.repo_path = QLineEdit()
        self.repo_path.setPlaceholderText("Enter repository path")
        self.layout.addWidget(QLabel("Repository Path:"))
        self.layout.addWidget(self.repo_path)

        self.status_btn = QPushButton("Git Status")
        self.status_btn.clicked.connect(self.status)
        self.layout.addWidget(self.status_btn)

        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Enter commit message")
        self.layout.addWidget(self.commit_msg)

        self.commit_btn = QPushButton("Commit Changes")
        self.commit_btn.clicked.connect(self.commit)
        self.layout.addWidget(self.commit_btn)

        self.push_btn = QPushButton("Push to Remote")
        self.push_btn.clicked.connect(self.push)
        self.layout.addWidget(self.push_btn)

    def status(self):
        path = self.repo_path.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Invalid repository path")
            return
        try:
            result = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
            QMessageBox.information(self, "Git Status", result.stdout or result.stderr)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Git error: {e}")

    def commit(self):
        path = self.repo_path.text().strip()
        msg = self.commit_msg.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Invalid repository path")
            return
        if not msg:
            QMessageBox.warning(self, "Error", "Commit message is empty")
            return
        try:
            subprocess.run(["git", "-C", path, "add", "."], check=True)
            subprocess.run(["git", "-C", path, "commit", "-m", msg], check=True)
            QMessageBox.information(self, "Commit", "Commit successful!")
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Commit failed: {e}")

    def push(self):
        path = self.repo_path.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Invalid repository path")
            return
        try:
            result = subprocess.run(["git", "-C", path, "push"], capture_output=True, text=True)
            QMessageBox.information(self, "Push Result", result.stdout or result.stderr)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Push failed: {e}")

class DockerManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DockerManager - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("DockerManager: Manage local containers in real-time")
        self.layout.addWidget(self.info_label)

        self.container_list = QListWidget()
        self.layout.addWidget(self.container_list)

        self.load_btn = QPushButton("Load Containers")
        self.load_btn.clicked.connect(self.load_containers)
        self.layout.addWidget(self.load_btn)

        self.start_btn = QPushButton("Start Selected")
        self.start_btn.clicked.connect(self.start_container)
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Selected")
        self.stop_btn.clicked.connect(self.stop_container)
        self.layout.addWidget(self.stop_btn)

        self.rm_btn = QPushButton("Remove Selected")
        self.rm_btn.clicked.connect(self.remove_container)
        self.layout.addWidget(self.rm_btn)

    def load_containers(self):
        try:
            result = subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True)
            containers = result.stdout.strip().splitlines()
            self.container_list.clear()
            self.container_list.addItems(containers if containers else ["No containers found"])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Docker error: {e}")

    def start_container(self):
        selected = self.container_list.currentItem()
        if selected:
            name = selected.text()
            try:
                subprocess.run(["docker", "start", name], check=True)
                QMessageBox.information(self, "Start", f"Container '{name}' started")
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, "Error", f"Failed to start: {e}")

    def stop_container(self):
        selected = self.container_list.currentItem()
        if selected:
            name = selected.text()
            try:
                subprocess.run(["docker", "stop", name], check=True)
                QMessageBox.information(self, "Stop", f"Container '{name}' stopped")
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, "Error", f"Failed to stop: {e}")

    def remove_container(self):
        selected = self.container_list.currentItem()
        if selected:
            name = selected.text()
            try:
                subprocess.run(["docker", "rm", name], check=True)
                QMessageBox.information(self, "Remove", f"Container '{name}' removed")
                self.load_containers()
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, "Error", f"Failed to remove: {e}")

class PackageManagerApp(QMainWindow):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, int)
    enable_buttons_signal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PackageManager - Luxxer")
        try:
            self.setWindowIcon(QIcon('icon.ico'))
        except Exception:
            pass
        self.resize(800, 600)

        self.log_signal.connect(self._append_log)
        self.finished_signal.connect(self._on_finished)
        self.enable_buttons_signal.connect(self._set_buttons_enabled)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Local Package Manager: install/update Python packages")
        self.layout.addWidget(self.info_label)

        # filter/search box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter packages (type to filter)...")
        self.search_box.textChanged.connect(self.filter_packages)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_box)
        self.layout.addLayout(search_layout)

        self.pkg_list = QListWidget()
        self.pkg_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.pkg_list)

        # control buttons
        btn_layout = QHBoxLayout()
        self.install_btn = QPushButton("Install Selected")
        self.install_btn.clicked.connect(self.install_pkg)
        btn_layout.addWidget(self.install_btn)

        self.update_btn = QPushButton("Update Selected")
        self.update_btn.clicked.connect(self.update_pkg)
        btn_layout.addWidget(self.update_btn)

        self.random_btn = QPushButton("Install Random")
        self.random_btn.clicked.connect(self.install_random)
        btn_layout.addWidget(self.random_btn)

        self.install_all_btn = QPushButton("Install All (careful)")
        self.install_all_btn.clicked.connect(self.install_all_prompt)
        btn_layout.addWidget(self.install_all_btn)

        self.layout.addLayout(btn_layout)

        # output log
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

        # prepare package list: real popular libs + placeholders to reach 500
        real_packages = [
            "requests","numpy","pandas","pyqt6","matplotlib","scipy","sympy","seaborn","sqlalchemy","flask",
            "django","fastapi","pydantic","typer","click","jupyter","notebook","ipython","ipykernel","tensorflow",
            "torch","torchvision","torchaudio","keras","scikit-learn","xgboost","lightgbm","catboost","transformers","huggingface_hub",
            "sentence-transformers","nltk","spacy","gensim","plotly","bokeh","dash","altair","folium","networkx",
            "graphviz","scapy","impacket","cryptography","paramiko","fabric","pycryptodome","pyjwt","requests-ntlm","sqlmap",
            "beautifulsoup4","lxml","html5lib","scrapy","selenium","playwright","boto3","google-cloud-storage","google-cloud-bigquery","azure-storage-blob",
            "docker","kubernetes","ansible","pytest","tox","coverage","hypothesis","kivy","wxpython","dearpygui",
            "tqdm","rich","colorama","loguru","faker","arrow","pendulum","dateparser","pytz","pyyaml",
            "toml","configparser","sh","fire","python-socketio","websockets","aiohttp","httpx","twisted","requests-html",
            "psycopg2","mysql-connector-python","pymongo","redis","cassandra-driver","tinydb","pillow","opencv-python","imageio","moviepy",
            "pydub","mutagen","pdfplumber","reportlab","pymupdf","pypdf2","dask","pyspark","vaex","modin",
            "mediapipe","onnxruntime","openai","stable-baselines3","fastapi-socketio","flask-socketio","email-validator","markdown","mistune","geopy",
            "shapely","pyproj","rtree","osmnx","s3fs","fsspec","smart-open","ujson","orjson","orator",
            "peewee","alembic","dataset","sqlalchemy-utils","greenlet","gevent","eventlet","sentry-sdk","prometheus-client","opentelemetry-api",
            "opentelemetry-sdk","pytest-cov","pyinstaller","cx_Freeze","nuitka","py2exe","cffi","cython","numba","llvmlite",
            "shap","lime","eli5","yellowbrick","mlflow","neptune-client","sacred","comet-ml","wandb","sklearn-pandas",
            "imbalanced-learn","category_encoders","featuretools","tsfresh","prophet","neuralprophet","pmdarima","statsmodels","librosa","soundfile",
            "pytorch-lightning","optuna","ray","gym","stable-baselines","pybullet","open3d","trimesh","pyvista","vedo",
            "tweepy","python-twitter","facebook-sdk","slack-sdk","python-telegram-bot","discord.py","aiofiles","asgiref","uvicorn","gunicorn",
            "black","isort","flake8","pylint","mypy","pre-commit","ruff","bandit","safety","requests-toolbelt",
            "paramiko","netmiko","nmap","python-nmap","mitmproxy","yara-python","pefile","capstone","lief","unicorn",
            "psutil","memory-profiler","line-profiler","profiling","pyinstrument","pympler","objgraph","boto","minio",
            "google-auth","oauthlib","requests-oauthlib","twilio","stripe","paypalrestsdk","pyOpenSSL","certifi",
            "brotli","lz4","zstandard","cryptography-fernet","asn1crypto","pyasn1","bcrypt","argon2-cffi"
        ]

        extras_needed = 500 - len(real_packages)
        extra_packages = [f"extra_pkg_{i+1}" for i in range(extras_needed)]
        self.packages = real_packages + extra_packages

        # populate QListWidget
        self.pkg_list.addItems(self.packages)

    # slot used by log_signal
    def _append_log(self, text: str):
        # append text preserving previous content
        self.log.append(text)

    # slot used at worker finish
    def _on_finished(self, friendly_action: str, returncode: int):
        if returncode == 0:
            self._append_log(f"{friendly_action} succeeded.")
            QMessageBox.information(self, friendly_action, f"{friendly_action} succeeded.")
        else:
            self._append_log(f"{friendly_action} failed (exit {returncode}).")
            QMessageBox.warning(self, friendly_action, f"{friendly_action} failed. See log.")
        # enable buttons again
        self._set_buttons_enabled(True)

    def filter_packages(self, text: str):
        text = text.lower().strip()
        self.pkg_list.clear()
        if not text:
            self.pkg_list.addItems(self.packages)
            return
        filtered = [p for p in self.packages if text in p.lower()]
        self.pkg_list.addItems(filtered)

    def run_pip_command(self, args, friendly_action):
        # disable buttons in main thread before starting worker
        self._set_buttons_enabled(False)

        def target():
            cmd = [sys.executable, "-m", "pip"] + args
            # emit running command
            self.log_signal.emit(f"> Running: {' '.join(cmd)}")
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True)
                out = (proc.stdout or "").strip()
                err = (proc.stderr or "").strip()

                if out:
                    self.log_signal.emit(out)
                if err:
                    self.log_signal.emit(err)
                # notify finish (main thread will handle QMessageBox)
                self.finished_signal.emit(friendly_action, proc.returncode)
            except Exception as e:
                self.log_signal.emit(f"Exception while running pip: {e}")
                self.finished_signal.emit(friendly_action, -1)

        t = threading.Thread(target=target, daemon=True)
        t.start()

    def install_pkg(self):
        selected = self.pkg_list.currentItem()
        if not selected:
            QMessageBox.information(self, "Install", "No package selected.")
            return
        pkg = selected.text()
        self.run_pip_command(["install", pkg], f"Install {pkg}")

    def update_pkg(self):
        selected = self.pkg_list.currentItem()
        if not selected:
            QMessageBox.information(self, "Update", "No package selected.")
            return
        pkg = selected.text()
        self.run_pip_command(["install", "--upgrade", pkg], f"Update {pkg}")

    def install_random(self):
        pkg = random.choice(self.packages)
        confirm = QMessageBox.question(self, "Install Random", f"Install random package: {pkg} ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.run_pip_command(["install", pkg], f"Install {pkg}")

    def install_all_prompt(self):
        reply = QMessageBox.warning(
            self, "Install All",
            "This will try to install ALL 500 packages (can be slow / heavy). Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # warning done on main thread; start worker
            self.run_pip_command(["install"] + self.packages, "Install all packages")

    def _set_buttons_enabled(self, enabled: bool):
        self.install_btn.setEnabled(enabled)
        self.update_btn.setEnabled(enabled)
        self.random_btn.setEnabled(enabled)
        self.install_all_btn.setEnabled(enabled)

# AppStore (demo)

class AppStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppStore - Luxxer (demo)")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 300)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Backup and restore local files")
        self.layout.addWidget(self.info_label)

        self.backup_btn = QPushButton("Create Backup")
        self.backup_btn.clicked.connect(self.create_backup)
        self.layout.addWidget(self.backup_btn)

        self.restore_btn = QPushButton("Restore Backup")
        self.restore_btn.clicked.connect(self.restore_backup)
        self.layout.addWidget(self.restore_btn)

    def create_backup(self):
        try:
            src_dir = QFileDialog.getExistingDirectory(self, "Select folder to backup")
            if not src_dir:
                return

            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save backup as",
                f"luxxer_backup_{int(datetime.datetime.now().timestamp())}.tar.gz",
                "Backup Archives (*.tar.gz)"
            )
            if not save_path:
                return

            with tarfile.open(save_path, "w:gz") as tar:
                tar.add(src_dir, arcname=os.path.basename(src_dir))

            QMessageBox.information(self, "Backup", f"Backup created at:\n{save_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Backup failed:\n{e}")

    def restore_backup(self):
        try:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select backup to restore", "", "Backup Archives (*.tar.gz)"
            )
            if not path:
                return
            restore_dir = QFileDialog.getExistingDirectory(self, "Select restore location")
            if not restore_dir:
                return

            with tarfile.open(path, "r:gz") as tar:
                tar.extractall(path=restore_dir)

            QMessageBox.information(self, "Restore", f"Backup restored to:\n{restore_dir}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Restore failed:\n{e}")

class DiskCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiskCleaner - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.info_label = QLabel("Disk Partitions and Usage (real-time).")
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
            partitions = psutil.disk_partitions(all=False)
            for p in partitions:
                try:
                    usage = psutil.disk_usage(p.mountpoint)
                    total_gb = usage.total / (1024 ** 3)
                    used_gb = usage.used / (1024 ** 3)
                    free_gb = usage.free / (1024 ** 3)
                    percent = usage.percent

                    self.disk_list.addItem(
                        f"{p.device} ({p.mountpoint}) - "
                        f"Total: {total_gb:.2f} GB, "
                        f"Used: {used_gb:.2f} GB, "
                        f"Free: {free_gb:.2f} GB, "
                        f"Usage: {percent}%"
                    )
                except PermissionError:
                    self.disk_list.addItem(f"{p.device} ({p.mountpoint}) - Access Denied")

            QMessageBox.information(self, "Refreshed", f"{len(partitions)} partitions listed.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not list partitions: {e}")

class SystemInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SystemInfo - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Attached Devices List (real-time)."))

        self.dev_list = QListWidget()
        l.addWidget(self.dev_list)

        self.refresh_btn = QPushButton("Refresh Devices")
        self.refresh_btn.clicked.connect(self.refresh_devices)
        l.addWidget(self.refresh_btn)

        self.refresh_devices()

    def refresh_devices(self):
        self.dev_list.clear()
        try:
            partitions = psutil.disk_partitions(all=True)
            for p in partitions:
                self.dev_list.addItem(
                    f"Disk: {p.device} -> {p.mountpoint} ({p.fstype})"
                )
            system = platform.system()
            if system == "Windows":
                try:
                    output = subprocess.check_output(
                        ["wmic", "path", "Win32_PnPEntity", "get", "Name"],
                        shell=True
                    ).decode(errors="ignore").splitlines()
                    for line in output:
                        if line.strip():
                            self.dev_list.addItem(f"Device: {line.strip()}")
                except Exception as e:
                    self.dev_list.addItem(f"Windows device scan error: {e}")

            elif system == "Linux":
                try:
                    output = subprocess.check_output(
                        ["lsusb"], shell=True
                    ).decode(errors="ignore").splitlines()
                    for line in output:
                        self.dev_list.addItem(f"USB: {line.strip()}")
                except Exception as e:
                    self.dev_list.addItem(f"Linux device scan error: {e}")

            elif system == "Darwin":  # macOS
                try:
                    output = subprocess.check_output(
                        ["system_profiler", "SPUSBDataType"],
                        shell=True
                    ).decode(errors="ignore").splitlines()
                    for line in output:
                        if line.strip():
                            self.dev_list.addItem(f"USB: {line.strip()}")
                except Exception as e:
                    self.dev_list.addItem(f"macOS device scan error: {e}")

            QMessageBox.information(
                self, "Refreshed", f"{self.dev_list.count()} devices listed."
            )

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not list devices: {e}")

system = platform.system()
jobs_cache = []

class PrinterManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrinterManager - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(500, 350)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.layout.addWidget(QLabel("Printer Queue Manager (real-time)."))

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
        global jobs_cache
        self.queue_list.clear()
        jobs_cache = []

        try:
            if system == "Windows":
                import win32print
                printers = win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
                )
                for flags, desc, name, comment in printers:
                    hprinter = win32print.OpenPrinter(name)
                    jobs = win32print.EnumJobs(hprinter, 0, -1, 1)
                    for job in jobs:
                        job_name = job["pDocument"]
                        self.queue_list.addItem(f"{name}: {job_name}")
                        jobs_cache.append((name, job_name, job["JobId"]))
                    win32print.ClosePrinter(hprinter)

            elif system in ["Linux", "Darwin"]:  # Linux/macOS
                import cups
                conn = cups.Connection()
                printers = conn.getPrinters()
                for printer in printers:
                    jobs = conn.getJobs(which_jobs="all")
                    for job_id, job in jobs.items():
                        job_name = job["title"]
                        self.queue_list.addItem(f"{printer}: {job_name}")
                        jobs_cache.append((printer, job_name, job_id))

            QMessageBox.information(self, "Queue Refreshed", f"{len(jobs_cache)} jobs loaded.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load printer jobs: {e}")

    def print_selected(self):
        selected = self.queue_list.currentItem()
        if not selected:
            return
        try:
            if system == "Windows":
                import win32print
                for printer, job_name, job_id in jobs_cache:
                    if job_name in selected.text():
                        hprinter = win32print.OpenPrinter(printer)
                        win32print.SetJob(hprinter, job_id, 0, None, win32print.JOB_CONTROL_RESUME)
                        win32print.ClosePrinter(hprinter)
                        QMessageBox.information(self, "Printing", f"Sent {job_name} to printer {printer}.")
                        return

            elif system in ["Linux", "Darwin"]:
                import cups
                conn = cups.Connection()
                for printer, job_name, job_id in jobs_cache:
                    if job_name in selected.text():
                        conn.restartJob(job_id)
                        QMessageBox.information(self, "Printing", f"Resumed {job_name} on {printer}.")
                        return

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not print: {e}")

class NetworkMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetworkMonitor - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        title = QLabel("🌐 Network Interfaces (Real-Time Monitor)")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        l.addWidget(title)

        self.if_list = QListWidget()
        l.addWidget(self.if_list, 1)

        self.refresh_btn = QPushButton("🔄 Refresh Now")
        self.refresh_btn.clicked.connect(self.refresh_interfaces)
        l.addWidget(self.refresh_btn)

        # Timer for real-time refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_interfaces)
        self.timer.start(2000) # refresh

        self.refresh_interfaces()

    def refresh_interfaces(self):
        self.if_list.clear()
        try:
            interfaces = psutil.net_if_addrs()
            for iface, addrs in interfaces.items():
                self.if_list.addItem(f"Interface: {iface}")
                for addr in addrs:
                    self.if_list.addItem(f"   {addr.family.name}: {addr.address}")
                self.if_list.addItem("")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot fetch interfaces: {e}")

import requests

class VPNClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPNClient - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 250)

        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        title = QLabel("🔒 VPN Client")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        l.addWidget(title)

        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Enter VPN server address")
        l.addWidget(self.server_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_vpn)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_vpn)
        self.disconnect_btn.setEnabled(False)
        l.addWidget(self.disconnect_btn)

        self.status_label = QLabel("Status: Disconnected")
        l.addWidget(self.status_label)

        self.ip_label = QLabel("Current IP: Unknown")
        l.addWidget(self.ip_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)

        self.connected = False
        self.vpn_server = None

    def connect_vpn(self):
        server = self.server_input.text().strip()
        if not server:
            QMessageBox.warning(self, "VPN", "Enter server address first")
            return

        self.vpn_server = server
        self.connected = True
        self.status_label.setText(f"Status: Connecting to {server}...")
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)

        self.timer.start(3000)
        self.update_status()

    def disconnect_vpn(self):
        self.connected = False
        self.vpn_server = None
        self.timer.stop()
        self.status_label.setText("Status: Disconnected")
        self.ip_label.setText("Current IP: Unknown")
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)

    def update_status(self):
        if not self.connected or not self.vpn_server:
            return

        try:
            ip = requests.get("https://api.ipify.org").text.strip()
            self.status_label.setText(f"Status: Connected to {self.vpn_server}")
            self.ip_label.setText(f"Current IP: {ip}")
        except Exception as e:
            self.status_label.setText("Status: Connection error")
            self.ip_label.setText("Current IP: Unknown")

class RemoteDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RemoteDesktop - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(500, 300)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Remote desktop client (VNC real-time)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter host:port (e.g. 192.168.1.10:5900)")
        l.addWidget(self.host_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_host)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_host)
        l.addWidget(self.disconnect_btn)

        self.status_label = QLabel("Status: Disconnected")
        l.addWidget(self.status_label)

        self.vnc_process = None

    def connect_host(self):
        host = self.host_input.text().strip()
        if host:
            self.vnc_process = QProcess(self)
            self.vnc_process.start("vncviewer", [host])

            self.status_label.setText(f"Connected to {host}")
            QMessageBox.information(self, "RemoteDesktop", f"Opened VNC session to {host}")
        else:
            QMessageBox.warning(self, "RemoteDesktop", "Enter host IP first")

    def disconnect_host(self):
        if self.vnc_process:
            self.vnc_process.kill()
            self.vnc_process = None
        self.status_label.setText("Status: Disconnected")
        QMessageBox.information(self, "RemoteDesktop", "Disconnected")

import paramiko

class SSHClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSHClient - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        self.setCentralWidget(w)

        l.addWidget(QLabel("SSH client (real-time)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host IP")
        l.addWidget(self.host_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        l.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        l.addWidget(self.pass_input)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_ssh)
        l.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_ssh)
        l.addWidget(self.disconnect_btn)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        l.addWidget(self.output_area)

        self.ssh_client = None
        self.transport = None

    def connect_ssh(self):
        host = self.host_input.text().strip()
        user = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not (host and user and password):
            QMessageBox.warning(self, "SSHClient", "Enter host, username, and password")
            return

        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(host, username=user, password=password)

            self.output_area.append(f"[+] Connected to {host} as {user}")
            QMessageBox.information(self, "SSHClient", f"Connected to {host} as {user}")

            # Start a thread to keep a real-time shell
            self.transport = self.ssh_client.get_transport().open_session()
            self.transport.get_pty()
            self.transport.invoke_shell()

            threading.Thread(target=self.read_output, daemon=True).start()

        except Exception as e:
            QMessageBox.critical(self, "SSHClient", f"Connection failed: {e}")

    def read_output(self):
        while True:
            if self.transport is None or self.transport.closed:
                break
            data = self.transport.recv(1024).decode("utf-8")
            if data:
                self.output_area.append(data)

    def disconnect_ssh(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            self.transport = None
            self.output_area.append("[-] Disconnected")
            QMessageBox.information(self, "SSHClient", "Disconnected")

class PortScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PortScanner - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(500, 350)

        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Port Scanner (real-time)"))

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Enter host IP")
        l.addWidget(self.host_input)

        self.scan_btn = QPushButton("Scan Ports")
        self.scan_btn.clicked.connect(self.scan_ports)
        l.addWidget(self.scan_btn)

        self.results_list = QListWidget()
        l.addWidget(self.results_list)

    def scan_ports(self):
        host = self.host_input.text().strip()
        if not host:
            QMessageBox.warning(self, "PortScanner", "Enter host IP first")
            return

        self.results_list.clear()
        QMessageBox.information(self, "PortScanner", f"Scanning {host}...")

        def do_scan():
            for port in range(1, 1025):  # scanning common ports (1–1024)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self.results_list.addItem(f"Port {port}: OPEN")
                sock.close()

            self.results_list.addItem("Scan complete.")

        threading.Thread(target=do_scan, daemon=True).start()

class ClipboardManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClipboardManager - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 300)

        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        # Clipboard history list
        self.clip_list = QListWidget()
        l.addWidget(self.clip_list)

        # Clear button
        self.clear_btn = QPushButton("Clear history")
        self.clear_btn.clicked.connect(self.clear_list)
        l.addWidget(self.clear_btn)

        # Connect to system clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        self.history = set()

    def on_clipboard_change(self):
        txt = self.clipboard.text().strip()
        if txt and txt not in self.history:
            self.history.add(txt)
            self.clip_list.addItem(txt[:200])

    def clear_list(self):
        self.clip_list.clear()
        self.history.clear()
        QMessageBox.information(self, "ClipboardManager", "Clipboard history cleared")

class SchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduler - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 300)

        # Main layout
        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        # List of alarms
        self.listw = QListWidget()
        l.addWidget(self.listw)

        # Add alarm button
        self.add_btn = QPushButton("Add Alarm")
        self.add_btn.clicked.connect(self.add_alarm)
        l.addWidget(self.add_btn)

        # Store alarms
        self.alarms = []

    def add_alarm(self):
        # Ask user for hours, minutes, seconds
        hours, ok1 = QInputDialog.getInt(self, "Alarm", "Hours:", min=0, max=23, value=0)
        if not ok1:
            return
        minutes, ok2 = QInputDialog.getInt(self, "Alarm", "Minutes:", min=0, max=59, value=0)
        if not ok2:
            return
        seconds, ok3 = QInputDialog.getInt(self, "Alarm", "Seconds:", min=0, max=59, value=10)
        if not ok3:
            return

        # Calculate alarm datetime
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)  # schedule for next day if time passed

        # Show in list
        self.listw.addItem(f"Alarm at {alarm_time.strftime('%H:%M:%S')}")

        # Calculate milliseconds until alarm
        delta_ms = int((alarm_time - now).total_seconds() * 1000)

        # Create QTimer for alarm
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.trigger_alarm(alarm_time))
        timer.start(delta_ms)

        # Store timer to prevent garbage collection
        self.alarms.append(timer)

    def trigger_alarm(self, alarm_time):
        QMessageBox.information(self, "Alarm", f"Alarm fired at {alarm_time.strftime('%H:%M:%S')}!")

import tempfile
import wave
import numpy as np
import sounddevice as sd

class VoiceRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceRecorder - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 250)

        # Layout
        w = QWidget()
        l = QVBoxLayout(w)
        self.setCentralWidget(w)

        l.addWidget(QLabel("Voice recorder - Real-time audio capture"))

        # Recording state
        self.recording = False
        self.audio_data = []
        self.fs = 44100  # Sample rate
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name

        # Buttons
        self.btn = QPushButton("Start recording")
        self.btn.clicked.connect(self.toggle_recording)
        l.addWidget(self.btn)

        self.playback_btn = QPushButton("Playback last recording")
        self.playback_btn.clicked.connect(self.playback)
        l.addWidget(self.playback_btn)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.audio_data = []
        self.btn.setText("Stop recording")
        self.stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback)
        self.stream.start()
        QMessageBox.information(self, "VoiceRecorder", "Recording started")

    def stop_recording(self):
        self.recording = False
        self.btn.setText("Start recording")
        self.stream.stop()
        self.stream.close()

        # Save to WAV
        audio_np = np.concatenate(self.audio_data, axis=0)
        with wave.open(self.temp_file, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.fs)
            wf.writeframes((audio_np * 32767).astype(np.int16).tobytes())

        QMessageBox.information(self, "VoiceRecorder", f"Recording stopped and saved to {self.temp_file}")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_data.append(indata.copy())

    def playback(self):
        if self.audio_data:
            # Load WAV file
            with wave.open(self.temp_file, "rb") as wf:
                data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                data = data.astype(np.float32) / 32767
                sd.play(data, wf.getframerate())
                sd.wait()
            QMessageBox.information(self, "VoiceRecorder", "Playback finished")
        else:
            QMessageBox.warning(self, "VoiceRecorder", "No recording found")

import re

class PasswordDialog(QDialog):
    def __init__(self, prompt="Enter password:", min_length=8):
        super().__init__()
        self.setWindowTitle("Secure Password Entry")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 200)
        self.min_length = min_length
        self.password = None

        # Layout
        layout = QVBoxLayout(self)

        self.label = QLabel(prompt)
        layout.addWidget(self.label)

        self.edit = QLineEdit()
        self.edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.edit)

        self.strength_label = QLabel("Password strength: ")
        layout.addWidget(self.strength_label)

        self.toggle_btn = QPushButton("Show / Hide")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.toggled.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_btn)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept_password)
        layout.addWidget(self.ok_btn)

        self.edit.textChanged.connect(self.update_strength)

    def toggle_visibility(self, checked):
        self.edit.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)

    def update_strength(self, text):
        strength = self.calculate_strength(text)
        self.strength_label.setText(f"Password strength: {strength}")

    def calculate_strength(self, pwd):
        score = 0
        if len(pwd) >= self.min_length:
            score += 1
        if re.search(r'[A-Z]', pwd):
            score += 1
        if re.search(r'[0-9]', pwd):
            score += 1
        if re.search(r'[^A-Za-z0-9]', pwd):
            score += 1

        if score <= 1:
            return "Weak"
        elif score == 2:
            return "Medium"
        elif score == 3:
            return "Strong"
        else:
            return "Very Strong"

    def accept_password(self):
        pwd = self.edit.text()
        if len(pwd) < self.min_length:
            QMessageBox.warning(self, "Weak Password", f"Password must be at least {self.min_length} characters long")
            return
        self.password = pwd
        self.accept()

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Calendar - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # Calendar
        self.cal = QCalendarWidget()
        self.cal.selectionChanged.connect(self.show_events)
        layout.addWidget(self.cal, 2)

        # Event list
        vbox = QVBoxLayout()
        self.event_list = QListWidget()
        vbox.addWidget(QLabel("Events for selected day:"))
        vbox.addWidget(self.event_list, 1)

        # Buttons
        btn_add = QPushButton("Add Event")
        btn_add.clicked.connect(self.add_event)
        btn_remove = QPushButton("Remove Event")
        btn_remove.clicked.connect(self.remove_event)
        vbox.addWidget(btn_add)
        vbox.addWidget(btn_remove)

        layout.addLayout(vbox, 1)

        # Internal storage: {date_string: [(event_text, color)]}
        self.events = {}
        self.show_events()

    def add_event(self):
        date = self.cal.selectedDate().toPyDate()
        text, ok = QInputDialog.getText(self, "Add Event", "Event description:")
        if ok and text.strip():
            color = QColorDialog.getColor(Qt.GlobalColor.yellow, self, "Pick event color")
            if not color.isValid():
                color = Qt.GlobalColor.yellow
            date_str = date.isoformat()
            self.events.setdefault(date_str, []).append((text.strip(), color))
            self.show_events()

    def remove_event(self):
        selected = self.event_list.currentRow()
        if selected == -1:
            return
        date_str = self.cal.selectedDate().toPyDate().isoformat()
        if date_str in self.events:
            self.events[date_str].pop(selected)
            if not self.events[date_str]:
                del self.events[date_str]
        self.show_events()

    def show_events(self):
        self.event_list.clear()
        date_str = self.cal.selectedDate().toPyDate().isoformat()
        if date_str in self.events:
            for text, color in self.events[date_str]:
                item = QLabel(text)
                item.setStyleSheet(f"color: {color.name()}")
                self.event_list.addItem(text)

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Task Manager - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Filter by process name...")
        self.search_bar.textChanged.connect(self.refresh)
        layout.addWidget(self.search_bar)

        # Process list
        self.listw = QListWidget()
        layout.addWidget(self.listw, 1)

        # Buttons
        hbox = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh Now")
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_kill = QPushButton("Kill Selected")
        self.btn_kill.clicked.connect(self.kill_selected)
        hbox.addWidget(self.btn_refresh)
        hbox.addWidget(self.btn_kill)
        layout.addLayout(hbox)

        # Timer for real-time update
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)  # every 2 seconds

        self.refresh()

    def refresh(self):
        filter_text = self.search_bar.text().lower()
        self.listw.clear()
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                name = p.info['name']
                if filter_text and filter_text not in name.lower():
                    continue
                cpu = p.info['cpu_percent']
                mem = p.info['memory_percent']
                self.listw.addItem(f"{p.info['pid']:5} | {name:25} | CPU: {cpu:5.1f}% | MEM: {mem:5.1f}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def kill_selected(self):
        selected = self.listw.currentItem()
        if not selected:
            return
        pid = int(selected.text().split('|')[0].strip())
        try:
            p = psutil.Process(pid)
            p.terminate()
            QMessageBox.information(self, "Task Manager", f"Process {pid} terminated.")
        except Exception as e:
            QMessageBox.warning(self, "Task Manager", f"Failed to terminate process {pid}: {e}")
        self.refresh()

class TerminalWidget(QWidget):
    command_entered = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.ico'))
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

class PaintCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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

# Zer3 Highlighter

class Zer3Highlighter(QSyntaxHighlighter):
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(1700, 600)

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
        code = self.editor.toPlainText().strip()
        if not code:
            self.output.setPlainText("⚠️ No code to run.")
            return
        try:
            result = self.interpreter.run(code)
            self.output.setPlainText(str(result))
        except Exception as e:
            self.output.setPlainText(f"❌ Error: {e}")

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
        self.setWindowIcon(QIcon('icon.ico'))
        w = QWidget()
        l = QVBoxLayout(w)

        l.addWidget(QLabel("LuxxerWeb safe browser launcher."))
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

import sys, imaplib, smtplib, email, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mail - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Login info
        self.email_address = None
        self.password = None
        self.imap_server = None
        self.smtp_server = None

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Inbox"))
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)
        header_layout.addWidget(self.login_btn)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_inbox)
        header_layout.addWidget(self.refresh_btn)
        self.compose_btn = QPushButton("Compose")
        self.compose_btn.clicked.connect(self.compose)
        header_layout.addWidget(self.compose_btn)
        self.layout.addLayout(header_layout)

        # Search
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search emails...")
        self.search_bar.textChanged.connect(self.filter_inbox)
        self.layout.addWidget(self.search_bar)

        # Inbox
        self.inbox_list = QListWidget()
        self.layout.addWidget(self.inbox_list)
        self.inbox = []

        # Drafts
        self.drafts = []

        # Auto-refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_inbox)
        self.timer.start(60000)  # every 60s

    def login(self):
        email_addr, ok1 = QInputDialog.getText(self, "Login", "Email:")
        pwd, ok2 = QInputDialog.getText(self, "Login", "Password:", QLineEdit.EchoMode.Password)
        if not (ok1 and ok2):
            return
        self.email_address = email_addr
        self.password = pwd

        # Simple server guessing for Gmail/Outlook
        if "gmail" in email_addr.lower():
            self.imap_server = "imap.gmail.com"
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
        elif "outlook" in email_addr.lower() or "hotmail" in email_addr.lower():
            self.imap_server = "imap-mail.outlook.com"
            self.smtp_server = "smtp.office365.com"
            self.smtp_port = 587
        else:
            QMessageBox.warning(self, "Login", "Unknown provider, please modify manually.")
            return

        try:
            # Test IMAP connection
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(self.email_address, self.password)
            QMessageBox.information(self, "Login", "Login successful!")
            self.refresh_inbox()
        except Exception as e:
            QMessageBox.warning(self, "Login", f"Failed to login: {e}")

    def refresh_inbox(self):
        if not hasattr(self, 'imap'):
            return
        try:
            self.inbox_list.clear()
            self.inbox = []
            self.imap.select("inbox")
            status, messages = self.imap.search(None, "ALL")
            for num in messages[0].split()[-20:][::-1]:  # last 20 emails
                status, data = self.imap.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])
                sender = msg.get("From")
                subject = msg.get("Subject")
                date = msg.get("Date")
                self.inbox.append({"sender": sender, "subject": subject, "date": date, "raw": msg})
                self.inbox_list.addItem(f"{date} | {sender} | {subject}")
        except Exception as e:
            QMessageBox.warning(self, "Inbox", f"Failed to refresh: {e}")

    def filter_inbox(self, text):
        self.inbox_list.clear()
        for mail in self.inbox:
            if text.lower() in mail['subject'].lower() or text.lower() in mail['sender'].lower():
                self.inbox_list.addItem(f"{mail['date']} | {mail['sender']} | {mail['subject']}")

    def compose(self):
        dlg = QTextEdit()
        dlg.setWindowTitle("Compose Email")
        dlg.resize(600, 400)
        dlg.show()

        def send_mail():
            recipient, ok = QInputDialog.getText(self, "Send Email", "Recipient:")
            if not ok:
                return
            subject, ok = QInputDialog.getText(self, "Send Email", "Subject:")
            if not ok:
                return
            body = dlg.toPlainText()
            try:
                smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
                smtp.starttls()
                smtp.login(self.email_address, self.password)
                msg = MIMEMultipart()
                msg['From'] = self.email_address
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                smtp.send_message(msg)
                smtp.quit()
                QMessageBox.information(self, "Email", "Email sent successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Email", f"Failed to send email: {e}")

        dlg.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        dlg.customContextMenuRequested.connect(lambda _: send_mail())

# Worker to run commands in a separate thread
class CmdWorker(QThread):
    output = pyqtSignal(str)
    def __init__(self, cmd, cwd):
        super().__init__()
        self.cmd = cmd
        self.cwd = cwd

    def run(self):
        try:
            process = subprocess.Popen(
                self.cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                shell=True,
                text=True
            )
            for line in process.stdout:
                self.output.emit(line.rstrip())
            process.wait()
            if process.returncode != 0:
                self.output.emit(f"[Process exited with code {process.returncode}]")
        except Exception as e:
            self.output.emit(f"Execution error: {e}")

class CmdApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Luxxer CMD')
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.history = []
        self.history_index = -1

        self.builtin_cmds = {f'cmd{i}': f'Built-in command {i}' for i in range(1, 401)}
        self.builtin_cmds.update({
            'help': 'Show all commands',
            'pwd': 'Show current directory',
            'cd': 'Change directory',
            'exit': 'Exit CMD'
        })

        # Display all commands on first launch
        self.write(f'Luxxer CMD (cwd={self.cwd}). Type commands below. Available commands:')
        self.write(', '.join(self.builtin_cmds.keys()))

    def write(self, text: str):
        self.output.append(text)

    def on_enter(self):
        line = self.input.text().strip()
        if not line:
            return
        self.write(f'> {line}')
        self.history.append(line)
        self.history_index = len(self.history)
        self.input.clear()

        parts = line.split()
        cmd = parts[0]
        args = parts[1:]

        # Handle built-in commands
        if cmd in self.builtin_cmds:
            if cmd == 'help':
                self.write('Available commands:')
                self.write(', '.join(self.builtin_cmds.keys()))
            elif cmd == 'pwd':
                self.write(self.cwd)
            elif cmd == 'cd':
                if args:
                    new_dir = os.path.abspath(os.path.join(self.cwd, args[0]))
                    if os.path.isdir(new_dir):
                        self.cwd = new_dir
                        self.write(f'cwd -> {self.cwd}')
                    else:
                        self.write("Directory not found")
                else:
                    self.write("cd requires a path")
            elif cmd == 'exit':
                self.close()
            else:
                self.write(f'{self.builtin_cmds[cmd]} executed.')
            return

        # Otherwise execute as real system command
        worker = CmdWorker(line, self.cwd)
        worker.output.connect(self.write)
        worker.start()

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

# Brute-force thread (local demo only, limited length to avoid runaway)
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

class CyberToolsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{tr('tools')} - Luxxer (educational)")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(900, 600)

        self._brute_thread: Optional[BruteForceThread] = None
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

class GuardianAVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GuardianAV - Luxxer')
        self.setWindowIcon(QIcon('icon.ico'))
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

class WinRarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WinRAR - Luxxer (fake)')
        self.setWindowIcon(QIcon('icon.ico'))
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

APP_STATE = {}
APP_STATE.setdefault('settings', {'lang': 'en', 'username': 'user'})

class FilePreviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Preview')
        self.setWindowIcon(QIcon('icon.ico'))
        layout = QVBoxLayout()
        self.label = QLabel('Select a file from Explorer')
        layout.addWidget(self.label)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def preview_file(self, path: str):
        try:
            with open(path,'r',encoding='utf-8') as f:
                text = f.read(5000)
            self.label.setText(text)
        except Exception as e:
            self.label.setText(f'Cannot preview: {e}')

class SettingsApp(QMainWindow):
    def __init__(self, main_ref=None):
        super().__init__()
        self.main_ref = main_ref

        self.setWindowTitle("Settings - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.main_ref = main_ref
        self.setObjectName('taskbar')
        self.setWindowIcon(QIcon('icon.ico'))

        # Layouts
        h = QHBoxLayout()
        self.setLayout(h)

        # Start button
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.main_ref.toggle_start)
        h.addWidget(self.start_btn)

        # CPU/RAM/GPU usage
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setFormat('CPU: %p%')
        self.ram_bar = QProgressBar()
        self.ram_bar.setFormat('RAM: %p%')
        h.addWidget(self.cpu_bar)
        h.addWidget(self.ram_bar)

        # Process button
        self.proc_btn = QPushButton('Processes')
        self.proc_btn.clicked.connect(self.show_processes)
        h.addWidget(self.proc_btn)

        # Time label
        self.time_label = QLabel(time.strftime('%H:%M'))
        h.addWidget(self.time_label)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_taskbar)
        self.timer.start(1000)

    def update_taskbar(self):
        self.cpu_bar.setValue(int(psutil.cpu_percent()))
        self.ram_bar.setValue(int(psutil.virtual_memory().percent))
        self.time_label.setText(time.strftime('%H:%M'))

    def show_processes(self):
        dlg = QWidget()
        dlg.setWindowTitle('Processes')
        dlg.resize(600, 400)
        layout = QVBoxLayout()
        dlg.setLayout(layout)

        self.proc_list = QListWidget()
        layout.addWidget(self.proc_list)

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.update_process_list)
        layout.addWidget(self.refresh_btn)

        self.kill_btn = QPushButton('Kill Selected Process')
        self.kill_btn.clicked.connect(self.kill_process)
        layout.addWidget(self.kill_btn)

        self.update_process_list()
        dlg.show()
        dlg.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def update_process_list(self):
        self.proc_list.clear()
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                item_text = f"{proc.info['pid']:5} | {proc.info['name'][:25]:25} | CPU: {proc.info['cpu_percent']:5.1f}% | RAM: {proc.info['memory_percent']:5.1f}%"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, proc.info['pid'])
                self.proc_list.addItem(item)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def kill_process(self):
        item = self.proc_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Kill Process", "No process selected!")
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            QMessageBox.information(self, "Kill Process", f"Process {pid} terminated.")
            self.update_process_list()
        except Exception as e:
            QMessageBox.warning(self, "Kill Process", f"Failed: {e}")

class ContactsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contacts - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
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
        self.setWindowIcon(QIcon('icon.ico'))
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

def instantiate_app_widget(app_class):
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

# Helpers: save and run
def safe_save_text(parent, title: str, default_name: str, text: str):
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

class SafeApp(QWidget):
    def __init__(self, app_name: str = "Unknown App"):
        try:
            super().__init__()
            self.app_name = app_name
            self.setWindowTitle(app_name)
            self.setWindowIcon(QIcon('icon.ico'))

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
        self.base_size = int(base_size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # drag helpers
        self._drag_start_pos = None

        # scale management
        self._scale = 1.0
        self._target_scale = 1.0
        self._min_scale = 0.9
        self._max_scale = 1.8
        self.setFixedSize(self.base_size, self.base_size)
        self.setToolTip(name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # default style
        self._apply_style(self.base_size)

    def _apply_style(self, size_px):
        font_px = max(10, int(size_px * 0.36))
        border_radius = int(size_px * 0.18)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0,0,0,0.65);
                color: white;
                font-weight: 700;
                font-size: {font_px}px;
                border-radius: {border_radius}px;
                border: 0px;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.06);
            }}
            QPushButton:pressed {{
                background-color: rgba(255,255,255,0.04);
            }}
        """)

    def set_scale_limits(self, min_s, max_s):
        self._min_scale = min_s
        self._max_scale = max_s

    def set_target_scale(self, s):
        self._target_scale = max(self._min_scale, min(self._max_scale, s))

    def step_towards_target(self, smooth=0.22):
        ds = (self._target_scale - self._scale) * smooth
        if abs(ds) < 0.001:
            if abs(self._target_scale - self._scale) > 0.0001:
                self._scale = self._target_scale
                self._apply_scale()
                return True
            return False
        self._scale += ds
        self._apply_scale()
        return True

    def _apply_scale(self):
        ns = max(12, int(round(self.base_size * self._scale)))
        self.setFixedSize(ns, ns)
        self._apply_style(ns)

    def reset_scale(self):
        self._target_scale = 1.0

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = ev.pos()
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        # start drag if moved beyond threshold
        if ev.buttons() & Qt.MouseButton.LeftButton and self._drag_start_pos is not None:
            if (ev.pos() - self._drag_start_pos).manhattanLength() > QApplication.startDragDistance():
                try:
                    mime = QMimeData()
                    mime.setText(self.full_name)
                    # include a pixmap snapshot so desktop can show same icon
                    pix = self.grab()
                    if not pix.isNull():
                        # attach image data to mime
                        mime.setImageData(pix.toImage())
                    drag = QDrag(self)
                    drag.setMimeData(mime)
                    # set feedback pixmap (scaled a bit)
                    small = pix.scaled(max(24, pix.width()//2), max(24, pix.height()//2),
                                       Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    drag.setPixmap(small)
                    # Use CopyAction — dock -> desktop should create a shortcut (copy)
                    drag.exec(Qt.DropAction.CopyAction)
                except Exception:
                    traceback.print_exc()
        super().mouseMoveEvent(ev)

# BottomDock
class BottomDock(QScrollArea):
    def __init__(self, main_ref, apps_list, base_btn_size=56, max_scale=1.8, influence=140, spacing=8):
        super().__init__()
        self.setObjectName('bottom_dock')
        self.main_ref = main_ref
        self.base_btn_size = int(base_btn_size)
        self.max_scale = float(max_scale)
        self.influence = float(influence)
        self.spacing = int(spacing)

        # ScrollArea setup
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedHeight(self.base_btn_size + 22)

        # Container for buttons
        self.container = QWidget()
        self.layout = QHBoxLayout(self.container)
        self.layout.setContentsMargins(10, 6, 10, 6)
        self.layout.setSpacing(self.spacing)
        self.setWidget(self.container)

        # Buttons list
        self.buttons = []
        for name in apps_list:
            btn = DockButton(name, self.base_btn_size)
            btn.clicked.connect(lambda checked=False, n=name: self._launch_safe(n))
            self.layout.addWidget(btn)
            btn.setMouseTracking(True)
            btn.set_scale_limits(0.95, self.max_scale)
            self.buttons.append(btn)

        # mouse tracking state
        self.setMouseTracking(True)
        self.container.setMouseTracking(True)
        self._last_pos = None

        # timer-driven smooth updates (~60fps)
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start()

        # smooth scroll animation holder
        self._scroll_anim = None

    def _launch_safe(self, name):
        try:
            if hasattr(self.main_ref, 'launch_app'):
                self.main_ref.launch_app(name)
        except Exception:
            traceback.print_exc()

    # Map global cursor to local dock coords, with protective checks
    def _update_cursor_local(self):
        try:
            gp = QCursor.pos()
            local = self.mapFromGlobal(gp)
            if -self.influence <= local.y() <= (self.height() + self.influence):
                self._last_pos = local
            else:
                self._last_pos = None
        except Exception:
            self._last_pos = None

    def enterEvent(self, ev):
        self._update_cursor_local()
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        self._last_pos = None
        super().leaveEvent(ev)

    def mouseMoveEvent(self, ev):
        self._update_cursor_local()
        super().mouseMoveEvent(ev)

    def wheelEvent(self, ev):
        delta = -ev.angleDelta().y()
        sb = self.horizontalScrollBar()
        target = sb.value() + delta * 2
        self.smooth_scroll_to(target)
        ev.accept()

    def smooth_scroll_to(self, target_value, duration=260):
        sb = self.horizontalScrollBar()
        target = max(sb.minimum(), min(sb.maximum(), int(target_value)))
        if self._scroll_anim is not None:
            try:
                self._scroll_anim.stop()
            except Exception:
                pass
        anim = QPropertyAnimation(sb, b"value", self)
        anim.setDuration(duration)
        anim.setStartValue(sb.value())
        anim.setEndValue(target)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()
        self._scroll_anim = anim

    def center_button_index(self, index, duration=300):
        if index < 0 or index >= len(self.buttons):
            return
        b = self.buttons[index]
        btn_center = b.geometry().left() + b.width() // 2
        viewport_center = self.viewport().width() // 2
        target = btn_center - viewport_center
        self.smooth_scroll_to(target, duration=duration)

    def _on_timer(self):
        if not self.buttons:
            return

        if self._last_pos is None:
            for b in self.buttons:
                b.set_target_scale(1.0)
                b.step_towards_target(smooth=0.25)
            return

        px = self._last_pos.x()
        scroll_val = self.horizontalScrollBar().value()
        sigma = max(1.0, (self.influence / 3.0))
        two_sigma_sq = 2.0 * (sigma * sigma)

        for i, b in enumerate(self.buttons):
            btn_left = b.geometry().left()
            btn_center_in_self = btn_left - scroll_val + (b.width() // 2)
            dist = abs(px - btn_center_in_self)
            if dist < self.influence * 1.6:
                factor = math.exp(-(dist * dist) / two_sigma_sq)
            else:
                factor = 0.0
            factor = max(0.0, min(1.0, factor))
            target = 1.0 + (self.max_scale - 1.0) * factor
            b.set_target_scale(target)

        for b in self.buttons:
            b.step_towards_target(smooth=0.22)

class PlaceholderApp(QMainWindow):
    def __init__(self, title: str, desc: str = ""):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('icon.ico'))
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
    'WebBrowser': WebBrowserApp,
    'Settings': lambda: SettingsApp(main_win) if 'main_win' in globals() else SettingsApp(None),
    'GamesApp': GamesApp,
    'ApplicationAdder': ApplicationAdderApp,
    'WinRAR': WinRarApp,
    'Zer3 IDE': Zer3IDE,
    'Calculator': CalculatorApp,
    'JokeGenerator': JokeGeneratorApp,
    'MotivationAIChat': lambda: MotivationAIChat(),
    'RandomChallenge': RandomChallengeApp,
    'Cyber Tools': CyberToolsApp,
    'GuardianAV': GuardianAVApp,
    'CMD': CmdApp,
    'TaskManager': TaskManagerApp,
    'FilePreview': FilePreviewApp,
    'Calendar': CalendarApp,
    'Mail': MailApp,
    'Contacts': ContactsApp,
    'HackerSimulator': HackerSimulatorApp,
    'ASCIIPainter': ASCIIPainterApp,
    'FortuneTeller': FortuneTellerApp,
    'Photos': PhotosApp,
    'MusicPlayer': MusicPlayerApp,
    'VideoPlayer': VideoPlayerApp,
    'PDFReader': PDFReaderApp,
    'OfficeWriter': OfficeWriterApp,
    'Spreadsheet': SpreadsheetApp,
    'Presentation': PresentationApp,
    'StickyNotes': StickyNotesApp,
    'Screenshot': ScreenshotApp,
    'ScreenRecorder': ScreenRecorderApp,
    'ImageEditorPro': ImageEditorProApp,
    'VideoEditor': VideoEditorApp,
    'MediaConverter': MediaConverterApp,
    'TerminalEmulator': TerminalEmulatorApp,
    'ShellX': ShellXApp,
    'GitClient': GitClientApp,
    'DockerManager': DockerManagerApp,
    'PackageManager': PackageManagerApp,
    'AppStore': AppStoreApp,
    'BackupRestore': BackupRestoreApp,
    'DiskCleaner': DiskCleanerApp,
    'DiskManager': DiskManagerApp,
    'SystemInfo': SystemInfoApp,
    'DeviceManager': DeviceManagerApp,
    'PrinterManager': PrinterManagerApp,
    'LuxxerWeb': LuxxerWebApp,
    'NetworkMonitor': NetworkMonitorApp,
    'VPNClient': VPNClientApp,
    'RemoteDesktop': RemoteDesktopApp,
    'SSHClient': SSHClientApp,
    'PortScanner': PortScannerApp,
    'WiFiAnalyzer': WiFiAnalyzerApp,
    'ClipboardManager': ClipboardManagerApp,
    'Scheduler': SchedulerApp,
    'VoiceRecorder': VoiceRecorderApp,
    'HabitTracker': HabitTrackerApp,
    'Pomodoro': PomodoroApp,
    'RandomStory': RandomStoryApp,
    'TravelTips': TravelTipsApp,
    'QRCodeGenerator': QRCodeGeneratorApp,
    'ColorPalette': ColorPaletteApp,
    'RecipeBox': RecipeBoxApp,
    'BudgetTracker': BudgetTrackerApp,
    'TerminalGames': TerminalGamesApp,
    'AmbientSound': AmbientSoundApp,
    'ScreenOrganizer': ScreenOrganizerApp,
    'ThemePreview': ThemePreviewApp,
    'TabbedBrowser': TabbedBrowserApp,
    'IncognitoBrowser': IncognitoBrowserApp,
    'ReaderModeBrowser': ReaderModeBrowserApp,
    'RSSFeedReader': RSSFeedReaderApp,
    'LocalNotes': LocalNotesApp,
    'SecureVaultLite': SecureVaultLiteApp,
    'ImageGallery': ImageGalleryApp,
    'BatchImageResizer': BatchImageResizerApp,
    'AudioPlayerPro': AudioPlayerProApp,
    'VideoStreamPlayer': VideoStreamPlayerApp,
    'JSONInspector': JSONInspectorApp,
    'CSVEditorPro': CSVEditorProApp,
    'SQLiteBrowser': SQLiteBrowserApp,
    'APIRequester': APIRequesterApp,
    'AutomationScript': AutomationScriptApp,
    'OCRTool': OCRToolApp,
    'PodcastManager': PodcastManagerApp,
    'EpubReader': EpubReaderApp,
    'ColorGrading': ColorGradingApp,
    'FontPreviewer': FontPreviewerApp,
    'IconSetManager': IconSetManagerApp,
    'ClipStack': ClipStackApp,
    'WindowTiler': WindowTilerApp,
    'DesktopSpaces': DesktopSpacesApp,
    'NetworkSpeedTester': NetworkSpeedTesterApp,
    'FocusTimer': FocusTimerApp,
    'PasswordGenerator': PasswordGeneratorApp,
    'WallpapersManager': WallpapersManagerApp
}

class MainWindow(QMainWindow):
    def __init__(self, APPS_LIST, APP_STATE=None):
        super().__init__()
        self.APP_STATE = APP_STATE or {}
        self.APP_STATE.setdefault('desktop_icons', [])
        self.setWindowTitle("Luxxer OS")
        self.setWindowIcon(QIcon("icon.ico"))
        self.resize(1280, 800)

        wallpaper_path = self.APP_STATE.get('settings', {}).get('wallpaper', "ScreenPhoto2-2560x1440px.png")
        self.wallpaper = QPixmap(wallpaper_path) if wallpaper_path else QPixmap()

        # MDI area (desktop background + app subwindows)
        self.mdi = QMdiArea()
        self.mdi.paintEvent = self._paint_background

        self.icon_area = IconAdderAreaMarquee(self.mdi.viewport(), cell_size=120, spacing=12)
        self.icon_area.setGeometry(self.mdi.viewport().rect())
        self.icon_area.lower()   # keep it behind MDI child windows visually
        self.icon_area.show()

        # important: let child receive drag events (avoid viewport swallowing them)
        try:
            self.mdi.viewport().setAcceptDrops(False)
        except Exception:
            pass

        # connect signals
        self.icon_area.icon_added.connect(self._on_icon_added)
        self.icon_area.icon_activated.connect(self._on_icon_activated)

        # Bottom dock (assumed to exist)
        self.dock = BottomDock(self, APPS_LIST)

        # central layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.mdi, 1)
        layout.addWidget(self.dock, 0)
        self.setCentralWidget(central)

        # app mapping placeholder
        self.app_map = {name: lambda n=name: QLabel(f"{n} (Placeholder)") for name in APPS_LIST}

        # context menu on desktop viewport
        self.mdi.viewport().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.mdi.viewport().customContextMenuRequested.connect(self._show_context_menu)
        self.centralWidget().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.centralWidget().customContextMenuRequested.connect(self._show_context_menu)

        self._patch_mouse_press(self.mdi.viewport())
        self._patch_mouse_press(self.centralWidget())

        # load icons from state after show (use timer so geometry is ready)
        QTimer.singleShot(40, self._load_desktop_icons)

    def _load_desktop_icons(self):
        try:
            names = self.APP_STATE.get('desktop_icons', []) or []
            self.icon_area.clear_icons()
            for n in names:
                self.icon_area.add_icon(n)
        except Exception:
            traceback.print_exc()

    def _position_icon_area(self):
        try:
            vp = self.mdi.viewport()
            self.icon_area.setGeometry(vp.rect())
        except Exception:
            pass

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        QTimer.singleShot(0, self._position_icon_area)

    def showEvent(self, ev):
        super().showEvent(ev)
        QTimer.singleShot(0, self._position_icon_area)

    def _on_icon_added(self, name: str, index: int, pos: QPoint):
        try:
            names = [it.name for it in self.icon_area.icons]
            self.APP_STATE['desktop_icons'] = names
            if save_state:
                try:
                    save_state(self.APP_STATE)
                except Exception:
                    pass
        except Exception:
            traceback.print_exc()

    def _on_icon_activated(self, name: str):
        try:
            if name in APP_MAPPING:
                self.launch_app(name)
            else:
                QMessageBox.information(self, "Launch", f"No app mapped for shortcut '{name}'.")
        except Exception:
            traceback.print_exc()

    def _patch_mouse_press(self, widget):
        old_mouse = getattr(widget, "mousePressEvent", None)
        def patched_mouse(e):
            try:
                if e.button() == Qt.MouseButton.RightButton:
                    pos = e.globalPosition().toPoint() if hasattr(e, "globalPosition") else e.globalPos()
                    self._show_context_menu(pos)
                    return
            except Exception:
                pass
            if callable(old_mouse):
                try:
                    old_mouse(e)
                except Exception:
                    pass
        widget.mousePressEvent = patched_mouse

    def _show_context_menu(self, global_pos):
        menu = QMenu(self)
        a_refresh = menu.addAction("Refresh")
        a_copy = menu.addAction("Copy")
        a_paste = menu.addAction("Paste")
        menu.addSeparator()
        a_settings = menu.addAction("Settings")
        a_change_wallpaper = menu.addAction("Change wallpaper...")
        menu.addSeparator()
        a_exit = menu.addAction("Exit Luxxer")

        a_refresh.triggered.connect(self._apply_mdi_background)
        a_settings.triggered.connect(lambda: self.launch_app("Settings"))
        a_change_wallpaper.triggered.connect(self._choose_wallpaper)
        a_exit.triggered.connect(QApplication.instance().quit)

        a_copy.triggered.connect(self._copy_to_clipboard)
        a_paste.triggered.connect(self._paste_from_clipboard)

        menu.exec(global_pos)

    def _choose_wallpaper(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose wallpaper", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if path:
            self.set_wallpaper(path)

    def set_wallpaper(self, path: str):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Wallpaper", "Failed to load image.")
            return
        self.wallpaper = pixmap
        try:
            self.mdi.viewport().update()
        except Exception:
            self.update()
        if self.APP_STATE is not None:
            self.APP_STATE.setdefault('settings', {})['wallpaper'] = path
            if save_state:
                try:
                    save_state(self.APP_STATE)
                except Exception:
                    pass

    def _paint_background(self, event):
        try:
            painter = QPainter(self.mdi.viewport())
            screen_size = QApplication.primaryScreen().size()
            rect = QRect(QPoint(0, 0), screen_size)

            # CLEAR background using window palette
            painter.fillRect(rect, self.palette().window())

            if self.wallpaper and not self.wallpaper.isNull():
                pm = self.wallpaper.scaled(rect.size(),
                                           Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                           Qt.TransformationMode.SmoothTransformation)
                x = (rect.width() - pm.width()) // 2
                y = (rect.height() - pm.height()) // 2
                painter.drawPixmap(x, y, pm)
        except Exception:
            traceback.print_exc()

    def _apply_mdi_background(self):
        try:
            self.mdi.viewport().update()
        except Exception:
            self.update()

    def _copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        focused = QApplication.focusWidget()
        try:
            if isinstance(focused, QLineEdit):
                clipboard.setText(focused.text())
            elif isinstance(focused, QTextEdit):
                clipboard.setText(focused.toPlainText())
            elif isinstance(focused, QLabel):
                clipboard.setText(focused.text())
            else:
                clipboard.setText("")
        except Exception:
            clipboard.setText("")

    def _paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        focused = QApplication.focusWidget()
        try:
            if isinstance(focused, QLineEdit):
                focused.setText(clipboard.text())
            elif isinstance(focused, QTextEdit):
                focused.insertPlainText(clipboard.text())
        except Exception:
            pass

    def launch_app(self, app_name: str):
        if app_name in APP_MAPPING:
            app_class = APP_MAPPING[app_name]
            try:
                app_widget = app_class() if callable(app_class) else app_class
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

    def open_app(self, app_class):
        if app_class is DesktopSpacesApp:
            app = app_class(self)
        else:
            app = app_class()
        app.show()

    def animate_window_show(self, sub):
        sub.setMinimumSize(0, 0)
        geom = sub.geometry()
        start_geom = QRect(geom.center().x(), geom.center().y(), 0, 0)
        anim = QPropertyAnimation(sub, b"geometry")
        anim.setDuration(400)
        anim.setStartValue(start_geom)
        anim.setEndValue(geom)
        anim.setEasingCurve(QPropertyAnimation.EasingCurveType.OutBack)
        sub.setGeometry(start_geom)
        anim.start()
        sub._anim = anim

# MAIN

if __name__ == "__main__":

    APP_STATE = load_state() or {}
    APP_STATE.setdefault('settings', {})

    app = QApplication(sys.argv)
    apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))

    install_global_handlers(restart_callback=lambda: launch_main(app))

    def launch_main(app_instance):
        start = StartScreen(app_instance, APP_STATE)
        if start.exec() == QDialog.DialogCode.Accepted:
            main_win = MainWindow(APPS_LIST)
            apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))
            main_win.showFullScreen()
            return app.exec()
        else:
            sys.exit(0)

    exit_code = run_with_bsod(lambda: launch_main(app))
    sys.exit(exit_code)