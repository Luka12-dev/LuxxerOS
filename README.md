# Luxxer OS - README

> **Important:** This document explains how to run, package, test and troubleshoot Luxxer OS (development edition). It also includes ethical & legal guidance, troubleshooting tips, packaging commands, and a developer-oriented changelog and contribution guide. Read carefully before running any scanning or networking tools included with the project.

---

## Table of contents

1. Quick start
2. What is Luxxer OS (short)
3. Running from source (recommended for developers)
4. Building a single-file `.exe` using PyInstaller (packaging)
5. Files included in the build (what to bundle)
6. Runtime requirements & optional features
7. Packaging caveats, exe size & tips to reduce size
8. How the supervised BSOD runner works (safety)
9. Troubleshooting common errors
10. Testing & diagnostics
11. Security, ethics & license (must read)
12. Contributing guidelines
13. Release notes & changelog (v2.0)
14. Credits & acknowledgements
15. FAQ
16. Appendix: Useful commands and examples

---

## 1) Quick start

If you just want to run Luxxer OS locally for development or testing:

1. Clone or copy the `Luxxer_OS` folder into a working directory.
2. Create a clean Python virtual environment:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies (minimum):

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, the most commonly used packages are `PyQt6`, `psutil`, `pyautogui`, `moviepy`, `cryptography`, `pillow`, and optionally `pytesseract`.

4. Run the app from the project root:

```bash
python Luxxer_OS.py
```

This launches the Start Screen. Accept the ethical notice and then continue to the main OS.

---

## 2) What is Luxxer OS (short)

Luxxer OS is an educational, experimental desktop-like environment implemented in Python using PyQt6. It bundles multiple small apps (Utilities, Tools, Games, Editors) into one unified shell that runs in a PyQt window and aims to be modular, hackable, and instructive.

**Important:** Some included tools may interact with local resources, networks, or devices. Use responsibly and ethically. See the Ethical Use notice further below.

---

## 3) Running from source (recommended for developers)

- Ensure `python` points to a modern interpreter (3.9+ recommended; 3.10/3.11 supported).
- Use a virtualenv to isolate packages.
- Typical dev dependencies:

```text
PyQt6
PyQt6-Qt6
PyQt6-sip
psutil
pyautogui
moviepy
pillow
cryptography
pytesseract (optional)
```

- Launch with logging enabled if you want to debug native crashes.

**Notes:**
- Some modules (PyQt6 WebEngine, QtPdf, QtMultimedia) may not be available in all PyQt6 builds. The code is defensive and will disable those features if they are missing.
- If an app fails to import, Luxxer OS will still run - missing apps become `None` and will not be instantiated.

---

## 4) Building a single-file `.exe` using PyInstaller

**Important**: creating a single-file `.exe` for such a large project can produce very large artifacts (several GB). Expect long build times and large output files.

An example PyInstaller command (single line) that bundles the files and icon you listed:

```bash
pyinstaller --noconfirm --clean --onefile \
  --name LuxxerOS \
  --add-data "Luxxer_OS.py;." \
  --add-data "BSOD.py;." \
  --add-data "iconadderonmainscreen.py;." \
  --add-data "apps_extra3.py;." \
  --add-data "Luxxer_OS_Start.py;." \
  --add-data "DesktopContextOpen.py;." \
  --add-data "RandomChallenge.py;." \
  --add-data "games_all.py;." \
  --add-data "MotivationAIChat.py;." \
  --add-data "settings_utils.py;." \
  --add-data "start_menu_file.py;." \
  --add-data "applicationadder.py;." \
  --add-data "apps_extra.py;." \
  --add-data "apps_extra2.py;." \
  --add-data "JokeGenerator.py;." \
  --add-data "isAll-ImportsHere.py;." \
  --icon icon.ico \
  Luxxer_OS.py
```

**Platform notes:**
- Run PyInstaller on the target platform (Windows users should run PyInstaller on Windows to get a Windows exe).
- Use `--onefile` to bundle into a single executable (but this increases startup time and size). To keep smaller results, omit `--onefile` and use the `dist/` folder with the `--onedir` format.

**Alternative**: for smaller artifacts, consider `--onedir` instead of `--onefile` and exclude large optional libs.

---

## 5) Files included in the build (what to bundle)

Suggested file list (already mentioned above):

- Luxxer_OS.py (main entry)
- BSOD.py (blue-screen supervisor)
- iconadderonmainscreen.py
- apps_extra3.py (bundle of many apps)
- Luxxer_OS_Start.py (start screen + theme)
- DesktopContextOpen.py
- RandomChallenge.py
- games_all.py
- MotivationAIChat.py
- settings_utils.py
- start_menu_file.py
- applicationadder.py
- apps_extra.py
- apps_extra2.py
- JokeGenerator.py
- isAll-ImportsHere.py
- icon.ico

---

## 6) Runtime requirements & optional features

**Required** (minimum for core UI):
- Python 3.9+
- PyQt6 and its Qt runtime

**Optional** (enable extra features):
- `psutil` - for device/disk info
- `pyautogui` - for automation features
- `moviepy` - for video editing features
- `pillow` (PIL) - image handling
- `cryptography` - secure vault features
- `pytesseract` + `tesseract` binary - OCR tools

If optional modules are not present, the corresponding features gracefully disable.

---

## 7) Packaging caveats, exe size & tips to reduce size

- The PyQt6 wheels include a large Qt runtime; bundling PyQt6 will create a large exe. Expect hundreds of MB to multiple GB (depends on `--onefile` and included resources).
- To reduce size:
  - Use `--exclude-module` for heavy optional modules you do not use.
  - Build using `--onedir` then prune unneeded Qt plugins.
  - Consider shipping a minimal set of apps and allowing users to download extras.
  - Use UPX compression (`--upx-dir`) with caution — may break some Qt plugins.

**Note:** 3rd-party libraries (moviepy, pytesseract) may add large native deps; only include them if needed.

---

## 8) How the supervised BSOD runner works (safety)

The BSOD module provides two modes:

- **Monitor (parent process)** - launches the app in a supervised child process. If the child exits with a non-zero code (due to Python exceptions, `SystemExit` with non-zero, or native crash), the parent shows a BSOD window displaying the child's stdout/stderr and the exit code, and offers a Restart button.

- **Supervised (child process)** - runs the app normally but installs an `excepthook` that prints the traceback to stderr and exits with a non-zero code so the monitor can detect it.

**Why this is used:** Native crashes (access violations) often do not provide Python-level exception traces. Using a monitor process allows the UI author to show a friendly Blue Screen with logs if something goes wrong.

**Important**: monitor-mode relies on `subprocess.Popen([...], stdout=PIPE, stderr=PIPE)`. If you use heavy GUI integrations or stdin/stdout redirections, be careful about deadlocks.

---

## 9) Troubleshooting common errors

### `ModuleNotFoundError: No module named 'paramiko'` or similar

- Install missing module in the environment that runs Luxxer OS:

```bash
pip install paramiko
```

- For packaged exe, make sure the module is included in the PyInstaller build (either it is installed in the build env or explicitly added with `--hidden-import`).

### PyQt6: `QTextCursor` attribute errors (e.g. `End`)

- In PyQt6, use `QTextCursor.MoveOperation.End` instead of older enum names. The code has been updated to use `QTextCursor.MoveOperation.End`.

### `super(): __class__ cell not found` runtime error

- This error appears when code uses zero-argument `super()` in a context where the `__class__` cell is missing (for example, when modules are executed in unusual ways or when source gets manipulated).
- Workaround used in this project: avoid zero-arg `super()` inside problematic modules and call base class `__init__` explicitly (e.g. `QMainWindow.__init__(self, parent)`).

### `Process finished with exit code -1073740791 (0xC0000409)` or other native crash exit

- This is a native crash (access violation / stack buffer overrun). The BSOD monitor should catch it - the monitor observes the child's non-zero exit and shows the BSOD window.
- To debug native crashes:
  - Run under a debugger (Visual Studio, WinDbg) on Windows.
  - Check native extension modules (C/C++ dependencies, third-party compiled libraries) for compatibility.
  - Simplify the app (disable optional modules) to isolate the offending module.

### GUI appears but then application exits silently

- Run Luxxer OS from a terminal to see printed tracebacks. The monitor mode will capture stdout/stderr; if running direct, printed exceptions may appear in the console.

---

## 10) Testing & diagnostics

- **Run the built-in BSOD test** by executing `BSOD.py` directly. It includes a small demonstration mode that throws a `RuntimeError` to show the BSOD UI.
- **Scan for problematic `super()` usage**: the project includes `isAll-ImportsHere.py` / `find_super.py` style utilities to locate zero-argument `super()` calls. Use the scanner in CI or before packaging to reduce the chance of `__class__ cell not found` issues.

Example: test the Motivation AI chat standalone:

```bash
python MotivationAIChat.py
```

If it runs stand-alone but fails inside Luxxer OS, check how it is imported (nested import may cause zero-arg `super()` problems). The project uses explicit base-class `__init__` in critical places to avoid this.

---

## 11) Security, ethics & license (MUST READ)

**Luxxer OS is an educational project.** The included tools can potentially be used to scan networks, enumerate devices, or interact with local system components. Please use them ethically.

By running Luxxer OS you agree to follow local laws and the ethical use guidance presented in the Start Screen.

**Highlights:**
- Do not access systems without authorization.
- Do not distribute or deploy malware.
- If you discover a vulnerability, follow responsible disclosure.

License: include whichever license file you prefer (MIT, Apache 2.0, etc.) in the repo root. If none provided, assume "All Rights Reserved" for binary distribution until you add a proper open-source license.

---

## 12) Contributing guidelines

If you want to help develop Luxxer OS:

1. Fork the repository
2. Use a branch per feature/bugfix
3. Run tests locally (add unit tests for logic-heavy modules)
4. Open a PR with description and screenshots

Please follow the project's ethical use statement in all contributions.

---

## 13) Release notes & changelog (v2.0)

- v2.0: Major improvements - StartScreen rewrite, BSOD monitor supervision, modular app guarding, improved theme system, many small apps added or improved (VideoEditor, ImageEditorPro, MediaConverter, DeviceManager, DiskManager, PrinterManager, DockerManager, GitClient). Many demo actions replaced with real functionality where the platform allows.

See `CHANGELOG.md` for a full, timestamped change log.

---

## 14) Credits & acknowledgements

Built with Python and PyQt6. Thanks to the open-source ecosystem: PyQt, psutil, pillow, moviepy, cryptography, and many others. Also thanks to contributors who wrote small utility apps bundled in `apps_extra*`.

---

## 15) FAQ

**Q: The app runs when I start MotivationAIChat.py directly but fails when launched inside Luxxer OS.**
A: This is usually caused by how the module is imported (namespace differences) or by a zero-arg `super()` in a nested import. The project includes a scanner and uses explicit base-class `__init__` in problem modules to avoid this — prefer `QMainWindow.__init__(self, parent)` instead of `super().__init__()` in modules that may be imported dynamically.

**Q: Can I disable the Start Screen or the ethical notice?**
A: The Start Screen includes a checkbox to hide it on future launches. We recommend keeping it enabled during development and in public releases.

**Q: The PR mentions BSOD, is this dangerous?**
A: The BSOD UI is an in-app, friendly error screen that appears in a monitor process when the child exits with an error. It does not crash or change the host OS - it only displays a full-screen window in the Luxxer OS process to help users capture debug info.

---

## 16) Appendix: Useful commands and examples

**Run in dev mode with logging**:
```bash
python Luxxer_OS.py 2>&1 | tee luxxer.log
```

**Build a directory (onedir) with PyInstaller** (smaller, easier to debug):
```bash
pyinstaller --noconfirm --clean --onedir --name LuxxerOS --add-data "BSOD.py;." --icon "icon.ico" Luxxer_OS.py
```

**Build a single-file exe (be prepared for long build and large exe)**
```bash
pyinstaller --noconfirm --clean --onefile --name LuxxerOS --add-data "BSOD.py;." --add-data "MotivationAIChat.py;." --icon "icon.ico" Luxxer_OS.py
```

**Tip:** If packaging fails with missing modules, add `--hidden-import modulename` or modify the `.spec` file.

---

### Final words

Thank you for working on Luxxer OS. This README is intentionally thorough - packaging a large, modular PyQt project is non-trivial and often requires iterating on the build until all optional dependencies and Qt plugins are handled.

If you want, I can also generate:
- a `requirements.txt` tuned to minimize exe size
- a PyInstaller spec file with plugin hooks for Qt
- a CI script for automated builds (Windows + Linux)

---

*End of README*