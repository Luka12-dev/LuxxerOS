# Luxxer OS v3.0

[![GitHub](https://img.shields.io/badge/GitHub-LuxxerOS-blue?logo=github)](https://github.com/Luka12-dev/LuxxerOS)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4.0%2B-green?logo=qt)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Version 3.0 introduces major stability improvements, custom cursor support, enhanced UI polish, and numerous bug fixes. This document provides comprehensive guidance for running, building, testing, and contributing to Luxxer OS.

---

## Table of Contents

- [What's New in v3.0](#whats-new-in-v30)
- [Quick Start Guide](#quick-start-guide)
- [About Luxxer OS](#about-luxxer-os)
- [Running from Source](#running-from-source)
- [Building Standalone Executables](#building-standalone-executables)
- [Project Structure & Files](#project-structure--files)
- [Dependencies & Optional Features](#dependencies--optional-features)
- [Custom Cursor System](#custom-cursor-system)
- [Performance & Optimization](#performance--optimization)
- [Supervised Error Handling (BSOD System)](#supervised-error-handling-bsod-system)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Security, Ethics & Legal Notice](#security-ethics--legal-notice)
- [Contributing to Luxxer OS](#contributing-to-luxxer-os)
- [Version History](#version-history)
- [Credits & Acknowledgements](#credits--acknowledgements)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Advanced Usage & Commands](#advanced-usage--commands)
- [License](#license)
- [Support & Contact](#support--contact)

---

## What's New in v3.0

### 🎯 Major Improvements

#### Custom Cursor Implementation
- Native custom cursor support with `cursor.png` for main interface
- Dedicated dock cursor (`cursor2.png`) with automatic fallback
- Global cursor override ensuring consistency across all UI elements
- Smooth cursor application to context menus, subwindows, and dynamic widgets

#### Stability & Bug Fixes
- Fixed critical crashes related to zero-argument `super()` calls
- Resolved dock repositioning and black screen issues
- Enhanced error handling throughout the codebase
- Improved widget lifecycle management to prevent memory leaks
- Fixed `QTextCursor` enum compatibility issues for PyQt6

#### UI/UX Enhancements
- Polished theme system with macOS-inspired design language
- Improved window animations with proper debouncing
- Enhanced dock magnification with configurable parameters
- Better context menu positioning and reliability
- Smoother transitions and visual feedback

#### Architecture Improvements
- Robust configuration sanitization for dock settings
- Safe widget cleanup and layout rebuilding
- Enhanced subwindow management with single-instance enforcement
- Improved resource loading with graceful fallbacks
- Better separation of concerns across modules

---

## Quick Start Guide

### For Users (Running Pre-built Release)

1. Download the latest release package for your platform
2. Extract to your preferred location
3. Double-click `LuxxerOS.exe` (Windows) or run the appropriate launcher
4. Accept the ethical use agreement on first launch
5. Explore the desktop environment and bundled applications

### For Developers (Running from Source)

1. Clone or download the project to your local machine
2. Create a virtual environment (highly recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:
   ```bash
   python Luxxer_OS.py
   ```

5. Accept the startup agreement and begin exploring

---

## About Luxxer OS

Luxxer OS is an educational desktop environment simulator built with Python and PyQt6. It provides a comprehensive sandbox for learning about:

- Operating system UI/UX design principles
- Desktop environment architecture
- Application windowing systems
- System resource management
- Security and ethical computing practices

### Key Features:

- **100+ integrated applications** covering productivity, development, multimedia, and utilities
- **Customizable themes** (Transparent, White, Dark)
- **Dock with macOS-style magnification effects**
- **Virtual filesystem** with desktop icon support
- **Application launcher** and window management
- **Integrated development tools** (IDE, terminal, debugger)
- **Multimedia support** (music, video, image editing)
- **Network and system monitoring tools**

**Educational Purpose:** This project is designed for learning, experimentation, and ethical security research in controlled environments.

---

## Running from Source

### System Requirements

- **Python:** 3.9 or newer (3.10/3.11 recommended)
- **Operating System:** Windows 10/11, macOS 10.14+, or modern Linux
- **RAM:** 4GB minimum, 8GB+ recommended
- **Disk Space:** 2GB for dependencies and runtime files

### Essential Dependencies

```text
PyQt6>=6.4.0
PyQt6-Qt6
PyQt6-sip
psutil
```

### Optional Dependencies (Enable Additional Features)

```text
pyautogui          # Automation and screenshot tools
moviepy            # Video editing capabilities
pillow             # Advanced image processing
cryptography       # Secure vault features
pytesseract        # OCR functionality
paramiko           # SSH client support
requests           # Network tools
```

### Development Setup

1. Configure your IDE to use the virtual environment
2. Enable hot-reload for faster development iterations
3. Run with logging to capture debug information:
   ```bash
   python Luxxer_OS.py 2>&1 | tee luxxer_debug.log
   ```

---

## Building Standalone Executables

### Using PyInstaller (Recommended)

#### Single-File Build (easier distribution, larger size):

```bash
pyinstaller --noconfirm --clean --onefile \
  --name LuxxerOS \
  --icon icon.ico \
  --add-data "Luxxer_OS.py;." \
  --add-data "BSOD.py;." \
  --add-data "Luxxer_OS_Start.py;." \
  --add-data "iconadderonmainscreen.py;." \
  --add-data "apps_extra.py;." \
  --add-data "apps_extra2.py;." \
  --add-data "apps_extra3.py;." \
  --add-data "applicationadder.py;." \
  --add-data "games_all.py;." \
  --add-data "settings_utils.py;." \
  --add-data "MotivationAIChat.py;." \
  --add-data "JokeGenerator.py;." \
  --add-data "RandomChallenge.py;." \
  --add-data "cursor.png;." \
  --add-data "cursor2.png;." \
  --add-data "*.ico;." \
  Luxxer_OS.py
```

#### Directory Build (faster startup, easier debugging):

```bash
pyinstaller --noconfirm --clean --onedir \
  --name LuxxerOS \
  --icon icon.ico \
  --add-data "cursor.png;." \
  --add-data "cursor2.png;." \
  --add-data "*.ico;." \
  Luxxer_OS.py
```

### Build Size Optimization

- **Expected size:** 500MB - 2GB (varies by platform and included dependencies)
- **Reduce size by:**
  - Using `--onedir` instead of `--onefile`
  - Excluding unused Qt plugins with `--exclude-module`
  - Removing optional dependencies not needed for your use case
  - Compressing with UPX (use cautiously as it may break some Qt components)

### Platform-Specific Notes

**Windows:**
- Build on Windows for Windows targets
- UAC prompts may appear for system monitoring tools
- Antivirus software may flag the executable (add exception if trusted)

**macOS:**
- Code signing required for distribution outside development
- Notarization needed for Gatekeeper compatibility
- Use `--windowed` flag to create `.app` bundle

**Linux:**
- AppImage format recommended for broad compatibility
- Ensure Qt platform plugins are included
- Test on target distribution (Ubuntu, Fedora, etc.)

---

## Project Structure & Files

### Core System Files

```
Luxxer_OS.py              # Main entry point and window management
BSOD.py                   # Supervised error handling system
Luxxer_OS_Start.py        # Startup screen and theme engine
iconadderonmainscreen.py  # Desktop icon management
settings_utils.py         # Configuration persistence
```

### Application Modules

```
apps_extra.py             # Extended utility applications
apps_extra2.py            # Additional productivity tools
apps_extra3.py            # Advanced system tools
applicationadder.py       # Dynamic app registration
games_all.py              # Entertainment applications
```

### Feature Modules

```
MotivationAIChat.py       # AI chat integration
JokeGenerator.py          # Entertainment features
RandomChallenge.py        # Gamification system
```

### Assets

```
icon.ico                  # Main application icon
cursor.png                # Primary custom cursor
cursor2.png               # Dock-specific cursor
*.ico                     # Application-specific icons
```

---

## Dependencies & Optional Features

### Tier 1: Core (Required)

| Package | Purpose | Fallback Behavior |
|---------|---------|-------------------|
| PyQt6 | UI framework | None - application won't run |
| psutil | System monitoring | Limited system info features |

### Tier 2: Enhanced Features (Recommended)

| Package | Purpose | Fallback Behavior |
|---------|---------|-------------------|
| pyautogui | Automation tools | Screenshot/recorder disabled |
| pillow | Image processing | Basic image viewing only |
| cryptography | Security features | Vault apps disabled |

### Tier 3: Advanced (Optional)

| Package | Purpose | Fallback Behavior |
|---------|---------|-------------------|
| moviepy | Video editing | Video editor unavailable |
| pytesseract | OCR capabilities | OCR tool disabled |
| paramiko | SSH functionality | SSH client disabled |
| requests | Network tools | API requester limited |

**Graceful Degradation:** Luxxer OS detects missing optional dependencies at runtime and disables only the affected features while maintaining core functionality.

---

## Custom Cursor System

### Overview

Version 3.0 introduces a sophisticated custom cursor system that provides visual consistency across the entire interface, including system-level context menus and dynamically created widgets.

### Implementation Details

**Cursor Files:**
- `cursor.png` - Main interface cursor (24x24px scaled)
- `cursor2.png` - Dock-specific cursor with fallback to `cursor.png`

**Key Features:**
- Global application-level cursor override using `QApplication.setOverrideCursor()`
- Automatic cursor application to all widgets including:
  - Main window and central widget
  - MDI area and viewport
  - Desktop icon area
  - Bottom dock
  - Context menus and dialogs
  - Dynamically created subwindows
- Fallback to platform default if custom cursors fail to load
- Proper cursor restoration on application exit

### Cursor Guidelines

**Creating Custom Cursors:**
1. Use 24x24px PNG images for optimal balance between visibility and performance
2. Include a clear hotspot indicator (top-left by default)
3. Test on all three themes (Transparent, White, Dark)
4. Ensure sufficient contrast against various backgrounds
5. Keep file size under 10KB for fast loading

**Technical Specifications:**
- **Format:** PNG with transparency
- **Recommended size:** 24x24 pixels
- **Color depth:** 32-bit RGBA
- **Hotspot:** (0, 0) top-left corner

---

## Performance & Optimization

### Startup Optimization

- **Lazy loading:** Applications instantiate only when launched
- **Module caching:** Frequently used modules remain in memory
- **Splash screen:** Minimal delay with async initialization
- **Config loading:** Fast JSON parsing with schema validation

### Runtime Performance

**Memory Management:**
- Proper widget disposal on close events
- Cleanup of animation objects after completion
- Efficient subwindow reuse for single-instance apps
- Periodic garbage collection triggers

**UI Responsiveness:**
- Worker threads for long-running operations
- Debouncing for rapid user actions (300ms default)
- Smooth animations with QPropertyAnimation
- Frame-rate optimized dock magnification (60 FPS target)

### Resource Usage Baselines

| Scenario | RAM Usage | CPU Usage |
|----------|-----------|-----------|
| Idle (desktop only) | 150-250 MB | <1% |
| 5 apps open | 300-500 MB | 2-5% |
| Heavy usage (10+ apps) | 600-900 MB | 5-15% |

---

## Supervised Error Handling (BSOD System)

### How It Works

The Blue Screen of Death (BSOD) system provides robust error recovery by supervising the main application in a parent process:

```
Parent Process (Monitor)
  └─> Child Process (Luxxer OS)
        ├─> Normal operation
        └─> On crash → BSOD UI with diagnostics
```

### Process Flow:

1. Parent launches child with stdout/stderr capture
2. Child runs Luxxer OS with custom exception hooks
3. On fatal error, child exits with non-zero code
4. Parent detects exit, displays BSOD with captured logs
5. User can restart or save diagnostics

### Error Categories

**Handled Gracefully:**
- Python exceptions (AttributeError, TypeError, etc.)
- Missing optional dependencies
- File I/O errors
- Network timeouts

**Requires Restart (BSOD):**
- Native crashes (segmentation faults)
- Unhandled exceptions in critical paths
- Qt internal errors
- Memory corruption

### Debugging with BSOD

The BSOD window provides:
- Full stack trace of the error
- Stdout/stderr logs from the session
- Exit code and signal information
- Timestamp and system context
- Restart button for quick recovery

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Issue: Application won't start
**Symptoms:** Double-click has no effect, or window closes immediately

**Solutions:**
1. Run from terminal to see error messages:
   ```bash
   python Luxxer_OS.py
   ```
2. Check Python version: `python --version` (need 3.9+)
3. Verify PyQt6 installation: `pip show PyQt6`
4. Check for missing dependencies: `pip install -r requirements.txt`

---

#### Issue: Custom cursors not appearing
**Symptoms:** Platform default cursor shown instead of custom

**Solutions:**
1. Verify `cursor.png` and `cursor2.png` exist in the application directory
2. Check file permissions (must be readable)
3. Ensure PNG format is valid (try opening in image viewer)
4. Check console for cursor loading warnings
5. **Fallback:** Application will use system cursor if custom fails

---

#### Issue: Dock appears black or empty
**Symptoms:** Bottom dock area is solid black with no icons

**Solutions:**
1. Right-click on dock → "Reset to Defaults"
2. Check `dock.json` configuration file for corruption
3. Delete `dock.json` to force regeneration
4. Verify application names in `apps_with_icons` list
5. Restart application after making changes

---

#### Issue: ModuleNotFoundError for specific apps
**Symptoms:** Individual applications fail to launch with import errors

**Solutions:**
1. Install missing module: `pip install <module_name>`
2. Check optional dependencies list in this README
3. For packaged builds, add `--hidden-import <module>` to PyInstaller command
4. Rebuild executable after adding dependencies

---

#### Issue: Native crashes with exit code -1073740791
**Symptoms:** Sudden application closure, BSOD appears with hex exit code

**Solutions:**
1. Update graphics drivers (often GPU-related)
2. Disable hardware acceleration in problematic apps
3. Check for conflicting Qt plugins
4. Run in compatibility mode (Windows)
5. Report crash with logs to [GitHub issues](https://github.com/Luka12-dev/LuxxerOS/issues)

---

## Testing & Quality Assurance

### Manual Testing Checklist

Before releases, verify:

- [ ] Application launches without errors
- [ ] All three themes render correctly
- [ ] Custom cursors appear throughout UI
- [ ] Dock magnification works smoothly
- [ ] At least 20 random apps launch successfully
- [ ] Subwindows can be resized, moved, closed
- [ ] Desktop icons can be added, moved, removed
- [ ] Settings persist across restarts
- [ ] Context menus appear at correct positions
- [ ] No memory leaks during 30-minute stress test

### Automated Testing

Run the test suite:
```bash
python -m pytest tests/
```

**Test Coverage Goals:**
- Core UI components: 80%+
- Application launchers: 70%+
- Configuration management: 90%+
- Error handling: 85%+

### Diagnostic Tools

**Built-in Diagnostics:**
```bash
# Run BSOD demo to test error handling
python BSOD.py

# Check for problematic super() usage
python isAll-ImportsHere.py

# Validate module imports
python -c "import Luxxer_OS; print('OK')"
```

**Performance Profiling:**
```bash
python -m cProfile -o profile.stats Luxxer_OS.py
python -m pstats profile.stats
```

---

## Security, Ethics & Legal Notice

### ⚠️ IMPORTANT - Read Before Use

Luxxer OS is an **educational platform** designed for learning in controlled environments. Some included tools can interact with system resources, networks, and devices.

### Ethical Use Guidelines

**You MUST:**
- ✅ Only use on systems you own or have explicit permission to test
- ✅ Respect all applicable laws and regulations in your jurisdiction
- ✅ Follow responsible disclosure for any vulnerabilities discovered
- ✅ Use tools in isolated environments (VMs, test networks)
- ✅ Document all experiments with clear intent and results
- ✅ Obtain consent before scanning or monitoring third-party systems

**You MUST NOT:**
- ❌ Access unauthorized systems, networks, or data
- ❌ Deploy malware or destructive code
- ❌ Violate privacy or data protection regulations
- ❌ Use tools for fraud, harassment, or illegal activities
- ❌ Bypass security controls on production systems
- ❌ Distribute modified versions with malicious intent

### Legal Responsibilities

By using Luxxer OS, you acknowledge that:

1. **Authorization Required:** Penetration testing, vulnerability scanning, and network enumeration require written permission
2. **Personal Liability:** You are solely responsible for your actions and their consequences
3. **No Warranty:** This software is provided "as-is" without guarantees
4. **Educational Purpose:** Tools are for learning, not production exploitation
5. **Compliance:** You will comply with all applicable laws (CFAA, GDPR, CCPA, etc.)

### Reporting Vulnerabilities

Found a security issue in Luxxer OS itself?

1. **DO NOT** publicly disclose until patched
2. Open a [security issue on GitHub](https://github.com/Luka12-dev/LuxxerOS/issues)
3. Include: Steps to reproduce, impact assessment, suggested fix
4. Allow 90 days for responsible disclosure timeline

### Privacy & Data Collection

Luxxer OS:
- ✅ Stores settings locally only (`app_state.json`, `dock.json`)
- ✅ Does not transmit telemetry or user data
- ✅ Does not include analytics or tracking
- ⚠️ Some apps may access local files, network interfaces, or system info when explicitly invoked

---

## Contributing to Luxxer OS

### How to Contribute

We welcome contributions! Here's how to get started:

1. **Fork** the repository on [GitHub](https://github.com/Luka12-dev/LuxxerOS)
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to your fork: `git push origin feature/amazing-feature`
5. **Open** a Pull Request with detailed description

### Contribution Guidelines

**Code Style:**
- Follow PEP 8 for Python code
- Use type hints where practical
- Document complex functions with docstrings
- Keep functions under 50 lines when possible

**Testing:**
- Add unit tests for new features
- Ensure existing tests pass
- Test on Windows, macOS, and Linux if possible
- Include manual testing steps in PR description

**Documentation:**
- Update README for significant changes
- Add inline comments for complex logic
- Update docstrings when modifying APIs
- Include screenshots for UI changes

**Commit Messages:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example:**
```
feat(dock): add custom cursor support with fallback

- Implemented QApplication.setOverrideCursor for global cursor
- Added cursor.png and cursor2.png loading with validation
- Cursor automatically applies to all widgets including context menus
- Falls back to system cursor if custom images fail to load

Closes #42
```

### Priority Areas for Contribution

- 🐛 Bug fixes (especially cross-platform issues)
- 📱 New application integrations
- 🎨 Theme improvements and customization
- 🌍 Internationalization and localization
- 📚 Documentation and tutorials
- 🧪 Test coverage expansion
- ♿ Accessibility enhancements

---

## Version History

### v3.0 (Current Release)

**Major Features:**
- ✨ Custom cursor system with global override
- 🐛 Fixed 50+ stability and crash issues
- 🎨 Polished theme engine with macOS-inspired design
- 🔧 Enhanced dock with robust configuration management
- 🪟 Improved window management with single-instance enforcement
- 🔄 Better error recovery with enhanced BSOD system

**Bug Fixes:**
- Fixed dock black screen issues
- Resolved zero-argument `super()` crashes
- Fixed `QTextCursor` enum compatibility
- Corrected context menu positioning
- Fixed memory leaks in widget lifecycle
- Resolved startup screen theme application

**Technical Improvements:**
- Refactored cursor application logic for consistency
- Enhanced configuration sanitization with type coercion
- Improved widget cleanup and layout rebuilding
- Better resource loading with graceful fallbacks
- Optimized animation performance and memory usage

### v2.0 (Previous Release)

**Major Features:**
- Redesigned Start Screen with ethical use agreement
- Introduced BSOD supervision system
- Added 30+ new applications
- Implemented modular app architecture
- Enhanced theme customization

### v1.0 (Initial Release)

**Major Features:**
- Basic desktop environment
- Core application suite
- Theme support
- Icon management

---

## Credits & Acknowledgements

### Core Development

- **Lead Developer:** Luka
- **Architecture:** Desktop environment simulation with PyQt6
- **Version:** 3.0

### Open Source Libraries

Special thanks to the maintainers of:

- **PyQt6** - Cross-platform UI framework
- **psutil** - System and process utilities
- **Pillow** - Python Imaging Library
- **moviepy** - Video editing capabilities
- **pyautogui** - GUI automation
- **cryptography** - Cryptographic recipes

### Community Contributors

Thanks to everyone who reported issues, suggested features, and contributed code to make Luxxer OS better.

### Inspiration

Desktop environment design inspired by:

- macOS Big Sur/Monterey UI/UX patterns
- Windows 11 fluent design system
- Various Linux desktop environments (KDE, GNOME)

---

## Frequently Asked Questions

### General Questions

**Q: Is Luxxer OS a real operating system?**  
A: No. Luxxer OS is a desktop environment simulator that runs as an application inside your existing OS (Windows, macOS, or Linux).

**Q: Can I use Luxxer OS for commercial purposes?**  
A: Check the LICENSE file. Generally, this is open-source for educational use; commercial deployment may require attribution or permission.

**Q: Why is the executable so large?**  
A: PyQt6 bundles a full Qt runtime (~400MB) plus Python interpreter and all dependencies. Single-file builds are convenient but larger than directory builds.

### Technical Questions

**Q: How do I add my own application to Luxxer OS?**  
A: Create a QWidget or QMainWindow subclass, add it to `APP_MAPPING` dictionary in `Luxxer_OS.py`, and include an icon in `APP_ICONS`.

**Q: Can I customize the cursors?**  
A: Yes! Replace `cursor.png` and `cursor2.png` with your own 24x24px PNG images.

**Q: Does Luxxer OS work offline?**  
A: Yes, completely. No network connection required except for apps that explicitly need internet (web browser, API tools, etc.).

**Q: Can I run Luxxer OS on Raspberry Pi?**  
A: Theoretically yes, but performance will be limited. Recommended: Raspberry Pi 4 with 4GB+ RAM.

### Troubleshooting Questions

**Q: Why does my antivirus flag the executable?**  
A: PyInstaller executables sometimes trigger false positives. Scan with VirusTotal and add exception if clean.

**Q: The application crashes immediately on macOS. How do I fix it?**  
A: Run from terminal to see errors. Often related to missing Qt platform plugins. Install via: `pip install PyQt6-Qt6`

**Q: Can I run multiple instances of Luxxer OS?**  
A: Yes, but they share the same `app_state.json` file. Changes in one instance may not appear in others until restart.

---

## Advanced Usage & Commands

### Developer Mode

Enable additional logging and debugging features:

```bash
# Maximum verbosity
python Luxxer_OS.py --verbose --debug

# Capture full trace on crash
python Luxxer_OS.py 2>&1 | tee full_trace.log

# Profile performance
python -m cProfile -o profile.stats Luxxer_OS.py
```

### Configuration Files

**Location:** Same directory as executable or `~/.luxxer/`

**Files:**
- `app_state.json` - User settings, desktop icons, theme preferences
- `dock.json` - Dock configuration (size, position, magnification)
- `luxxer.log` - Application logs (when logging enabled)

**Manual Configuration:**

```json
// app_state.json example
{
  "desktop_icons": ["Notebook", "Calculator", "Settings"],
  "settings": {
    "theme": "dark",
    "username": "YourName",
    "show_start": true,
    "wallpaper": "path/to/image.png"
  }
}
```

```json
// dock.json example
{
  "base_btn_size": 56,
  "max_scale": 1.8,
  "influence": 140.0,
  "spacing": 8,
  "position": "bottom",
  "magnification_enabled": true,
  "smoothness": 0.22
}
```

### Command-Line Arguments

```bash
# Skip startup screen
python Luxxer_OS.py --no-start

# Force theme
python Luxxer_OS.py --theme dark

# Custom config directory
python Luxxer_OS.py --config-dir /path/to/config

# Safe mode (minimal apps loaded)
python Luxxer_OS.py --safe-mode
```

### Batch Operations

**Reset all settings:**
```bash
rm app_state.json dock.json
python Luxxer_OS.py
```

**Backup configuration:**
```bash
cp app_state.json app_state.backup.json
cp dock.json dock.backup.json
```

**Export desktop layout:**  
From within Luxxer OS: Right-click desktop → Export Layout → Save JSON

---

## License

**MIT License**

Copyright (c) 2024 Luka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Support & Contact

- **Repository:** [https://github.com/Luka12-dev/LuxxerOS](https://github.com/Luka12-dev/LuxxerOS)
- **Issues:** [https://github.com/Luka12-dev/LuxxerOS/issues](https://github.com/Luka12-dev/LuxxerOS/issues)
- **Discussions:** [https://github.com/Luka12-dev/LuxxerOS/discussions](https://github.com/Luka12-dev/LuxxerOS/discussions)

---

**Thank you for using Luxxer OS! Happy exploring! 🚀**