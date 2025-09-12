Luxxer OS - README (v1.0)

Luxxer OS - demo desktop environment written in Python + PyQt6.
A playful, extensible "OS-like" app that bundles dozens of tiny apps, utilities and minigames into a single desktop-style experience. This file explains how to install, run, package, develop and debug Luxxer OS and its companion modules.

Table of Contents

About

Highlights / Features

Screenshots

System Requirements

Security & Ethics Notice

Repository Layout (important files)

Quick start - run locally (dev)

Creating a distributable EXE (PyInstaller)

Recommended build workflow (spec file approach)

Dependencies

Configuration & persistent state (app_state.json)

How apps are registered & how to add apps

Games integration (games_all.py)

Common errors & debugging tips

Packaging tips to reduce EXE size

Testing & CI suggestions

Roadmap & Ideas

Contributing

Changelog (v1.0)

License & Credits

Contact / Support

About

Luxxer OS is a demonstration project that mimics a lightweight desktop environment using PyQt6. It contains:

A fullscreen main window (MDI + desktop layer).

A dock / bottom bar with quick-launch apps.

A set of small applications (productivity, tools, games).

A Settings app with live theme switching (dark/light/transparent).

A StartScreen that appears once (or until the user toggles it off).

A launcher for bundled games (games_all.py) which can start games in separate processes.

Persistence via settings_utils.py saving to app_state.json.

This project is intended as an educational demo and prototyping playground - not a production OS.

Highlights / Features

PyQt6-based desktop UI: MDI subwindows + desktop background.

Theme system: dark, light, transparent - applied at runtime to QApplication.

Settings saved automatically and applied immediately (no restart required).

Games launcher that runs Pygame/Ursina games in subprocesses to keep GUI responsive.

Application adder: dynamically add user applications to a registry.

StartScreen with legal/ethical notice - must accept once before continuing.

Many small, modular application classes that can be extended or replaced.

Screenshots

![Main Desktop](screenshots/screen1.png)
![Start Screen](screenshots/screen2.png)
![Settings](screenshots/screen3.png)
![Cybersecurity Tools](screenshots/screen4.png)


(You said you will add the images later - place them in screenshots/ and the README will reference them.)

System Requirements

Minimum

OS: Windows 10 (64-bit)

CPU: Dual-core 2.0 GHz (Intel Celeron / AMD)

RAM: 4 GB

Storage: 1 GB free (application + dependencies)

Graphics: Integrated GPU (Intel HD or equivalent)

Python 3.10 recommended (works on 3.8+ with compatible PyQt6 wheel)

Recommended

OS: Windows 10/11 (64-bit)

CPU: Quad-core (Intel Core i5 / AMD Ryzen 5 or better)

RAM: 8 GB+

Storage: 3 GB free (allow room for caches, games and optional ML deps)

GPU: Discrete GPU for 3D games (Ursina): GTX 900 series / AMD RX 400+

Internet: Recommended for installing dependencies and optional features (Ursina, pygame, torch)

The packaged EXE can grow large (hundreds of MB). During development you will see larger sizes due to bundled libraries.

Security & Ethics Notice

Luxxer OS includes playful "hacker" apps (simulators) and system utilities intended for educational and entertainment purposes only. Do not use any component of Luxxer OS for malicious or illegal activities.

Before the first run, users must accept the legal/ethical agreement in the StartScreen; the application will not proceed until the user clicks Continue and accepts. Once accepted, the start screen will not show again unless the user resets settings.

Repository Layout (important files)

Place these files in your project root:

Luxxer_OS.py               # Main application entry
Luxxer_OS_Start.py         # Start screen & theme utilities
start_menu_file.py         # Start menu widget
settings_utils.py          # save_state / load_state helpers
apps_extra.py              # extra apps (HackerSimulator, etc.)
apps_extra2.py             # more extra apps
ApplicationAdder.py        # application adder GUI
JokeGenerator.py           # joke app
MotivationAIChat.py        # local motivational chat (simple)
games_all.py               # games (pygame/ursina) + launcher GUI
games_all_launcher.py      # optional smaller launcher wrapper
README.md                  # this file
MainIco.ico                # icon for exe
screenshots/               # your screenshot images
app_state.json             # optional persisted settings (created on first save)


Filenames must match exactly when packaging - the build script will check for these names.

Quick start - run locally (dev)

Create and activate a Python virtual environment:

python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# or cmd
.\.venv\Scripts\activate.bat
# or bash
source .venv/bin/activate


Install dependencies (core):

pip install -U pip
pip install PyQt6 PyQt6-Qt6 PyQt6-sip


Optional packages (games, media, ML features):

pip install pygame ursina moviepy psutil pyautogui
# If you intend to use optional ML features:
pip install torch torchvision


Run the app:

python Luxxer_OS.py


If you get ImportError or NameError about a missing file, make sure each file in the Repository Layout
 exists and is in the same folder.

Creating a distributable EXE (PyInstaller)

Note: PyInstaller command-lines can be long. On Windows PowerShell use a single line (no trailing backslashes). Use --add-data to include additional Python modules or data files. On Windows, --add-data uses SRC;DEST (semicolon) format.

Example (PowerShell single-line):

pyinstaller --noconfirm --onefile --windowed --icon=MainIco.ico `
  --add-data "Luxxer_OS.py;." `
  --add-data "apps_extra.py;." `
  --add-data "apps_extra2.py;." `
  --add-data "JokeGenerator.py;." `
  --add-data "MotivationAIChat.py;." `
  --add-data "ApplicationAdder.py;." `
  --add-data "games_all.py;." `
  --add-data "settings_utils.py;." `
  --add-data "start_menu_file.py;." `
  --add-data "Luxxer_OS_Start.py;." `
  Luxxer_OS.py


In PowerShell you can use the backtick ` at end of line to continue the command. If you prefer a single physical line, remove the backticks and join everything into one line.

Important tips:

Provide --hidden-import for modules PyInstaller misses (e.g. --hidden-import=moviepy.editor).

If packaging for Windows, run PyInstaller inside the Windows virtual env.

The --add-data "file;." option copies the file into the root of the bundle. Use --add-data "path\to\dir;dir" to copy directories.

For many files, prefer using a .spec file (explained in next section).

Recommended build workflow (spec file approach)

Run PyInstaller once to generate a spec:

pyinstaller --onefile --windowed Luxxer_OS.py


This produces Luxxer_OS.spec. Edit the spec to add datas and hiddenimports in a clean, maintainable way. Example spec snippet:

# Luxxer_OS.spec (excerpt)
block_cipher = None

a = Analysis(
    ['Luxxer_OS.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Luxxer_OS.py', '.'), ('apps_extra.py', '.'), ('apps_extra2.py','.'), 
        ('JokeGenerator.py','.'), ('MotivationAIChat.py','.'), ('ApplicationAdder.py','.'), 
        ('games_all.py','.'), ('settings_utils.py','.'), ('start_menu_file.py','.'), ('Luxxer_OS_Start.py','.')
    ],
    hiddenimports=['moviepy.editor','pyautogui','psutil'],
    ...
)
# then build normally


Re-run PyInstaller with the spec:

pyinstaller Luxxer_OS.spec


This is more robust when bundling many assets.

Dependencies (detailed)

Core

PyQt6 - GUI toolkit (required)

PyQt6-Qt6, PyQt6-sip - supporting wheels

Optional / Feature-based

pygame - 2D games (Snake, Pong, Breakout)

ursina - 3D mini-games (Runner, Ball)

moviepy - media helpers, video operations

pyautogui - screenshot / screen recording helper stubs

psutil - system information helpers

torch / torchvision - AI/ML features (heavy; optional)

Install only the packages you need to keep your environment smaller.

Configuration & persistent state (app_state.json)

settings_utils.py provides save_state(state) and load_state() helpers. By default we persist to app_state.json in the application working directory.

Common keys in APP_STATE:

{
  "settings": {
    "username": "user",
    "theme": "transparent",
    "show_start": true
  },
  "desktop_icons": [
    "Explorer", "Notebook", "Paint"...
  ],
  "pinned_apps": [ ... ]
}


theme - one of dark, light (white), transparent.

show_start - if false, the StartScreen won't appear at next launch.

Save happens automatically on changes (Settings app calls save_state).

How apps are registered & how to add apps

Two variables matter inside Luxxer_OS.py:

APPS_LIST - a list of app display names shown in dock/start menu.

APP_MAPPING / app_map - mapping from display name to the app class or a callable that creates the app widget.

Example snippet inside Luxxer_OS.py (simplified):

APPS_LIST = ["Explorer", "Notebook", "Paint", "Settings", "Games"]
APP_MAPPING = {
    "Explorer": ExplorerApp,
    "Notebook": NotebookApp,
    "Paint": PaintApp,
    "Settings": lambda: SettingsApp(main_win) if 'main_win' in globals() else SettingsApp(None),
    "Games": lambda: GamesApp()  # wrapper that launches games_all launcher
}


To add an app:

Create a class named MyNewApp(QMainWindow) in an appropriate file (e.g., apps_extra.py).

Import it in Luxxer_OS.py (or the module you use to build APP_MAPPING).

Add its display name to APPS_LIST and add APP_MAPPING["DisplayName"] = MyNewApp.

Note: If your app class needs a reference to the main window (for theme or actions), accept a main_ref parameter in the constructor.

Games integration (games_all.py)

games_all.py contains implementations for several small games and a PyQt launcher that starts games in their own subprocesses:

snake (Pygame)

pong (Pygame)

breakout (Pygame)

How to integrate in Luxxer_OS:

Provide an entry in APP_MAPPING that creates a small wrapper window which calls subprocess.Popen([sys.executable, path_to_games_all, "launcher"]) or that instantiates the launcher_main() GUI function from games_all.py.

Make sure games_all.py is included in your PyInstaller datas list or present next to the EXE.

Example app wrapper:

class GamesApp(QMainWindow):
    def __init__(self, main_ref=None):
        super().__init__()
        self.setWindowTitle("Games")
        btn = QPushButton("Open Games Launcher")
        btn.clicked.connect(self.open_launcher)
        self.setCentralWidget(btn)

    def open_launcher(self):
        python = sys.executable
        subprocess.Popen([python, os.path.join(os.path.dirname(__file__), "games_all.py")])

Common errors & debugging tips
ImportError: cannot import name 'StartScreen' from partially initialized module (circular import)

This is caused by circular imports (module A imports B and B imports A).

Fix: Remove cross-module imports. Pass APP_STATE as a parameter when creating StartScreen instead of importing it from Luxxer_OS.

Keep UI modules independent: StartScreen should not import Luxxer_OS. Luxxer_OS imports StartScreen and passes required data.

NameError: DesktopArea is not defined

Likely you created DesktopArea in another module but not imported yet.

Solution: Ensure DesktopArea is defined before using or import it.

AttributeError: 'MainWindow' object has no attribute 'app_area'

Make sure the UI element self.app_area is created in __init__ before being referenced.

Re-check widget creation order.

Crashes when changing theme or repainting (exit code 0xC0000409)

Avoid painting widget contents directly from non-Qt threads.

Use QTimer.singleShot(0, ...) or QApplication.instance().setStyleSheet(...) and let Qt handle repaint.

Do not call repaint() on QMdiArea subwindows from external threads; schedule updates on the main thread.

PyInstaller errors ERROR: Script file '\\' does not exist.

This usually comes from a leftover line-continuation backslash or incorrect quoting in PowerShell.

Use backtick ` for continuation in PowerShell or put the entire command on one line.

Packaging tips to reduce EXE size

Avoid bundling optional heavy libraries (torch, torchvision) unless you need them.

Use a requirements split: requirements-core.txt vs requirements-optional.txt.

Remove unneeded packages from your venv before building.

Use UPX (optional) for compression but test for compatibility.

Consider shipping only the main EXE and a libs folder for big optional modules that you can lazy-load.

Testing & CI suggestions

Add a small unit test suite for non-GUI logic (settings, file utilities).

Use CI (GitLab/GitHub Actions) to run flake8, pytest, and a smoke test that starts the main window headless (-platform offscreen) for CI GUI tests.

Build artifacts in CI (Windows runner) and publish them to releases.

Roadmap & Ideas

Add plugin system for third-party apps (drop a .py in a folder and auto-register).

Online app store integration (optional, with proper sandboxing).

Better multi-monitor / resolution handling.

Localization (translations) - simple JSON-based TRANSLATIONS dictionary.

Installer with auto-update (NSIS / Inno Setup).

Better resource management for subprocess games.

Contributing

Fork the repository.

Create a new branch: feature/<your-feature>.

Add tests where applicable.

Open a PR describing the change and how to test.

Please follow the coding style used across the project - modular app classes, minimal global side-effects and pass main_ref references where needed.

Changelog (v1.0)

v1.0 (initial public demo)

Full MDI desktop with dock, start menu, settings.

Theme system with dark, light, transparent.

StartScreen must be accepted once (persisted).

Games launcher supporting pygame + ursina (subprocessed).

AppAdder for adding custom apps.

~70 demo apps included (productivity, utilities, mini-games).

settings_utils.py for saving/loading app_state.json.

License & Credits

License: MIT (recommended for open-source demo projects). Include a LICENSE file in repo root.

Credits: You (project owner), community contributors, PyQt6 authors.

Ethical statement: Software is for educational/demo purposes only. Not to be used for malicious activities.

Contact / Support

For issues, open an issue in the repository.

For private support or paid consult, provide contact details here (email/GitLab username).

Appendix - Example PyInstaller one-liner (single line)

If you prefer a single-line in PowerShell (escape double quotes properly):

pyinstaller --noconfirm --onefile --windowed --icon=MainIco.ico --add-data "Luxxer_OS.py;." --add-data "apps_extra.py;." --add-data "apps_extra2.py;." --add-data "JokeGenerator.py;." --add-data "MotivationAIChat.py;." --add-data "ApplicationAdder.py;." --add-data "games_all.py;." --add-data "settings_utils.py;." --add-data "start_menu_file.py;." --add-data "Luxxer_OS_Start.py;." Luxxer_OS.py


If PowerShell complains, either (a) wrap each --add-data with single quotes, or (b) use the backtick continuation approach demonstrated earlier.

Appendix - Troubleshooting: Start screen acceptance not persisted

If your StartScreen keeps showing even after Accept, ensure:

APP_STATE['settings']['show_start'] is set to False when accepting.

save_state(APP_STATE) is called successfully and writes app_state.json.

Your startup code loads APP_STATE = load_state() before creating StartScreen and uses it to set initial radio states.

No circular imports: Luxxer_OS_Start should not import Luxxer_OS to get APP_STATE. Instead Luxxer_OS should import Luxxer_OS_Start and pass APP_STATE to StartScreen.

Appendix - Example minimal settings_utils.py
# settings_utils.py
import json, os
STATE_FILE = "app_state.json"

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

Final notes

Keep your virtual environment clean before building final executables.

Test theme switching at runtime using apply_theme_global() and make sure subwindows refresh via QTimer.singleShot(0, ...) if necessary.

If you intend to distribute widely, consider splitting optional heavy features (torch, ursina) into separate optional installers.