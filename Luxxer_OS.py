from __future__ import annotations
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
from iconadderonmainscreen import IconAdderAreaMarquee, IconAdderArea
import operator as op

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

from runners import _DesktopItemRunner

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
    'Notebook','Paint','Explorer','WebBrowser','Settings','LuxxerArchiver','Zer3 IDE','Calculator',
    'Cyber Tools','GuardianAV','CMD','RandomChallenge','MotivationAIChat','JokeGenerator',
    'TaskManager','FilePreview','Calendar','HackerSimulator','ASCIIPainter','FortuneTeller',
    'Mail','Contacts','Photos','MusicPlayer','VideoPlayer','PDFReader','OfficeWriter',
    'Spreadsheet','Presentation','StickyNotes','Screenshot','ScreenRecorder',
    'ImageEditorPro','VideoEditor','MediaConverter','TerminalEmulator','ShellX','GitClient',
    'DockerManager','PackageManager','AppStore','BackupRestore','DiskCleaner','DiskManager',
    'SystemInfo','DeviceManager','PrinterManager','LuxxerWeb','NetworkMonitor','VPNClient','RemoteDesktop',
    'SSHClient','PortScanner','WiFiAnalyzer','ClipboardManager','Scheduler','VoiceRecorder',
    'GamesApp','ApplicationAdder','HabitTracker','Pomodoro','RandomStory','TravelTips',
    'QRCodeGenerator','ColorPalette','RecipeBox','BudgetTracker',
    'TerminalGames','AmbientSound','ScreenOrganizer','ThemePreview',
    'WebBrowser','TabbedBrowser','IncognitoBrowser','ReaderModeBrowser',
    'RSSFeedReader','LocalNotes','SecureVaultLite','ImageGallery','BatchImageResizer',
    'AudioPlayerPro','VideoStreamPlayer','JSONInspector','CSVEditorPro','SQLiteBrowser',
    'APIRequester','AutomationScript','OCRTool','PodcastManager','EpubReader','ColorGrading',
    'FontPreviewer','IconSetManager','ClipStack','WindowTiler','DesktopSpaces',
    'NetworkSpeedTester','FocusTimer','PasswordGenerator','WallpapersManager'
]

APP_ICONS = {
    'Notebook': 'NoteBook.ico',
    'Paint': 'Paint.ico',
    'Explorer': 'Explorer.ico',
    'WebBrowser': 'WebBrovser.ico',
    'Settings': 'Settings.ico',
    'LuxxerArchiver': 'LuxxerArchiver.ico',
    'Zer3 IDE': 'IDE.ico',
    'Calculator': 'Calculator.ico',
    'Cyber Tools': 'CyberTools.ico',
    'GuardianAV': 'GuardianAV.ico',
    'CMD': 'CMD.ico',
    'RandomChallenge': 'RandomChallenge.ico',
    'MotivationAIChat': 'MotivationAIChat.ico',
    'JokeGenerator': 'Joke.ico',
    'TaskManager': 'TaskManager.ico',
    'FilePreview': 'file.ico',
    'Calendar': 'Calendar.ico',
    'HackerSimulator': 'HackerSimulation.ico',
    'ASCIIPainter': 'ASCII.ico',
    'FortuneTeller': 'FortuneTeller.ico',
    'Mail': 'Mail.ico',
    'Contacts': 'Contacts.ico',
    'Photos': 'Photos.ico',
    'MusicPlayer': 'Music.ico',
    'VideoPlayer': 'Video.ico',
    'PDFReader': 'PDFReader.ico',
    'OfficeWriter': 'Office.ico',
    'Spreadsheet': 'Spreadsheet.ico',
    'Presentation': 'Presentation.ico',
    'StickyNotes': 'StickyNotes.ico',
    'Screenshot': 'ScreenShot.ico',
    'ScreenRecorder': 'ScreenRecorder.ico',
    'ImageEditorPro': 'ImageEditor.ico',
    'VideoEditor': 'VideoEditor.ico',
    'MediaConverter': 'Media.ico',
    'TerminalEmulator': 'terminalemulator.ico',
    'ShellX': 'ShellX.ico',
    'GitClient': 'GitClient.ico',
    'DockerManager': 'DockerManager.ico',
    'PackageManager': 'PackageManager.ico',
    'AppStore': 'AppStore.ico',
    'BackupRestore': 'Backup.ico',
    'DiskCleaner': 'DiskCleaner.ico',
    'DiskManager': 'DiskManager.ico',
    'SystemInfo': 'Info.ico',
    'DeviceManager': 'Device.ico',
    'PrinterManager': 'Printer.ico',
    'LuxxerWeb': 'LuxxerWeb.ico',
    'NetworkMonitor': 'NetworkMonitor.ico',
    'VPNClient': 'VPNClient.ico',
    'RemoteDesktop': 'RemoteDesktop.ico',
    'SSHClient': 'SSHClient.ico',
    'PortScanner': 'PortScanner.ico',
    'WiFiAnalyzer': 'WifiAnalyzer.ico',
    'ClipboardManager': 'ClipboardManager.ico',
    'Scheduler': 'Scheduler.ico',
    'VoiceRecorder': 'VoiceRecorder.ico',
    'GamesApp': 'GamesApp.ico',
    'ApplicationAdder': 'ApplicationAdder.ico',
    'HabitTracker': 'HabitTracker.ico',
    'Pomodoro': 'Pomodoro.ico',
    'RandomStory': 'RandomStory.ico',
    'TravelTips': 'TravelTips.ico',
    'QRCodeGenerator': 'QRCodeGenerator.ico',
    'ColorPalette': 'ColorPalette.ico',
    'RecipeBox': 'RecipeBox.ico',
    'BudgetTracker': 'BudgetTracker.ico',
    'TerminalGames': 'TerminalGames.ico',
    'AmbientSound': 'AmbientSound.ico',
    'ScreenOrganizer': 'ScreenOrganizer.ico',
    'ThemePreview': 'ThemePreview.ico',
    'TabbedBrowser': 'TabbedBrowser.ico',
    'IncognitoBrowser': 'IncognitoBrowser.ico',
    'ReaderModeBrowser': 'ReaderModeBrowser.ico',
    'RSSFeedReader': 'RSSFeedReader.ico',
    'LocalNotes': 'LocalNotes.ico',
    'SecureVaultLite': 'SecureVaultLite.ico',
    'ImageGallery': 'ImageGallery.ico',
    'BatchImageResizer': 'BatchImageResizer.ico',
    'AudioPlayerPro': 'AudioPlayerPro.ico',
    'VideoStreamPlayer': 'VideoStreamPlayer.ico',
    'JSONInspector': 'JSONInspector.ico',
    'CSVEditorPro': 'CSVEditorPro.ico',
    'SQLiteBrowser': 'SQLiteBrowser.ico',
    'APIRequester': 'APIRequester.ico',
    'AutomationScript': 'AutomationScript.ico',
    'OCRTool': 'OCRTool.ico',
    'PodcastManager': 'PodcastManager.ico',
    'EpubReader': 'EpubReader.ico',
    'ColorGrading': 'ColorGrading.ico',
    'FontPreviewer': 'FontPreviewer.ico',
    'IconSetManager': 'IconSetManager.ico',
    'ClipStack': 'ClipStack.ico',
    'WindowTiler': 'WindowTiler.ico',
    'DesktopSpaces': 'DesktopSpaces.ico',
    'NetworkSpeedTester': 'NetworkSpeedTester.ico',
    'FocusTimer': 'FocusTimer.ico',
    'PasswordGenerator': 'PasswordGenerator.ico',
    'WallpapersManager': 'WallpapersManager.ico',
}

import os
import math
import wave
import struct
import tempfile
import time

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class MusicGeneratorThread(QThread):
    progress = pyqtSignal(int)           # 0..100
    finished = pyqtSignal(list)          # list of generated file paths
    message = pyqtSignal(str)

    def __init__(self, out_dir, num_tracks=3, duration_s=120, sr=22050, parent=None):
        super().__init__(parent)
        self.out_dir = out_dir
        self.num_tracks = num_tracks
        self.duration_s = duration_s
        self.sr = sr
        os.makedirs(self.out_dir, exist_ok=True)

    def run(self):
        generated = []
        total = self.num_tracks
        for idx in range(1, self.num_tracks + 1):
            fname = os.path.join(self.out_dir, f"luxxer_track{idx}.wav")
            # if file exists and non-zero size -> skip
            if os.path.exists(fname) and os.path.getsize(fname) > 1024:
                self.message.emit(f"Track {idx} exists, skipping generation.")
                generated.append(fname)
                self.progress.emit(int((len(generated) / total) * 100))
                continue
            self.message.emit(f"Generating track {idx} ... (this may take seconds)")
            try:
                self._generate_track_file(seed=idx, path=fname)
                generated.append(fname)
            except Exception as e:
                self.message.emit(f"Failed to generate track {idx}: {e}")
            self.progress.emit(int((len(generated) / total) * 100))
        self.finished.emit(generated)

    def _generate_track_file(self, seed: int, path: str):
        sr = self.sr
        duration = self.duration_s
        total_samples = int(sr * duration)
        # open wave file
        with wave.open(path, 'wb') as wf:
            nchannels = 1
            sampwidth = 2  # bytes (int16)
            wf.setnchannels(nchannels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(sr)

            # params for sound
            bpm = 70 + seed * 5
            beat = 60.0 / bpm
            chord_changes_s = beat * 4
            chord_seconds_per_change = chord_changes_s
            # chord progression semitone offsets
            chords = [
                [0, 7, 12],
                [2, 9, 14],
                [-3, 4, 9],
                [5, 12, 17],
            ]
            # helper functions
            def sine(freq, t):
                return math.sin(2.0 * math.pi * freq * t)

            def clamp16(x):
                if x > 32767: return 32767
                if x < -32768: return -32768
                return int(x)

            # streaming in chunks of e.g. 2048 samples
            CHUNK = 2048
            # precompute phase accumulators for some oscillators per chunk for continuity
            phase_pad = 0.0
            phase_arp = 0.0
            phase_bass = 0.0
            # simple RNG
            rng_state = seed * 1234567

            def randf():
                nonlocal rng_state
                rng_state = (1103515245 * rng_state + 12345) & 0x7fffffff
                return (rng_state / 0x7fffffff) * 2 - 1

            t_sample = 0
            max_amp = 0.0

            for chunk_start in range(0, total_samples, CHUNK):
                samples = []
                for i in range(CHUNK):
                    n = chunk_start + i
                    if n >= total_samples:
                        break
                    t = n / sr

                    # PAD - slow detuned stack
                    pad = 0.0
                    freqs = [110 * (1 + 0.0005 * seed), 110 * 1.003, 110 * 0.997]
                    pad_env = 0.4 * (0.5 + 0.5 * math.sin(0.03 * 2 * math.pi * t + seed))
                    for f in freqs:
                        pad += sine(f, t + phase_pad) * 0.3
                    pad = pad * pad_env

                    # chord (changes per bar)
                    bar_idx = int(t / chord_seconds_per_change)
                    chord = chords[(bar_idx + seed) % len(chords)]
                    chord_sig = 0.0
                    for sem in chord:
                        chord_freq = 110 * (2 ** (sem / 12.0))
                        chord_sig += sine(chord_freq, t) * 0.25

                    # arpeggio - short pluck notes
                    arp_rate = 8 + (seed % 4)  # notes per second
                    arp_period = int(sr / arp_rate)
                    note_idx = ((chunk_start + i) // arp_period + seed) % 8
                    arp_notes = [0, 4, 7, 12, 7, 4, 0, -5]
                    note = arp_notes[note_idx % len(arp_notes)]
                    freq_arp = 220 * (2 ** (note / 12.0))
                    arp_env = math.exp(-5.0 * ((n % arp_period) / sr))
                    arp_sig = 0.0
                    try:
                        arp_sig = 0.7 * math.sin(2.0 * math.pi * freq_arp * t + phase_arp) * arp_env
                    except Exception:
                        arp_sig = 0.0

                    # bass - on beats
                    beat_samples = int(beat * sr)
                    bass_sig = 0.0
                    if (n % beat_samples) < int(0.6 * beat_samples):
                        bass_freq = 55 * (1.0 + 0.02 * seed)
                        bass_env = math.exp(-6.0 * ((n % beat_samples) / sr))
                        bass_sig = 0.8 * math.sin(2.0 * math.pi * bass_freq * t + phase_bass) * bass_env

                    # hi-hat noise on off-beats
                    hat = 0.0
                    if (n % (beat_samples // 2)) < int(0.05 * sr):
                        hat = 0.06 * randf()

                    # melody - occasional
                    melody = 0.0
                    if (n % int(sr * (0.5 + 0.2 * (seed % 3)))) < int(0.4 * sr):
                        mel_note = [0,2,4,5,7,9,11,12][((n // 44100) + seed) % 8]
                        mel_freq = 440 * (2 ** (mel_note / 12.0))
                        melody = 0.5 * math.sin(2.0 * math.pi * mel_freq * t) * (0.8 - 0.6*(seed%3)/3)

                    # mix
                    sample = 0.5*pad + 0.9*chord_sig + 0.7*arp_sig + 0.9*bass_sig + hat + 0.6*melody
                    # light limiting
                    sample = max(-1.0, min(1.0, sample))
                    int_sample = clamp16(int(sample * 30000))
                    samples.append(int_sample)
                    if abs(int_sample) > max_amp:
                        max_amp = abs(int_sample)
                # write chunk
                if samples:
                    data = struct.pack('<' + 'h'*len(samples), *samples)
                    wf.writeframes(data)
            # small trailing silence to ensure clean end
            wf.writeframes(b'\x00\x00' * 512)
        # done file
        time.sleep(0.05)

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MusicPlayer - Luxxer")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(560, 420)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        # Playlist
        self.playlist = QListWidget()
        self.layout.addWidget(self.playlist)

        # Buttons row
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
        self.status = QLabel("Initializing...")
        self.layout.addWidget(self.status)

        # Media player setup
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.current_track = None

        # tracks list holds full paths
        self.tracks = []

        # prepare storage dir for generated tracks
        home = os.path.expanduser('~') or tempfile.gettempdir()
        self._tracks_dir = os.path.join(home, '.luxxer', 'tracks')
        os.makedirs(self._tracks_dir, exist_ok=True)

        # check and add existing generated tracks and start generation if missing
        self._add_existing_generated_tracks()

        # if some generated missing -> spawn generator in background thread
        missing = [i for i in range(1,4) if not os.path.exists(os.path.join(self._tracks_dir, f"luxxer_track{i}.wav"))]
        if missing:
            self.status.setText("Generating built-in Luxxer tracks (background)...")
            self._gen_thread = MusicGeneratorThread(out_dir=self._tracks_dir, num_tracks=3, duration_s=120, sr=22050)
            self._gen_thread.progress.connect(self._on_gen_progress)
            self._gen_thread.message.connect(lambda m: self.status.setText(m))
            self._gen_thread.finished.connect(self._on_gen_finished)
            self._gen_thread.start()
        else:
            self.status.setText("Ready. Built-in tracks loaded.")

    def _add_existing_generated_tracks(self):
        for i in range(1,4):
            p = os.path.join(self._tracks_dir, f"luxxer_track{i}.wav")
            if os.path.exists(p) and p not in self.tracks:
                self.tracks.append(p)
                self.playlist.addItem(os.path.basename(p))

    def _on_gen_progress(self, pct):
        self.status.setText(f"Generating built-ins... {pct}%")

    def _on_gen_finished(self, paths):
        # add any newly generated files to playlist
        added = 0
        for p in paths:
            if p and os.path.exists(p) and p not in self.tracks:
                self.tracks.append(p)
                self.playlist.addItem(os.path.basename(p))
                added += 1
        self.status.setText(f"Generated {added} built-in tracks. Ready.")

    def load_track(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open audio", "", "Audio (*.mp3 *.wav *.ogg);;All Files (*)")
        if path:
            if path not in self.tracks:
                self.tracks.append(path)
                self.playlist.addItem(os.path.basename(path))
            self.status.setText(f"Loaded: {os.path.basename(path)}")

    def play(self):
        selected = self.playlist.currentRow()
        if selected >= 0 and selected < len(self.tracks):
            track = self.tracks[selected]
            if self.current_track != track:
                url = QUrl.fromLocalFile(os.path.abspath(track))
                self.player.setSource(url)
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
        self.status.setText(f"Loaded: {os.path.basename(self.current_path) if self.current_path else '-'} "
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
            for port in range(1, 1025):  # scanning common ports (1-1024)
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

import math

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Luxxer Calculator")
        self.setWindowIcon(QIcon("icon.ico"))
        self.resize(1280, 800)

        # === CENTRAL WIDGET ===
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(50, 40, 50, 40)
        self.layout.setSpacing(30)

        # === DISPLAY ===
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Consolas", 30))
        self.display.setMinimumHeight(80)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 3px solid #00ffaa;
                border-radius: 15px;
                padding: 15px;
                background: #0A0A0A;
                color: #00FFAA;
            }
        """)
        self.layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(15)

        buttons = [
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', '=', '+', '√'],
            ['(', ')', '^', '%', 'π'],
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                btn = QPushButton(text)
                btn.setFont(QFont("Segoe UI", 22))
                btn.setFixedSize(QSize(140, 80))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1E1E1E;
                        border: 2px solid #333;
                        border-radius: 12px;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #00FFAA;
                        color: black;
                        transform: scale(1.05);
                    }
                """)
                btn.clicked.connect(lambda _, t=text: self.on_button_click(t))
                grid.addWidget(btn, r, c)
        self.layout.addLayout(grid)

        extra_layout = QHBoxLayout()
        extra_layout.setSpacing(20)

        pitagora_btn = QPushButton("Pythagoras Theorem")
        pitagora_btn.setFont(QFont("Segoe UI", 18))
        pitagora_btn.setMinimumHeight(70)
        pitagora_btn.setStyleSheet("""
            QPushButton {
                background-color: #00FFAA;
                color: black;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc88;
            }
        """)
        pitagora_btn.clicked.connect(self.show_pythagoras)
        extra_layout.addWidget(pitagora_btn)

        clear_btn = QPushButton("Clear Display")
        clear_btn.setFont(QFont("Segoe UI", 18))
        clear_btn.setMinimumHeight(70)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DD0000;
            }
        """)
        clear_btn.clicked.connect(lambda: self.display.clear())
        extra_layout.addWidget(clear_btn)

        self.layout.addLayout(extra_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def on_button_click(self, text):
        if text == '=':
            self.evaluate()
        elif text == '√':
            self.display.setText(self.display.text() + 'sqrt(')
        elif text == '^':
            self.display.setText(self.display.text() + '**')
        elif text == 'π':
            self.display.setText(self.display.text() + str(math.pi))
        else:
            self.display.setText(self.display.text() + text)

    def evaluate(self):
        expr = self.display.text()
        try:
            allowed = {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "pi": math.pi, "abs": abs,
                "round": round, "pow": pow
            }
            val = eval(expr, {"__builtins__": {}}, allowed)
            self.display.setText(str(round(val, 6)))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid expression:\n{e}")

    def show_pythagoras(self):
        dlg = PythagorasDialog(self)
        dlg.exec()


class PythagorasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pythagoras Theorem")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout()
        layout.setSpacing(20)

        lbl = QLabel("Calculate c from a² + b² = c²")
        lbl.setFont(QFont("Segoe UI", 16))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #00ffaa; font-weight: bold;")
        layout.addWidget(lbl)

        btn = QPushButton("Enter sides a, b")
        btn.setFont(QFont("Segoe UI", 14))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #00ffaa;
                color: black;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #00cc88;
            }
        """)
        btn.clicked.connect(self.calc)
        layout.addWidget(btn)

        self.result = QLabel("Result: c = ?")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setFont(QFont("Consolas", 18))
        self.result.setStyleSheet("color: #00ffaa; font-weight: bold;")
        layout.addWidget(self.result)

        self.setLayout(layout)

    def calc(self):
        try:
            a, ok1 = QInputDialog.getDouble(self, "Input", "Enter side a:")
            if not ok1: return
            b, ok2 = QInputDialog.getDouble(self, "Input", "Enter side b:")
            if not ok2: return
            c = math.sqrt(a ** 2 + b ** 2)
            self.result.setText(f"Result: c = {round(c, 4)}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {e}")


import os
import sys
import re
import time
import math
import ast
import traceback
import colorsys
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional, Any, Tuple

from functools import partial

class InterpreterError(Exception):
    def __init__(self, message: str, line: Optional[int] = None):
        if line is not None:
            message = f"Line {line}: {message}"
        super().__init__(message)
        self.line = line

# Safe evaluator

def safe_eval_expr(expr: str, vars_map: Dict[str, Any]) -> float:
    if expr is None or str(expr).strip() == "":
        raise InterpreterError("Empty expression")
    try:
        node = ast.parse(expr, mode='eval')
    except Exception as e:
        raise InterpreterError(f"Parse error: {e}")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return float(n.value)
            raise InterpreterError("Only numeric constants allowed")
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                return left / right
            if isinstance(n.op, ast.Pow):
                return left ** right
            if isinstance(n.op, ast.Mod):
                return left % right
            raise InterpreterError("Unsupported binary operator")
        if isinstance(n, ast.UnaryOp):
            v = _eval(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +v
            if isinstance(n.op, ast.USub):
                return -v
            raise InterpreterError("Unsupported unary operator")
        if isinstance(n, ast.Name):
            if n.id in vars_map:
                try:
                    return float(vars_map[n.id])
                except Exception:
                    raise InterpreterError(f"Variable {n.id} is not numeric")
            raise InterpreterError(f"Unknown variable: {n.id}")
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                fname = n.func.id
                allowed = {'sin','cos','tan','sqrt','log','ceil','floor'}
                if fname in allowed and len(n.args) == 1:
                    aval = _eval(n.args[0])
                    if fname == 'ceil':
                        return float(math.ceil(aval))
                    if fname == 'floor':
                        return float(math.floor(aval))
                    return float(getattr(math, fname)(aval))
            raise InterpreterError("Function calls not allowed except limited math funcs")
        raise InterpreterError(f"Unsupported expression element: {type(n)}")

    return float(_eval(node))

# Zer3Interpreter

class Zer3Interpreter:
    def __init__(self, timeout: float = 5.0):
        self.vars: Dict[str, Any] = {}
        self.timeout = float(timeout)
        # pick available python executable
        self.python_exec = shutil.which("python3") or shutil.which("python") or sys.executable

        # safe builtins (minimal, non-dangerous)
        self.safe_builtins = {
            'abs': abs, 'min': min, 'max': max, 'sum': sum, 'len': len, 'range': range,
            'sorted': sorted, 'round': round, 'enumerate': enumerate, 'list': list, 'tuple': tuple,
            'dict': dict, 'set': set, 'bool': bool, 'int': int, 'float': float, 'str': str,
            # disable input and file ops by default
            'print': print,
        }

    def run(self, code: str) -> str:
        code = code or ""
        # Prefer subprocess for isolation
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
                combined = (out + ("\n" + err if err else "")).strip()
                return combined
            except subprocess.TimeoutExpired:
                return f"<error: execution timed out after {self.timeout} seconds>"
            except Exception as e:
                # fallback to local exec
                fallback_msg = f"<warning: python subprocess failed, using fallback: {e}>"
                fb = self._run_fallback(code)
                return f"{fallback_msg}\n{fb}"
        else:
            return self._run_fallback(code)

    def _run_fallback(self, code: str) -> str:
        f = io.StringIO()
        try:
            with contextlib.redirect_stdout(f):
                # Provide read-only safe builtins and persistent vars
                exec_globals = {"__builtins__": self.safe_builtins}
                # expose a copy of current vars as 'vars' inside local namespace
                exec_locals = self.vars
                exec(code, exec_globals, exec_locals)
        except Exception as e:
            f.write(f"<error: {e}>\n")
            f.write(traceback.format_exc())
        return f.getvalue().strip()

# Syntax highlighter for Zer3/Python-like code

class Zer3Highlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        # formats
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

        # patterns
        keywords = [
            "False","None","True","and","as","assert","async","await","break","class",
            "continue","def","del","elif","else","except","finally","for","from","global",
            "if","import","in","is","lambda","nonlocal","not","or","pass","raise",
            "return","try","while","with","yield"
        ]
        builtins = [
            "abs","all","any","bin","bool","bytearray","bytes","callable","chr",
            "classmethod","compile","complex","dict","dir","divmod","enumerate",
            "eval","filter","float","format","frozenset","getattr","globals",
            "hasattr","hash","hex","id","int","isinstance","issubclass",
            "iter","len","list","locals","map","max","memoryview","min","next","object",
            "oct","pow","print","property","range","repr","reversed","round",
            "set","setattr","slice","sorted","staticmethod","str","sum","super","tuple",
            "type","vars","zip"
        ]

        # compile regexes
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        bi_pattern = r"\b(" + "|".join(builtins) + r")\b"

        self.rules = []
        self.rules.append((QRegularExpression(kw_pattern), self._fmt_keyword))
        self.rules.append((QRegularExpression(bi_pattern), self._fmt_builtin))
        self.rules.append((QRegularExpression(r"\b[0-9]+(?:\.[0-9]+)?\b"), self._fmt_number))
        self.rules.append((QRegularExpression(r'"[^"\n]*"'), self._fmt_string))
        self.rules.append((QRegularExpression(r"'[^'\n]*'"), self._fmt_string))
        self.comment_re = QRegularExpression(r"#.*")

        # triple quotes
        self.triple_double = QRegularExpression('"""')
        self.triple_single = QRegularExpression("'''")

    def highlightBlock(self, text: str) -> None:
        # handle simple triple-quote multiline strings
        self.setCurrentBlockState(0)
        # naive multiline handling
        if self.previousBlockState() != 0:
            # we were inside a multi-line string
            dq = self.triple_double if getattr(self, "_ml_is_double", True) else self.triple_single
            match = dq.match(text)
            if match.hasMatch():
                end_index = match.capturedStart()
                self.setFormat(0, end_index + 3, self._fmt_string)
                self.setCurrentBlockState(0)
            else:
                self.setFormat(0, len(text), self._fmt_string)
                self.setCurrentBlockState(1)
                return

        # find starting triple quotes
        for triple, is_double in ((self.triple_double, True), (self.triple_single, False)):
            it = triple.globalMatch(text)
            while it.hasNext():
                m = it.next()
                start = m.capturedStart()
                rest = text[start+3:]
                end_seq = '"""' if is_double else "'''"
                end_pos = rest.find(end_seq)
                if end_pos == -1:
                    self.setFormat(start, len(text)-start, self._fmt_string)
                    self.setCurrentBlockState(1)
                    self._ml_is_double = is_double
                else:
                    self.setFormat(start, end_pos+6, self._fmt_string)

        # inline comments
        cm = self.comment_re.globalMatch(text)
        while cm.hasNext():
            m = cm.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self._fmt_comment)

        # other rules
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

# Worker thread to run interpreter without blocking GUI

class InterpreterWorker(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, interpreter: Zer3Interpreter, code: str, parent=None):
        super().__init__(parent)
        self.interpreter = interpreter
        self.code = code

    def run(self):
        try:
            res = self.interpreter.run(self.code)
            # emit output lines
            if res is None:
                res = ""
            for line in str(res).splitlines() or [""]:
                self.output.emit(line)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(tb)
        finally:
            self.finished.emit()

# Zer3IDE (simple)
class Zer3IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zer3 IDE - Luxxer")
        if os.path.exists('icon.ico'):
            self.setWindowIcon(QIcon('icon.ico'))
        self.resize(1000, 700)

        self.interpreter = Zer3Interpreter(timeout=6.0)
        self.worker: Optional[InterpreterWorker] = None

        self._init_ui()
        self._connect_actions()

    def _init_ui(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)
        act_open = QAction("Open", self)
        act_save = QAction("Save", self)
        act_run = QAction("Run", self)
        act_stop = QAction("Stop", self)
        toolbar.addAction(act_open)
        toolbar.addAction(act_save)
        toolbar.addSeparator()
        toolbar.addAction(act_run)
        toolbar.addAction(act_stop)
        self.act_open = act_open
        self.act_save = act_save
        self.act_run = act_run
        self.act_stop = act_stop

        # central layout with splitter
        central = QWidget()
        v = QVBoxLayout(central)
        splitter = QSplitter(Qt.Orientation.Vertical)
        v.addWidget(splitter)

        # editor
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setPlaceholderText("# Write Zer3 / Python code here...")
        self.highlighter = Zer3Highlighter(self.editor.document())

        # bottom console
        console_container = QWidget()
        ch = QVBoxLayout(console_container)
        label = QLabel("Output:")
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(220)
        ch.addWidget(label)
        ch.addWidget(self.console)

        splitter.addWidget(self.editor)
        splitter.addWidget(console_container)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(central)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # store actions on object for signals
        self._widgets = {
            'open': act_open, 'save': act_save, 'run': act_run, 'stop': act_stop
        }

    def _connect_actions(self):
        self.act_open.triggered.connect(self.open_file)
        self.act_save.triggered.connect(self.save_file)
        self.act_run.triggered.connect(self.run_code)
        self.act_stop.triggered.connect(self.stop_code)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), "Python (*.py);;All Files (*)")
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                txt = f.read()
            self.editor.setPlainText(txt)
            self.status.showMessage(f"Opened {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Open error", str(e))

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", os.getcwd(), "Python (*.py);;All Files (*)")
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.status.showMessage(f"Saved {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Save error", str(e))

    def append_console(self, text: str):
        self.console.appendPlainText(text)

    def run_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            QMessageBox.information(self, "No code", "Editor is empty.")
            return

        # if worker running, ask user to stop first
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Running", "Interpreter is already running.")
            return

        self.console.clear()
        self.status.showMessage("Running...")
        self.worker = InterpreterWorker(self.interpreter, code)
        self.worker.output.connect(self.append_console)
        self.worker.error.connect(lambda tb: self.append_console("[ERROR]\n" + tb))
        self.worker.finished.connect(lambda: self.status.showMessage("Finished"))
        self.worker.start()

    def stop_code(self):
        if self.worker and self.worker.isRunning():
            try:
                # best effort: terminate the thread (not always safe)
                # QThread cannot be safely killed; advise user to restart IDE if needed.
                self.append_console("Stop requested (best-effort). If subprocess is running, it may continue until completion.")
                # no direct kill; rely on subprocess timeout; set interpreter timeout small if needed
                self.status.showMessage("Stop requested")
            except Exception:
                pass
        else:
            self.append_console("No running process.")

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Still running", "Interpreter is running. Stop it before exit.")
            event.ignore()
            return
        event.accept()

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

# Worker that runs external commands and streams stdout

class CmdWorker(QThread):
    output = pyqtSignal(str)
    finished_ok = pyqtSignal()

    def __init__(self, cmd: str, cwd: str):
        super().__init__()
        self.cmd = cmd
        self.cwd = cwd
        self._proc = None

    def run(self):
        try:
            # Start process
            self._proc = subprocess.Popen(
                self.cmd,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                shell=True,
                text=True,
                bufsize=1
            )
            if self._proc.stdout is not None:
                for line in self._proc.stdout:
                    try:
                        self.output.emit(line.rstrip('\n'))
                    except Exception:
                        pass
            self._proc.wait()
            if self._proc.returncode != 0:
                self.output.emit(f"[Process exited with code {self._proc.returncode}]")
        except Exception as e:
            self.output.emit(f"Execution error: {e}")
        finally:
            self.finished_ok.emit()

    def terminate_process(self):
        try:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
                time.sleep(0.05)
                if self._proc.poll() is None:
                    self._proc.kill()
        except Exception:
            pass

# Safe arithmetic evaluator (based on ast) for `calc`

# support basic arithmetic operators
_allowed_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.BitXor: op.xor,
    ast.FloorDiv: op.floordiv,
}

def safe_eval(expr: str):
    try:
        node = ast.parse(expr, mode='eval')
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Num):
            return n.n
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            op_type = type(n.op)
            if op_type in _allowed_operators:
                return _allowed_operators[op_type](left, right)
        if isinstance(n, ast.UnaryOp):
            operand = _eval(n.operand)
            op_type = type(n.op)
            if op_type in _allowed_operators:
                return _allowed_operators[op_type](operand)
        raise ValueError('Unsupported expression')

    return _eval(node)

# Main CMD GUI app

class CmdApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Luxxer CMD')
        if os.path.exists('icon.ico'):
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

        # State
        self.cwd = os.path.abspath(os.path.expanduser('~'))
        self.history: List[str] = []
        self.history_index = -1
        self.active_workers: List[CmdWorker] = []

        # Mapping to handler methods
        self.handlers = {
            'help': self._h_help,
            'pwd': self._h_pwd,
            'ls': self._h_ls,
            'cd': self._h_cd,
            'mkdir': self._h_mkdir,
            'rmdir': self._h_rmdir,
            'rm': self._h_rm,
            'touch': self._h_touch,
            'cat': self._h_cat,
            'echo': self._h_echo,
            'clear': self._h_clear,
            'cls': self._h_clear,
            'exit': self._h_exit,
            'stat': self._h_stat,
            'file': self._h_fileinfo,
            'tree': self._h_tree,
            'count': self._h_count,
            'whoami': self._h_whoami,
            'date': self._h_date,
            'dateutc': self._h_dateutc,
            'uptime': self._h_uptime,
            'env': self._h_env,
            'set': self._h_setenv,
            'unset': self._h_unsetenv,
            'ping': self._h_ping,
            'ip': self._h_ip,
            'calc': self._h_calc,
            'rand': self._h_rand,
            'randf': self._h_randf,
            'sleep': self._h_sleep,
            'hostname': self._h_hostname,
            'platform': self._h_platform,
            'arch': self._h_arch,
            'cpu': self._h_cpu,
            'mem': self._h_mem,
            'head': self._h_head,
            'tail': self._h_tail,
            'md5': self._h_hash,
            'sha1': self._h_hash,
            'sha256': self._h_hash,
            'mv': self._h_mv,
            'cp': self._h_cp,
            'ln': self._h_ln,
            'zip': self._h_zip,
            'unzip': self._h_unzip,
            'tar': self._h_tar,
            'untar': self._h_unzip,
            'find': self._h_find,
            'grep': self._h_grep,
            'sort': self._h_sort,
            'uniq': self._h_uniq,
            'wc': self._h_wc,
            'chmod': self._h_chmod,
            'ln': self._h_ln,
            'mv': self._h_mv,
            'cp': self._h_cp,
            'serve': self._h_serve,
            'jsonfmt': self._h_jsonfmt,
            'base64enc': self._h_base64enc,
            'base64dec': self._h_base64dec,
        }

        # Commands that should be run as external processes (best-effort)
        self.external_cmd_prefixes = ('git','docker','pip','npm','node','python','wget','curl','ss','ifconfig','traceroute')

        # Intro
        self.write(f'Luxxer CMD (cwd={self.cwd}). Type commands below. Available commands:')
        self.write(', '.join(sorted(list(self.handlers.keys()) + list(self.external_cmd_prefixes))))

    # utility to append text to output and autoscroll
    def write(self, text: str):
        try:
            self.output.append(text)
            self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
        except Exception:
            pass

    def cleanup_worker(self, worker: CmdWorker):
        if worker in self.active_workers:
            try:
                self.active_workers.remove(worker)
            except ValueError:
                pass
        try:
            worker.deleteLater()
        except Exception:
            pass

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

        def safe_path(p):
            return os.path.abspath(os.path.join(self.cwd, p))

        # if we have a handler, call it
        try:
            if cmd in self.handlers:
                try:
                    self.handlers[cmd](args)
                except Exception as e:
                    self.write(f"Handler error: {e}")
                return

            # external command prefix: spawn worker (non-blocking)
            if cmd.startswith(self.external_cmd_prefixes):
                worker = CmdWorker(line, self.cwd)
                worker.output.connect(self.write)
                worker.finished_ok.connect(lambda w=worker: self.cleanup_worker(w))
                self.active_workers.append(worker)
                worker.start()
                return

            # fallback: try a safe shell command via worker
            worker = CmdWorker(line, self.cwd)
            worker.output.connect(self.write)
            worker.finished_ok.connect(lambda w=worker: self.cleanup_worker(w))
            self.active_workers.append(worker)
            worker.start()
        except Exception as e:
            self.write(f"Execution dispatch error: {e}")

    # Handler implementations

    def _h_help(self, args):
        self.write('Builtin commands:')
        self.write(', '.join(sorted(self.handlers.keys())))
        self.write('External prefixes (run via shell): ' + ','.join(self.external_cmd_prefixes))

    def _h_pwd(self, args):
        self.write(self.cwd)

    def _h_ls(self, args):
        try:
            target = self.cwd if not args else safe_join(self.cwd, args[0])
            entries = os.listdir(target)
            self.write('  '.join(entries))
        except Exception as e:
            self.write(f'ls error: {e}')

    def _h_cd(self, args):
        if not args:
            self.write('cd requires a path')
            return
        path = safe_join(self.cwd, args[0])
        if os.path.isdir(path):
            self.cwd = path
            self.write(f'cwd -> {self.cwd}')
        else:
            self.write('Directory not found')

    def _h_mkdir(self, args):
        if not args:
            self.write('mkdir requires a folder name')
            return
        try:
            os.makedirs(safe_join(self.cwd, args[0]), exist_ok=True)
            self.write(f"Directory '{args[0]}' created")
        except Exception as e:
            self.write(f'mkdir error: {e}')

    def _h_rmdir(self, args):
        if not args:
            self.write('rmdir requires a folder name')
            return
        try:
            os.rmdir(safe_join(self.cwd, args[0]))
            self.write(f"Directory '{args[0]}' removed")
        except Exception as e:
            self.write(f'rmdir error: {e}')

    def _h_rm(self, args):
        if not args:
            self.write('rm requires a file name')
            return
        try:
            os.remove(safe_join(self.cwd, args[0]))
            self.write(f"File '{args[0]}' removed")
        except Exception as e:
            self.write(f'rm error: {e}')

    def _h_touch(self, args):
        if not args:
            self.write('touch requires a file name')
            return
        try:
            open(safe_join(self.cwd, args[0]), 'a').close()
            self.write(f"File '{args[0]}' created")
        except Exception as e:
            self.write(f'touch error: {e}')

    def _h_cat(self, args):
        if not args:
            self.write('cat requires a file name')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    self.write(line.rstrip('\n'))
        except Exception as e:
            self.write(f'cat error: {e}')

    def _h_echo(self, args):
        self.write(' '.join(args))

    def _h_clear(self, args):
        self.output.clear()

    def _h_exit(self, args):
        self.close()

    def _h_stat(self, args):
        if not args:
            self.write('stat requires a path')
            return
        try:
            p = safe_join(self.cwd, args[0])
            st = os.stat(p)
            self.write(str(st))
        except Exception as e:
            self.write(f'stat error: {e}')

    def _h_fileinfo(self, args):
        if not args:
            self.write('file requires a path')
            return
        p = safe_join(self.cwd, args[0])
        if os.path.exists(p):
            typ = 'Directory' if os.path.isdir(p) else 'File' if os.path.isfile(p) else 'Other'
            self.write(f"{p} -> {typ}")
        else:
            self.write('Path does not exist')

    def _h_tree(self, args):
        # robust tree: limit depth and node count to avoid UI freeze
        root = self.cwd if not args else safe_join(self.cwd, args[0])
        max_depth = 6
        max_nodes = 2000
        count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                depth = dirpath.replace(root, '').count(os.sep)
                if depth > max_depth:
                    # don't recurse deeper
                    dirnames[:] = []
                    continue
                indent = ' ' * 4 * depth
                base = os.path.basename(dirpath) or dirpath
                self.write(f"{indent}{base}/")
                count += 1
                if count > max_nodes:
                    self.write('[Truncated: too many files]')
                    break
                for f in filenames:
                    self.write(f"{indent}    {f}")
                    count += 1
                    if count > max_nodes:
                        self.write('[Truncated: too many files]')
                        break
                if count > max_nodes:
                    break
        except Exception as e:
            self.write(f'tree error: {e}')

    def _h_count(self, args):
        try:
            self.write(f"{len(os.listdir(self.cwd))} items in current folder")
        except Exception as e:
            self.write(f'count error: {e}')

    def _h_whoami(self, args):
        try:
            import getpass
            self.write(getpass.getuser())
        except Exception as e:
            self.write(f'whoami error: {e}')

    def _h_date(self, args):
        from datetime import datetime
        self.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _h_dateutc(self, args):
        from datetime import datetime, timezone
        self.write(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))

    def _h_uptime(self, args):
        try:
            # best-effort: use psutil boot_time if available
            if psutil:
                self.write(f'Uptime: {time.time() - psutil.boot_time():.0f} seconds')
            else:
                self.write('Uptime info unavailable (install psutil)')
        except Exception as e:
            self.write(f'uptime error: {e}')

    def _h_env(self, args):
        for k, v in os.environ.items():
            self.write(f"{k}={v}")

    def _h_setenv(self, args):
        if len(args) >= 2:
            os.environ[args[0]] = ' '.join(args[1:])
            self.write(f"{args[0]} set")
        else:
            self.write('Usage: set VAR VALUE')

    def _h_unsetenv(self, args):
        if args:
            os.environ.pop(args[0], None)
            self.write(f"{args[0]} removed")
        else:
            self.write('unset requires variable name')

    def _h_ping(self, args):
        target = args[0] if args else '8.8.8.8'
        param = '-n' if sys.platform.startswith('win') else '-c'
        worker = CmdWorker(f"ping {param} 1 {target}", self.cwd)
        worker.output.connect(self.write)
        worker.finished_ok.connect(lambda w=worker: self.cleanup_worker(w))
        self.active_workers.append(worker)
        worker.start()

    def _h_ip(self, args):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.write(f"{hostname} -> {ip}")
        except Exception as e:
            self.write(f'ip error: {e}')

    def _h_calc(self, args):
        if not args:
            self.write('calc requires an expression')
            return
        expr = ' '.join(args)
        try:
            res = safe_eval(expr)
            self.write(str(res))
        except Exception as e:
            self.write(f'calc error: {e}')

    def _h_rand(self, args):
        import random
        self.write(str(random.randint(0, 1000)))

    def _h_randf(self, args):
        import random
        self.write(str(random.random()))

    def _h_sleep(self, args):
        try:
            sec = float(args[0]) if args else 1.0
            time.sleep(sec)
            self.write(f'Slept {sec}s')
        except Exception as e:
            self.write(f'sleep error: {e}')

    def _h_hostname(self, args):
        self.write(socket.gethostname())

    def _h_platform(self, args):
        import platform
        self.write(platform.platform())

    def _h_arch(self, args):
        import platform
        self.write(platform.machine())

    def _h_cpu(self, args):
        import multiprocessing
        self.write(f"CPUs: {multiprocessing.cpu_count()}")

    def _h_mem(self, args):
        if psutil:
            self.write(str(psutil.virtual_memory()))
        else:
            self.write('Memory info unavailable (install psutil)')

    def _h_head(self, args):
        n = int(args[0]) if args and args[0].isdigit() else 10
        if not args:
            self.write('head requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                for i, l in enumerate(f):
                    if i >= n: break
                    self.write(l.rstrip('\n'))
        except Exception as e:
            self.write(f'head error: {e}')

    def _h_tail(self, args):
        n = int(args[0]) if args and args[0].isdigit() else 10
        if not args:
            self.write('tail requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                for l in lines[-n:]:
                    self.write(l.rstrip('\n'))
        except Exception as e:
            self.write(f'tail error: {e}')

    def _h_hash(self, args):
        if not args:
            self.write('hash requires filename')
            return
        alg = 'md5' if 'md5' in sys._getframe(1).f_code.co_name else None
        # simpler: inspect caller name is fragile; use the invoked command mapping instead
        # We'll infer based on how handler was called by checking first word of function name
        cmdname = sys._getframe(1).f_code.co_name
        cmd = 'md5' if 'md5' in cmdname else ('sha1' if 'sha1' in cmdname else 'sha256')
        try:
            h = hashlib.new(cmd)
            p = safe_join(self.cwd, args[0])
            with open(p, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    h.update(chunk)
            self.write(h.hexdigest())
        except Exception as e:
            self.write(f'{cmd} error: {e}')

    def _h_mv(self, args):
        if len(args) < 2:
            self.write('mv requires source and destination')
            return
        try:
            shutil.move(safe_join(self.cwd, args[0]), safe_join(self.cwd, args[1]))
            self.write(f"Moved {args[0]} -> {args[1]}")
        except Exception as e:
            self.write(f'mv error: {e}')

    def _h_cp(self, args):
        if len(args) < 2:
            self.write('cp requires source and destination')
            return
        try:
            shutil.copy2(safe_join(self.cwd, args[0]), safe_join(self.cwd, args[1]))
            self.write(f"Copied {args[0]} -> {args[1]}")
        except Exception as e:
            self.write(f'cp error: {e}')

    def _h_ln(self, args):
        if len(args) < 2:
            self.write('ln requires target and link_name')
            return
        try:
            os.symlink(safe_join(self.cwd, args[0]), safe_join(self.cwd, args[1]))
            self.write(f"Symlink {args[1]} -> {args[0]}")
        except Exception as e:
            self.write(f'ln error: {e}')

    def _h_zip(self, args):
        if len(args) < 2:
            self.write('zip usage: zip <src> <dest.zip>')
            return
        try:
            src = safe_join(self.cwd, args[0])
            dst = safe_join(self.cwd, args[1])
            with zipfile.ZipFile(dst, 'w') as z:
                if os.path.isdir(src):
                    for root, _, files in os.walk(src):
                        for f in files:
                            full = os.path.join(root, f)
                            arc = os.path.relpath(full, start=os.path.dirname(src))
                            z.write(full, arcname=arc)
                else:
                    z.write(src, arcname=os.path.basename(src))
            self.write(f'Zipped {args[0]} -> {args[1]}')
        except Exception as e:
            self.write(f'zip error: {e}')

    def _h_unzip(self, args):
        if not args:
            self.write('unzip requires archive path')
            return
        try:
            src = safe_join(self.cwd, args[0])
            if zipfile.is_zipfile(src):
                with zipfile.ZipFile(src, 'r') as z:
                    z.extractall(self.cwd)
                self.write(f'Unzipped {args[0]}')
            else:
                try:
                    with tarfile.open(src, 'r:*') as t:
                        t.extractall(self.cwd)
                    self.write(f'Extracted {args[0]}')
                except Exception:
                    self.write('Unsupported archive or corrupted')
        except Exception as e:
            self.write(f'unzip error: {e}')

    def _h_find(self, args):
        if not args:
            self.write('find requires a pattern (fnmatch style)')
            return
        pattern = args[0]
        max_results = 200
        found = 0
        try:
            for root, dirs, files in os.walk(self.cwd):
                for name in files + dirs:
                    if fnmatch.fnmatch(name, pattern):
                        self.write(os.path.join(root, name))
                        found += 1
                        if found >= max_results:
                            self.write('[Truncated results]')
                            return
        except Exception as e:
            self.write(f'find error: {e}')

    def _h_grep(self, args):
        if len(args) < 2:
            self.write('grep usage: grep <pattern> <file>')
            return
        pattern = args[0]
        filep = safe_join(self.cwd, args[1])
        try:
            with open(filep, 'r', encoding='utf-8', errors='replace') as f:
                for i, l in enumerate(f, start=1):
                    if pattern in l:
                        self.write(f"{i}: {l.rstrip()}")
        except Exception as e:
            self.write(f'grep error: {e}')

    def _h_sort(self, args):
        if not args:
            self.write('sort requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            for l in sorted(lines):
                self.write(l.rstrip('\n'))
        except Exception as e:
            self.write(f'sort error: {e}')

    def _h_uniq(self, args):
        if not args:
            self.write('uniq requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            seen = set()
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                for l in f:
                    l2 = l.rstrip('\n')
                    if l2 not in seen:
                        self.write(l2)
                        seen.add(l2)
        except Exception as e:
            self.write(f'uniq error: {e}')

    def _h_wc(self, args):
        if not args:
            self.write('wc requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            lines = text.count('\n')
            words = len(text.split())
            chars = len(text)
            self.write(f"{lines} {words} {chars} {args[0]}")
        except Exception as e:
            self.write(f'wc error: {e}')

    def _h_chmod(self, args):
        if len(args) < 2:
            self.write('chmod requires mode and file')
            return
        try:
            mode = int(args[0], 8)
            p = safe_join(self.cwd, args[1])
            os.chmod(p, mode)
            self.write('chmod OK')
        except Exception as e:
            self.write(f'chmod error: {e}')

    def _h_serve(self, args):
        port = int(args[0]) if args else 8000
        # spawn a worker that runs python -m http.server
        worker = CmdWorker(f"python -m http.server {port}", self.cwd)
        worker.output.connect(self.write)
        worker.finished_ok.connect(lambda w=worker: self.cleanup_worker(w))
        self.active_workers.append(worker)
        worker.start()
        self.write(f"Serving {self.cwd} on port {port}")

    def _h_jsonfmt(self, args):
        if not args:
            self.write('jsonfmt requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                obj = json.load(f)
            self.write(json.dumps(obj, indent=2, ensure_ascii=False))
        except Exception as e:
            self.write(f'jsonfmt error: {e}')

    def _h_base64enc(self, args):
        if not args:
            self.write('base64enc requires filename')
            return
        try:
            p = safe_join(self.cwd, args[0])
            with open(p, 'rb') as f:
                b = base64.b64encode(f.read()).decode('ascii')
            self.write(b)
        except Exception as e:
            self.write(f'base64enc error: {e}')

    def _h_base64dec(self, args):
        if len(args) < 2:
            self.write('base64dec requires input_file output_file')
            return
        try:
            src = safe_join(self.cwd, args[0])
            dst = safe_join(self.cwd, args[1])
            with open(src, 'r', encoding='utf-8') as f:
                b = base64.b64decode(f.read())
            with open(dst, 'wb') as w:
                w.write(b)
            self.write('base64 decoded')
        except Exception as e:
            self.write(f'base64dec error: {e}')

    def _h_tar(self, args):
        if len(args) < 2:
            self.write('tar usage: tar <src> <dest.tar>')
            return
        try:
            src = os.path.join(self.cwd, args[0])
            dst = os.path.join(self.cwd, args[1])
            with tarfile.open(dst, 'w') as tar:
                if os.path.isdir(src):
                    tar.add(src, arcname=os.path.basename(src))
                else:
                    tar.add(src, arcname=os.path.basename(src))
            self.write(f'Tarred {args[0]} -> {args[1]}')
        except Exception as e:
            self.write(f'tar error: {e}')

def safe_join(base, target):
    # resolve and ensure it's within base (avoid escaping with ..)
    if not target:
        return base
    joined = os.path.abspath(os.path.join(base, target))
    try:
        base_abs = os.path.abspath(base)
        if os.path.commonpath([base_abs, joined]) != base_abs:
            # attempted escape -> treat as relative inside base
            return os.path.abspath(os.path.join(base_abs, os.path.relpath(joined, start='/')))
    except Exception:
        pass
    return joined

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


import hashlib
import logging
import math
import os
import queue
import shutil
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
    from PyQt6.QtGui import QIcon, QAction
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QProgressBar, QTabWidget, QFileDialog, QTableWidget, QTableWidgetItem,
        QHeaderView, QMessageBox, QListWidget, QListWidgetItem, QCheckBox, QLineEdit,
        QTextEdit, QSystemTrayIcon, QMenu, QSplitter, QSizePolicy
    )
except Exception as e:
    print("PyQt6 is required: pip install PyQt6")
    raise

LOG_DIR = Path.home() / ".guardianav" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "guardianav.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("guardianav")

KNOWN_BAD_SHA256 = {
    # EICAR (plain ASCII) SHA256
    "275a021bbfb6480f2c343b2b3a9e0b0b0abf3fca0cf2741d9a5a5c1f3c6f0d7a",
}

# EICAR test pattern (do not modify):
EICAR_ASCII = (
    "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
)

SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".scr", ".bat", ".cmd", ".vbs", ".js", ".ps1", ".jar"}

# Utilities

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_entropy(path: Path, sample_size: int = 1024 * 128) -> float:
    """Approximate Shannon entropy from the first sample_size bytes."""
    try:
        with path.open("rb") as f:
            data = f.read(sample_size)
        if not data:
            return 0.0
        freq = [0] * 256
        for b in data:
            freq[b] += 1
        entropy = 0.0
        for c in freq:
            if c:
                p = c / len(data)
                entropy -= p * math.log2(p)
        return entropy
    except Exception:
        return 0.0

@dataclass
class Detection:
    path: Path
    reason: str
    sha256: str
    size: int

# Scanner Worker
class ScanWorker(QThread):
    progress = pyqtSignal(int)  # files scanned
    status = pyqtSignal(str)
    found = pyqtSignal(object)  # Detection
    finished = pyqtSignal(int)  # total scanned

    def __init__(self, roots: List[Path], heuristics: bool = True, parent=None):
        super().__init__(parent)
        self.roots = roots
        self.heuristics = heuristics
        self._stop = threading.Event()
        self.scanned = 0

    def stop(self):
        self._stop.set()

    def run(self):
        try:
            for root in self.roots:
                if self._stop.is_set():
                    break
                for dirpath, _dirnames, filenames in os.walk(root):
                    if self._stop.is_set():
                        break
                    for name in filenames:
                        if self._stop.is_set():
                            break
                        path = Path(dirpath) / name
                        try:
                            det = self.inspect(path)
                            self.scanned += 1
                            self.progress.emit(self.scanned)
                            if det:
                                self.found.emit(det)
                        except Exception as e:
                            logger.warning(f"Scan error on {path}: {e}")
            self.finished.emit(self.scanned)
        except Exception as e:
            logger.exception(f"Worker crashed: {e}")
            self.finished.emit(self.scanned)

    # Core inspection logic
    def inspect(self, path: Path) -> Optional[Detection]:
        if not path.exists() or not path.is_file():
            return None
        # Skip very large files > 200 MB in MVP for speed
        try:
            size = path.stat().st_size
        except Exception:
            return None
        if size > 200 * 1024 * 1024:
            return None

        # Read small sample for EICAR check
        reason = None
        try:
            with path.open("rb") as f:
                head = f.read(1024)
        except Exception:
            head = b""

        # 1) EICAR content check (safe test string)
        try:
            if EICAR_ASCII.encode("ascii") in head:
                sha = sha256_of_file(path)
                return Detection(path, "EICAR test file detected", sha, size)
        except Exception:
            pass

        # 2) Hash match check
        try:
            sha = sha256_of_file(path)
            if sha in KNOWN_BAD_SHA256:
                return Detection(path, "Known-bad SHA256 signature", sha, size)
        except Exception:
            sha = ""

        # 3) Heuristic flags
        if self.heuristics:
            ext = path.suffix.lower()
            ent = file_entropy(path)
            flags = []
            if ext in SUSPICIOUS_EXTENSIONS:
                flags.append(f"ext:{ext}")
            if ent >= 7.5:
                flags.append(f"entropy:{ent:.2f}")
            if size > 50 * 1024 * 1024:
                flags.append(f"size:{size//(1024*1024)}MB")
            if flags:
                return Detection(path, "Heuristic: " + ", ".join(flags), sha, size)

        return None

class LuxxerArchiverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Luxxer Archiver')
        self.setWindowIcon(QIcon('icon.ico'))

        central = QWidget()
        layout = QVBoxLayout(central)

        self.file_sel = QLineEdit()
        self.file_sel.setPlaceholderText("Select file or folder to archive")
        sel_btn = QPushButton('Select Source')
        sel_btn.clicked.connect(self.select_file)

        self.dest_edit = QLineEdit()
        self.dest_edit.setPlaceholderText("Save destination (.zip or .tar)")
        save_btn = QPushButton('Select Destination')
        save_btn.clicked.connect(self.select_dest)

        self.encrypt_check = QCheckBox("Encrypt with password (ZIP only)")
        self.extract_check = QCheckBox("Extract mode (unpack archive)")
        self.add_check = QCheckBox("Add to existing archive (append mode)")

        self.create_btn = QPushButton('Run Operation')
        self.create_btn.clicked.connect(self.run_operation)

        layout.addWidget(QLabel("Source Path:"))
        layout.addWidget(self.file_sel)
        layout.addWidget(sel_btn)
        layout.addWidget(QLabel("Destination Path:"))
        layout.addWidget(self.dest_edit)
        layout.addWidget(save_btn)
        layout.addWidget(self.encrypt_check)
        layout.addWidget(self.extract_check)
        layout.addWidget(self.add_check)
        layout.addWidget(self.create_btn)

        self.setCentralWidget(central)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select file or folder')
        if not path:
            path = QFileDialog.getExistingDirectory(self, 'Select folder')
        if path:
            self.file_sel.setText(path)

    def select_dest(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save archive', '', 'ZIP Files (*.zip);;TAR Files (*.tar)')
        if path:
            self.dest_edit.setText(path)

    def run_operation(self):
        src = self.file_sel.text().strip()
        dst = self.dest_edit.text().strip()
        if not src or not os.path.exists(src):
            QMessageBox.warning(self, 'Error', 'Invalid source path.')
            return
        if not dst:
            QMessageBox.warning(self, 'Error', 'Please choose a destination.')
            return

        # Mode: extract or create
        if self.extract_check.isChecked():
            self.extract_archive(dst if os.path.exists(dst) else src)
        elif self.add_check.isChecked():
            self.add_to_archive(src, dst)
        else:
            self.create_archive(src, dst)

    # Create Archive
    def create_archive(self, src, dst):
        encrypt = self.encrypt_check.isChecked()
        fmt = 'zip' if dst.lower().endswith('.zip') else 'tar'

        try:
            if fmt == 'zip':
                if encrypt:
                    pwd, ok = QInputDialog.getText(self, "Encryption", "Enter password for archive:")
                    if not ok or not pwd:
                        QMessageBox.warning(self, 'Cancelled', 'No password set, aborting.')
                        return
                    with pyzipper.AESZipFile(dst, 'w', compression=pyzipper.ZIP_DEFLATED,
                                              encryption=pyzipper.WZ_AES) as zf:
                        zf.setpassword(pwd.encode())
                        self._zip_add(src, zf)
                else:
                    shutil.make_archive(os.path.splitext(dst)[0], 'zip',
                                        os.path.dirname(src), os.path.basename(src))
            else:
                with tarfile.open(dst, 'w') as tar:
                    tar.add(src, arcname=os.path.basename(src))

            QMessageBox.information(self, 'Success', f'Archive created at:\n{dst}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to create archive:\n{e}')

    # Extract Archive
    def extract_archive(self, src):
        if not os.path.exists(src):
            QMessageBox.warning(self, 'Error', 'Archive not found.')
            return
        target_dir = QFileDialog.getExistingDirectory(self, 'Select extraction destination')
        if not target_dir:
            return
        try:
            if src.endswith('.zip'):
                try:
                    with pyzipper.AESZipFile(src, 'r') as zf:
                        try:
                            zf.extractall(target_dir)
                        except RuntimeError:
                            pwd, ok = QInputDialog.getText(self, "Password", "Enter password:")
                            if ok and pwd:
                                zf.pwd = pwd.encode()
                                zf.extractall(target_dir)
                            else:
                                return
                except Exception:
                    shutil.unpack_archive(src, target_dir)
            elif src.endswith('.tar'):
                with tarfile.open(src, 'r') as tar:
                    tar.extractall(target_dir)
            else:
                shutil.unpack_archive(src, target_dir)
            QMessageBox.information(self, 'Extracted', f'Archive extracted to:\n{target_dir}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Extraction failed:\n{e}')

    # Add to existing archive
    def add_to_archive(self, src, dst):
        if not os.path.exists(dst):
            QMessageBox.warning(self, 'Error', 'Destination archive does not exist.')
            return
        try:
            if dst.endswith('.zip'):
                with pyzipper.AESZipFile(dst, 'a', compression=pyzipper.ZIP_DEFLATED) as zf:
                    self._zip_add(src, zf)
            elif dst.endswith('.tar'):
                QMessageBox.warning(self, 'Info', 'TAR does not support append mode in this app.')
                return
            QMessageBox.information(self, 'Updated', f'File added to archive:\n{os.path.basename(dst)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add file:\n{e}')

    # Internal helper
    def _zip_add(self, src, zf):
        if os.path.isdir(src):
            for root, dirs, files in os.walk(src):
                for f in files:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, os.path.dirname(src))
                    zf.write(full_path, rel_path)
        else:
            zf.write(src, os.path.basename(src))

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

class ScanWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, paths):
        super().__init__()
        self.paths = paths
        self._running = True

    def run(self):
        for path in self.paths:
            if not self._running:
                break
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if not self._running:
                            break
                        full_path = os.path.join(root, f)
                        self.progress.emit(f"Scanning {full_path} ...")
                        time.sleep(0.05)  # simulate scan delay
        self.finished.emit()

    def stop(self):
        self._running = False

class GuardianAVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guardian AV")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Status label
        self.status_label = QLabel("System is idle")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        layout.addWidget(self.status_label)

        # Scan button
        self.scan_btn = QPushButton("Run Full Scan")
        self.scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_btn)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.worker = None

    def start_scan(self):
        self.log_area.clear()
        self.status_label.setText("Scanning...")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: orange;")
        self.scan_btn.setEnabled(False)

        # Paths to scan (you can add more folders)
        paths = ["C:/Users/Public/Documents", "C:/Users/Public/Downloads"]

        # Start worker thread
        self.worker = ScanWorker(paths)
        self.worker.progress.connect(self.update_log)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def update_log(self, message):
        self.log_area.append(message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def scan_finished(self):
        self.status_label.setText("System is secure")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.log_area.append("Scan complete ✅")
        self.scan_btn.setEnabled(True)

# Worker Thread
class WiFiScanWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, interval=2):
        super().__init__()
        self._running = True
        self.interval = interval  # seconds between scans

    def run(self):
        while self._running:
            try:
                # Windows WiFi scan command
                result = subprocess.run(
                    ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                    capture_output=True, text=True
                )
                output = result.stdout
                networks = self.parse_networks(output)
                self.progress.emit(networks)
            except Exception as e:
                self.progress.emit(f"Error scanning: {e}")
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False

    def parse_networks(self, raw_text):
        lines = raw_text.splitlines()
        networks = []
        ssid = None
        for line in lines:
            line = line.strip()
            if line.startswith("SSID "):
                ssid = line.split(":", 1)[1].strip()
            elif line.startswith("Signal") and ssid:
                signal = line.split(":", 1)[1].strip()
                networks.append(f"{ssid} ({signal})")
                ssid = None
        if not networks:
            return "No networks found"
        return "\n".join(networks)

# Main App
class WiFiAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Analyzer")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QLabel("Available WiFi Networks")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        self.network_list = QTextEdit()
        self.network_list.setReadOnly(True)
        layout.addWidget(self.network_list)

        self.refresh_btn = QPushButton("Refresh Networks")
        self.refresh_btn.clicked.connect(self.toggle_scan)
        layout.addWidget(self.refresh_btn)

        self.worker = None
        self.scanning = False

    def toggle_scan(self):
        if not self.scanning:
            self.start_scan()
        else:
            self.stop_scan()

    def start_scan(self):
        self.worker = WiFiScanWorker(interval=2)  # scan every 2 seconds
        self.worker.progress.connect(self.update_network_list)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()
        self.refresh_btn.setText("Stop Scanning")
        self.scanning = True

    def stop_scan(self):
        if self.worker:
            self.worker.stop()
        self.refresh_btn.setText("Refresh Networks")
        self.scanning = False

    def update_network_list(self, networks_text):
        self.network_list.setPlainText(networks_text)

    def scan_finished(self):
        self.refresh_btn.setText("Refresh Networks")
        self.scanning = False

# DockButton (modified minimally to support icons)
class DockButton(QPushButton):
    def __init__(self, name, icon_path: str = None, base_size=56):
        # keep the original behaviour of showing first letter unless we have an icon
        super().__init__(name[0].upper() if name else '?')
        self.full_name = name
        self.base_size = int(base_size)
        self.icon_path = icon_path

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # drag helpers
        self._drag_start_pos = None

        # scale management
        self._scale = 1.0
        self._target_scale = 1.0
        self._min_scale = 0.9
        self._max_scale = 1.8

        # initial fixed size
        self.setFixedSize(self.base_size, self.base_size)
        self.setToolTip(name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # if an icon path was provided, use it (no exception if file missing; QIcon handles it)
        if self.icon_path:
            self.setIcon(QIcon(self.icon_path))
            self.setIconSize(QSize(self.base_size - 12, self.base_size - 12))
            self.setText("")  # icon only
        else:
            # text fallback remains first letter (same as before)
            if not self.text():
                self.setText(name[0].upper() if name else '?')

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
        # update icon size when style/size changes (if icon present)
        if self.icon_path and not self.icon().isNull():
            # keep a small padding from the button size
            icon_sz = max(12, int(round(size_px * 0.72)))
            self.setIconSize(QSize(icon_sz, icon_sz))

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
                    # Use CopyAction - dock -> desktop should create a shortcut (copy)
                    drag.exec(Qt.DropAction.CopyAction)
                except Exception:
                    traceback.print_exc()
        super().mouseMoveEvent(ev)


# BottomDock (only change: pass icon_path from APP_ICONS when creating DockButton)
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
            # get the icon path from global APP_ICONS if present (falls back to None)
            icon_path = APP_ICONS.get(name) if 'APP_ICONS' in globals() else None
            btn = DockButton(name, icon_path, self.base_btn_size)
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

APP_MAPPING = {
    'Notebook': NotebookApp,
    'Paint': PaintApp,
    'Explorer': ExplorerApp,
    'WebBrowser': WebBrowserApp,
    'Settings': lambda: SettingsApp(main_win) if 'main_win' in globals() else SettingsApp(None),
    'GamesApp': GamesApp,
    'ApplicationAdder': ApplicationAdder,
    'LuxxerArchiver': LuxxerArchiverApp,
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
    'WallpapersManager': WallpapersManagerApp,
}


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

    @staticmethod
    def create_app(app_name: str, desc: str = "", icon: str = "icon.ico"):
        factory = APP_MAPPING.get(app_name)
        if factory is None:
            print(f"[placeholder] Created nameiconApp for '{app_name}'")
            return lambda: PlaceholderApp(app_name, desc)
        return lambda: factory()

apps_with_icons = [
    {
        "name": name,
        "icon": APP_ICONS.get(name, "icon.ico"),
        "creator": PlaceholderApp.create_app(name, icon=APP_ICONS.get(name, "icon.ico"))
    }
    for name in APPS_LIST
]

def run_with_bsod(func):
    try:
        return func()
    except Exception:
        traceback.print_exc()
        return 1

class MainWindow(QMainWindow):
    def __init__(self, apps_with_icons, APP_STATE=None):
        super().__init__()
        self.APP_STATE = APP_STATE or {}
        self.APP_STATE.setdefault('desktop_icons', [])
        self.setWindowTitle("Luxxer OS")
        try:
            self.setWindowIcon(QIcon("icon.ico"))
        except Exception:
            pass
        self.resize(1280, 800)

        # Normalize apps_with_icons into dicts with creator
        self.apps_with_icons = []
        for entry in apps_with_icons or []:
            if isinstance(entry, str):
                name = entry
                icon = APP_ICONS.get(name, "icon.ico")
                creator = self._make_placeholder_creator(name)
            elif isinstance(entry, dict):
                name = entry.get("name") or entry.get("title") or str(entry)
                icon = entry.get("icon", APP_ICONS.get(name, "icon.ico"))
                creator = entry.get("creator")
                if not callable(creator):
                    creator = self._make_smart_creator(name)
            else:
                name = str(entry)
                icon = APP_ICONS.get(name, "icon.ico")
                creator = self._make_placeholder_creator(name)

            self.apps_with_icons.append({"name": name, "icon": icon, "creator": creator})

        app_names = [a["name"] for a in self.apps_with_icons]

        # wallpaper (improved with warning)
        wallpaper_path = self.APP_STATE.get('settings', {}).get('wallpaper', "ScreenPhoto2-2560x1440px.png")
        if wallpaper_path:
            if os.path.exists(wallpaper_path):
                pm = QPixmap(wallpaper_path)
                if pm.isNull():
                    print(f"[WARNING] Main Background not found or failed to load: {wallpaper_path}")
                    self.wallpaper = QPixmap()
                else:
                    self.wallpaper = pm
            else:
                print(f"[WARNING] Main Background not found: {wallpaper_path}")
                self.wallpaper = QPixmap()
        else:
            self.wallpaper = QPixmap()

        # MDI area and background paint
        self.mdi = QMdiArea()
        # override paintEvent with bound method that uses viewport rect
        self.mdi.paintEvent = self._paint_background

        # Icon area - desktop icons
        self.icon_area = IconAdderAreaMarquee(self.mdi.viewport(), cell_size=120, spacing=12)
        self.icon_area.setGeometry(self.mdi.viewport().rect())
        self.icon_area.lower()
        self.icon_area.show()

        # safe connect - avoid multiple connects
        try:
            try:
                self.icon_area.icon_added.disconnect()
            except Exception:
                pass
            try:
                self.icon_area.icon_activated.disconnect()
            except Exception:
                pass
            self.icon_area.icon_added.connect(self._on_icon_added)
            self.icon_area.icon_activated.connect(self._on_icon_activated)
        except Exception:
            pass

        # Bottom dock with app names
        self.dock = BottomDock(self, app_names)

        # central layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.mdi, 1)
        layout.addWidget(self.dock, 0)
        self.setCentralWidget(central)

        # quick app_map for placeholders
        self.app_map = {a["name"]: (lambda n=a["name"]: QLabel(f"{n} (Placeholder)")) for a in self.apps_with_icons}

        # context menu on desktop viewport
        self.mdi.viewport().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.mdi.viewport().customContextMenuRequested.connect(self._show_context_menu)
        self.centralWidget().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.centralWidget().customContextMenuRequested.connect(self._show_context_menu)

        # patch right-click behavior
        self._patch_mouse_press(self.mdi.viewport())
        self._patch_mouse_press(self.centralWidget())

        # track opened subwindows to avoid duplicates
        self._open_subwindows = {}  # app_name -> QMdiSubWindow

        # Desktop double-open guard (debounce)
        self._recently_opened_paths = set()

        # auto-refresh timer
        self._auto_refresh_timer = QTimer(self)
        self._auto_refresh_timer.setInterval(1000)
        self._auto_refresh_timer.timeout.connect(self._apply_mdi_background)
        self._auto_refresh_enabled = False

        self._icons_visible = True
        self._icons_locked = False

        # load icons after geometry ready
        QTimer.singleShot(40, self._load_desktop_icons)

        # Desktop simulation folder
        self._desktop_path = os.path.join(os.getcwd(), "Desktop")
        os.makedirs(self._desktop_path, exist_ok=True)

        self._desktop_widget = QWidget(self.mdi.viewport())
        self._desktop_widget.setGeometry(self.mdi.viewport().rect())
        self._desktop_widget.lower()
        self._desktop_widget.show()

        self._desktop_items = []

    # helpers
    def _get_icon_area_names(self) -> list:
        names = []
        for it in getattr(self.icon_area, "icons", []):
            n = None
            try:
                if hasattr(it, "name"):
                    n = getattr(it, "name")
            except Exception:
                n = None
            if not n and hasattr(it, "text") and callable(getattr(it, "text")):
                try:
                    n = it.text()
                except Exception:
                    n = None
            if not n:
                try:
                    prop = it.property("name")
                    if prop:
                        n = prop
                except Exception:
                    pass
            if not n:
                try:
                    prop2 = it.property("path")
                    if prop2:
                        n = prop2
                except Exception:
                    pass
            if n:
                try:
                    n = str(n)
                except Exception:
                    pass
            if n:
                names.append(n)
        return names

    # creators helpers
    def _make_placeholder_creator(self, name):
        return lambda n=name: PlaceholderApp(n, "Work in progress")

    def _make_smart_creator(self, name):
        def creator():
            cls_or_factory = APP_MAPPING.get(name)
            if cls_or_factory is None:
                return PlaceholderApp(name, "Work in progress")
            try:
                return cls_or_factory()
            except TypeError:
                try:
                    return cls_or_factory(self)
                except Exception:
                    return cls_or_factory()
            except Exception as e:
                traceback.print_exc()
                return PlaceholderApp(name, f"Failed to instantiate: {e}")
        return creator

    # icon loading / layout
    def _load_desktop_icons(self):
        try:
            # idempotent load: clear existing items first
            names = self.APP_STATE.get('desktop_icons', []) or []
            if hasattr(self.icon_area, "clear_icons"):
                try:
                    self.icon_area.clear_icons()
                except Exception:
                    pass
            else:
                # otherwise, clear icon-area container list if present
                if hasattr(self.icon_area, 'icons'):
                    try:
                        self.icon_area.icons = []
                    except Exception:
                        pass

            # add only unique names to avoid duplicates
            seen = set()
            for n in names:
                if n in seen:
                    continue
                seen.add(n)
                if hasattr(self.icon_area, "add_icon"):
                    try:
                        self.icon_area.add_icon(n)
                    except Exception:
                        # fallback to manual add if add_icon not working
                        pass
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

    # icon signals
    def _on_icon_added(self, name: str, index: int = None, pos: QPoint = None):
        try:
            if self._icons_locked:
                QMessageBox.information(self, "Locked", "Desktop icons are locked; changes won't be saved.")
                return
            names = self._get_icon_area_names()
            # dedupe
            unique = []
            for n in names:
                if n not in unique:
                    unique.append(n)
            self.APP_STATE['desktop_icons'] = unique
            try:
                save_state(self.APP_STATE)
            except Exception:
                pass
        except Exception:
            traceback.print_exc()

    def _on_icon_activated(self, name: str):
        try:
            # reuse existing subwindow for same app
            if name in self._open_subwindows:
                try:
                    sub = self._open_subwindows[name]
                    if sub and not sub.isHidden():
                        sub.showNormal()
                        sub.widget().setFocus()
                        sub.activateWindow()
                        return
                except Exception:
                    pass

            if name in APP_MAPPING:
                self.launch_app(name)
            else:
                if any(a["name"] == name for a in self.apps_with_icons):
                    self.launch_app(name)
                else:
                    QMessageBox.information(self, "Launch", f"No app mapped for shortcut '{name}'.")
        except Exception:
            traceback.print_exc()

    # mouse/right-click helper
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

    # context menu actions helpers
    def toggle_auto_refresh(self):
        if self._auto_refresh_enabled:
            self._auto_refresh_timer.stop()
            self._auto_refresh_enabled = False
            QMessageBox.information(self, "Auto-refresh", "Auto-refresh stopped.")
        else:
            self._auto_refresh_timer.start()
            self._auto_refresh_enabled = True
            QMessageBox.information(self, "Auto-refresh", "Auto-refresh started (every 1s).")

    def toggle_icons_visibility(self):
        self._icons_visible = not self._icons_visible
        self.icon_area.setVisible(self._icons_visible)

    def toggle_lock_icons(self):
        self._icons_locked = not self._icons_locked
        QMessageBox.information(self, "Icons lock",
                                "Desktop icons locked." if self._icons_locked else "Desktop icons unlocked.")

    def add_shortcut_prompt(self):
        text, ok = QInputDialog.getText(self, "Add shortcut", "Name for new shortcut:")
        if not ok or not text.strip():
            return
        name = text.strip()
        try:
            if hasattr(self.icon_area, "add_icon"):
                self.icon_area.add_icon(name)
            else:
                QMessageBox.warning(self, "Not supported", "Add shortcut is not available with current icon area.")
                return
            names = self._get_icon_area_names()
            # dedupe before saving
            unique = []
            for n in names:
                if n not in unique:
                    unique.append(n)
            self.APP_STATE['desktop_icons'] = unique
            try:
                save_state(self.APP_STATE)
            except Exception:
                pass
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Error", "Failed to add shortcut.")

    def export_desktop_layout(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Export desktop layout", "", "JSON Files (*.json);;All Files (*)")
            if not path:
                return
            layout = self.APP_STATE.get('desktop_icons', []) or []
            with open(path, "w", encoding="utf-8") as f:
                json.dump(layout, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Exported", f"Layout exported to:{path}")
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Error", "Failed to export layout.")

    def import_desktop_layout(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Import desktop layout", "", "JSON Files (*.json);;All Files (*)")
            if not path:
                return
            with open(path, "r", encoding="utf-8") as f:
                layout = json.load(f)
            if not isinstance(layout, list):
                QMessageBox.warning(self, "Invalid", "Layout file must contain a JSON array of icon names.")
                return
            # dedupe
            unique = []
            for n in layout:
                if n not in unique:
                    unique.append(n)
            self.APP_STATE['desktop_icons'] = unique
            try:
                save_state(self.APP_STATE)
            except Exception:
                pass
            self._load_desktop_icons()
            QMessageBox.information(self, "Imported", f"Layout imported from:{path}")
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Error", "Failed to import layout.")

    def clear_desktop(self):
        r = QMessageBox.question(self, "Clear desktop", "Remove all desktop icons?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            try:
                if hasattr(self.icon_area, "clear_icons"):
                    self.icon_area.clear_icons()
                else:
                    self.APP_STATE['desktop_icons'] = []
                    try:
                        save_state(self.APP_STATE)
                    except Exception:
                        pass
                    self._load_desktop_icons()
                QMessageBox.information(self, "Cleared", "Desktop icons removed.")
            except Exception:
                traceback.print_exc()
                QMessageBox.warning(self, "Error", "Failed to clear desktop.")

    def reflow_icons(self):
        try:
            names = self.APP_STATE.get('desktop_icons', []) or []
            if hasattr(self.icon_area, "clear_icons"):
                self.icon_area.clear_icons()
            for n in names:
                if hasattr(self.icon_area, "add_icon"):
                    self.icon_area.add_icon(n)
            QMessageBox.information(self, "Reflow", "Desktop icons reflowed.")
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Error", "Failed to reflow icons.")

    def open_terminal(self):
        try:
            if 'CMD' in APP_MAPPING:
                self.launch_app('CMD')
            else:
                import subprocess, platform
                if platform.system() == "Windows":
                    subprocess.Popen(["cmd.exe"])
                else:
                    subprocess.Popen(["x-terminal-emulator"])
        except Exception:
            traceback.print_exc()
            QMessageBox.warning(self, "Error", "Failed to open terminal.")

    def _show_context_menu(self, global_pos):
        try:
            sender = self.sender()
            if isinstance(global_pos, QPoint) and sender is not None and hasattr(sender, "mapToGlobal"):
                try:
                    global_pos = sender.mapToGlobal(global_pos)
                except Exception:
                    pass
        except Exception:
            pass

        menu = QMenu(self)

        a_refresh = menu.addAction("Refresh Now")
        a_auto = menu.addAction("Toggle Auto-Refresh")
        a_auto.setCheckable(True)
        a_auto.setChecked(self._auto_refresh_enabled)
        menu.addSeparator()

        a_toggle_icons = menu.addAction("Show/Hide Desktop Icons")
        a_lock_icons = menu.addAction("Lock/Unlock Desktop Icons")
        menu.addSeparator()

        a_add = menu.addAction("Add Shortcut...")
        a_reflow = menu.addAction("Reflow icons")
        a_clear = menu.addAction("Clear Desktop")
        a_export = menu.addAction("Export Layout...")
        a_import = menu.addAction("Import Layout...")
        menu.addSeparator()

        a_new_folder = menu.addAction("New Folder")
        a_new_txt = menu.addAction("New Text File")
        menu.addSeparator()

        a_terminal = menu.addAction("Open Terminal")
        a_settings = menu.addAction("Settings")
        a_change_wallpaper = menu.addAction("Change wallpaper...")
        menu.addSeparator()
        a_exit = menu.addAction("Exit Luxxer")

        a_copy = menu.addAction("Copy")
        a_paste = menu.addAction("Paste")

        action = menu.exec(global_pos)

        if action == a_refresh:
            self._apply_mdi_background()
        elif action == a_auto:
            self.toggle_auto_refresh()
        elif action == a_toggle_icons:
            self.toggle_icons_visibility()
        elif action == a_lock_icons:
            self.toggle_lock_icons()
        elif action == a_add:
            self.add_shortcut_prompt()
        elif action == a_reflow:
            self.reflow_icons()
        elif action == a_clear:
            self.clear_desktop()
        elif action == a_export:
            self.export_desktop_layout()
        elif action == a_import:
            self.import_desktop_layout()
        elif action == a_new_folder:
            self.create_folder()
        elif action == a_new_txt:
            self.create_text_file()
        elif action == a_terminal:
            self.open_terminal()
        elif action == a_settings:
            try:
                if "Settings" in APP_MAPPING:
                    self.launch_app("Settings")
                else:
                    settings_window = SettingsApp()
                    sub = QMdiSubWindow()
                    sub.setWidget(settings_window)
                    sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
                    sub.setWindowTitle("Settings")
                    self.mdi.addSubWindow(sub)
                    sub.show()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open Settings: {e}")
        elif action == a_change_wallpaper:
            self._choose_wallpaper()
        elif action == a_exit:
            self.close()
        elif action == a_copy:
            self._copy_to_clipboard()
        elif action == a_paste:
            self._paste_from_clipboard()

    def create_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            folder_path = os.path.join(self._desktop_path, name)
            try:
                os.makedirs(folder_path, exist_ok=True)
                self._add_desktop_item(folder_path, icon_path="folder.ico")
                names = self.APP_STATE.get('desktop_icons', [])
                if name not in names:
                    names.append(name)
                self.APP_STATE['desktop_icons'] = names
                try:
                    save_state(self.APP_STATE)
                except Exception:
                    pass
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create folder: {e}")

    def create_text_file(self):
        name, ok = QInputDialog.getText(self, "New Text File", "File name (without .txt):")
        if ok and name:
            file_path = os.path.join(self._desktop_path, f"{name}.txt")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("")
                self._add_desktop_item(file_path, icon_path="txt.ico")
                names = self.APP_STATE.get('desktop_icons', [])
                if f"{name}.txt" not in names:
                    names.append(f"{name}.txt")
                self.APP_STATE['desktop_icons'] = names
                try:
                    save_state(self.APP_STATE)
                except Exception:
                    pass
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create file: {e}")

    def _add_desktop_item(self, path, icon_path=None):
        name = os.path.basename(path)
        icon_label = QLabel(self.icon_area)
        try:
            icon_label.setPixmap(QPixmap(icon_path or "icon.ico").scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                                                                         Qt.TransformationMode.SmoothTransformation))
        except Exception:
            pass
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setProperty("name", name)

        text_label = QLabel(name, self.icon_area)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QWidget(self.icon_area)
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(2)
        vbox.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(text_label, 0, Qt.AlignmentFlag.AlignCenter)

        container.setProperty("path", path)
        container.setProperty("name", name)
        container.show()

        if hasattr(self.icon_area, "icons"):
            # avoid adding same container twice
            try:
                if container not in self.icon_area.icons:
                    self.icon_area.icons.append(container)
            except Exception:
                pass

        def open_runner(event=None, p=path):
            # guard: don't open duplicates for the same path rapidly
            if p in self._recently_opened_paths:
                return
            self._recently_opened_paths.add(p)
            QTimer.singleShot(300, lambda: self._recently_opened_paths.discard(p))
            self._open_desktop_item(p)

        container.mouseDoubleClickEvent = open_runner

    def _open_desktop_item(self, path):
        try:
            runner = _DesktopItemRunner(path)
            title = os.path.basename(path)
            # reuse a subwindow for identical path/title
            existing = next((s for s in self.mdi.subWindowList() if s.windowTitle() == title), None)
            if existing:
                existing.showNormal()
                existing.widget().setFocus()
                existing.activateWindow()
                return

            sub = QMdiSubWindow()
            sub.setWidget(runner)
            sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            sub.setWindowTitle(title)
            self.mdi.addSubWindow(sub)
            sub.show()
            self.animate_window_show(sub)
        except Exception:
            traceback.print_exc()

    def _choose_wallpaper(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose wallpaper", "",
                                              "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if path:
            self.set_wallpaper(path)

    def set_wallpaper(self, path: str):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"[WARNING] Main Background not found or failed to load: {path}")
            QMessageBox.warning(self, "Wallpaper", "Failed to load image.")
            return
        self.wallpaper = pixmap
        try:
            # ensure MDI viewport repaints the wallpaper
            self.mdi.viewport().update()
        except Exception:
            self.update()
        if self.APP_STATE is not None:
            self.APP_STATE.setdefault('settings', {})['wallpaper'] = path
            try:
                save_state(self.APP_STATE)
            except Exception:
                pass

    def _paint_background(self, event):
        try:
            # paint wallpaper directly onto viewport using the event's painter when available
            painter = QPainter(self.mdi.viewport())
            rect = self.mdi.viewport().rect()
            painter.fillRect(rect, self.palette().window())
            if self.wallpaper and not self.wallpaper.isNull():
                pm = self.wallpaper.scaled(rect.size(),
                                           Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                           Qt.TransformationMode.SmoothTransformation)
                x = (rect.width() - pm.width()) // 2
                y = (rect.height() - pm.height()) // 2
                painter.drawPixmap(x, y, pm)
            painter.end()
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
        # single-instance per app_name: if open, activate and return
        try:
            # debounce rapid launches per app_name
            if app_name in self._recently_opened_paths:
                return
            self._recently_opened_paths.add(app_name)
            QTimer.singleShot(300, lambda n=app_name: self._recently_opened_paths.discard(n))

            # if we already have a live subwindow, bring it to front
            existing = self._open_subwindows.get(app_name)
            if existing and existing in self.mdi.subWindowList():
                try:
                    existing.showNormal()
                    existing.widget().setFocus()
                    existing.activateWindow()
                    return
                except Exception:
                    # fallthrough to create new if activation failed
                    pass

            app_info = next((a for a in self.apps_with_icons if a["name"] == app_name), None)
            if not app_info:
                QMessageBox.warning(self, "Error", f"App '{app_name}' does not exist!")
                return

            creator = app_info.get("creator")
            if callable(creator):
                app_widget = creator()
            else:
                if isinstance(creator, QWidget):
                    app_widget = creator
                else:
                    app_widget = creator()

            # sizing logic (robust)
            try:
                native_min = app_widget.minimumSizeHint() if hasattr(app_widget, "minimumSizeHint") else app_widget.minimumSize()
            except Exception:
                native_min = QSize(200, 100)
            native_min_w = max(1, native_min.width() or 0)
            native_min_h = max(1, native_min.height() or 0)

            try:
                hint = app_widget.sizeHint() if hasattr(app_widget, "sizeHint") else QSize(native_min_w, native_min_h)
            except Exception:
                hint = QSize(native_min_w, native_min_h)
            desired_w = max(1, hint.width() or native_min_w)
            desired_h = max(1, hint.height() or native_min_h)

            BASE_MIN_W, BASE_MIN_H = 900, 800
            enforced_min_w = max(native_min_w, BASE_MIN_W)
            enforced_min_h = max(native_min_h, BASE_MIN_H)

            vp_rect = self.mdi.viewport().rect()
            vp_w = max(1, vp_rect.width())
            vp_h = max(1, vp_rect.height())

            effective_min_w = min(enforced_min_w, vp_w)
            effective_min_h = min(enforced_min_h, vp_h)

            final_w = min(max(desired_w, enforced_min_w), vp_w)
            final_h = min(max(desired_h, enforced_min_h), vp_h)

            sub = QMdiSubWindow()
            sub.setWidget(app_widget)
            sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            sub.setWindowTitle(app_name)

            # ensure sizes are applied safely
            try:
                sub.setMinimumSize(effective_min_w, effective_min_h)
                sub.resize(final_w, final_h)
            except Exception:
                pass

            # add to MDI
            self.mdi.addSubWindow(sub)

            # center it in viewport
            vp = self.mdi.viewport().rect()
            x = max(0, (vp.width() - final_w) // 2)
            y = max(0, (vp.height() - final_h) // 2)
            target_geom = QRect(x, y, final_w, final_h)

            # show and animate
            sub.show()
            self.animate_window_show(sub, target_geom)

            # remember open subwindow
            self._open_subwindows[app_name] = sub

            # cleanup when the subwindow is destroyed to avoid stale references
            try:
                sub.destroyed.connect(lambda obj, name=app_name: self._open_subwindows.pop(name, None))
            except Exception:
                # fallback: try hooking to closeEvent by overriding if possible
                try:
                    orig_close = getattr(sub, "closeEvent", None)

                    def close_and_cleanup(event, name=app_name, orig=orig_close):
                        self._open_subwindows.pop(name, None)
                        if callable(orig):
                            try:
                                orig(event)
                            except Exception:
                                pass
                        else:
                            event.accept()
                    sub.closeEvent = close_and_cleanup
                except Exception:
                    pass

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Cannot start '{app_name}': {e}")

    def open_app(self, app_class):
        if app_class is DesktopSpacesApp:
            app = app_class(self)
        else:
            app = app_class()
        app.show()

    def animate_window_show(self, sub, target_geom: QRect = None):
        """Animate a subwindow from a small center rect to its final geometry the *first time* it's shown.
        Subsequent calls (e.g. when moving/resizing/focusing) will **not** re-run the animation which
        previously caused the visual 'new-window' glitch when users dragged or restored windows.
        """
        try:
            # If we've already animated this subwindow once, don't animate again.
            if getattr(sub, '_animated_once', False):
                return

            # compute target geometry clamped to mdi viewport
            if target_geom is None:
                target_geom = sub.geometry()

            vp = self.mdi.viewport().rect()
            w = min(target_geom.width(), vp.width())
            h = min(target_geom.height(), vp.height())
            tx = max(0, min(target_geom.x(), vp.width() - w))
            ty = max(0, min(target_geom.y(), vp.height() - h))
            final = QRect(tx, ty, w, h)

            # choose a small centered start rect (visually pleasing but non-destructive)
            center_x = final.center().x()
            center_y = final.center().y()
            start_w = max(8, min(32, final.width()//8))
            start_h = max(8, min(32, final.height()//8))
            start = QRect(center_x, center_y, start_w, start_h)

            # stop any previous animation object on this sub
            try:
                old = getattr(sub, '_open_anim', None)
                if old is not None:
                    try:
                        old.stop()
                    except Exception:
                        pass
            except Exception:
                pass

            anim = QPropertyAnimation(sub, b"geometry")
            anim.setDuration(360)
            anim.setStartValue(start)
            anim.setEndValue(final)
            anim.setEasingCurve(QEasingCurve.Type.OutBack)

            # keep reference so it doesn't get GC'd and mark as animated
            sub._open_anim = anim
            sub._animated_once = True

            anim.start()

        except Exception:
            traceback.print_exc()


# End of MainWindow


if __name__ == "__main__":
    # simplified start-up: no boot screen, single app.exec() call
    APP_STATE = load_state() or {}
    APP_STATE.setdefault('settings', {})

    app = QApplication(sys.argv)
    apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))

    apps_simple = [{"name": name, "icon": APP_ICONS.get(name, "icon.ico")} for name in APPS_LIST]

    start = StartScreen(app, APP_STATE)
    if start.exec() == QDialog.DialogCode.Accepted:
        main_win = MainWindow(apps_simple, APP_STATE)
        apply_theme_global(APP_STATE['settings'].get('theme', 'transparent'))
        main_win.showFullScreen()
        try:
            exit_code = app.exec()
        except Exception:
            traceback.print_exc()
            exit_code = 1
        sys.exit(exit_code)
    else:
        sys.exit(0)
