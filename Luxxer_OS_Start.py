from PyQt6.QtWidgets import (
    QDialog, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QRadioButton, QLineEdit, QCheckBox, QTextEdit, QButtonGroup,
    QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QGraphicsBlurEffect,
    QWidget, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QColor, QFont, QPalette, QBrush, QLinearGradient, QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel
from PyQt6.QtCore import Qt

def apply_theme_global(theme: str):
    """
    Apply a macOS-like polished style for three themes:
      - "transparent" (default) : glassy / translucent
      - "white"                 : bright / crisp
      - "dark" or "black"       : deep / high-contrast
    Safe to call at startup or when switching themes.
    """
    qapp = QApplication.instance()
    if qapp is None:
        return

    t = (theme or "transparent").lower()

    # Default variables (transparent-style baseline)
    accent = "#7CC1FF"
    bg_main = "transparent"
    bg_panel = "rgba(18,18,20,0.78)"
    dock_bg = "rgba(12,12,14,0.62)"
    text = "#FFFFFF"
    muted = "rgba(255,255,255,0.72)"
    border = "1px solid rgba(255,255,255,0.06)"
    scrollbar = "rgba(255,255,255,0.12)"
    panel_gloss = "linear-gradient(to bottom, rgba(255,255,255,0.02), rgba(0,0,0,0.06))"

    # Per-theme palettes (macOS-inspired adjustments)
    if t == "white":
        accent = "#1E90FF"  # crisp blue accent
        bg_main = "qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #fbfdff, stop:1 #f3f7fb)"
        bg_panel = "#ffffff"
        dock_bg = "#f2f5f9"
        text = "#0B1220"
        muted = "#6b7280"
        border = "1px solid #e6eef7"
        scrollbar = "#cfd8e9"
        panel_gloss = "linear-gradient(to bottom, rgba(255,255,255,0.98), rgba(245,249,255,0.9))"

    elif t == "dark":
        accent = "#0EA5A9"  # teal-ish accent for contrast
        bg_main = "#0b0f12"
        bg_panel = "#0f1417"
        dock_bg = "#0c1113"
        text = "#E6F0F0"
        muted = "#94a3a8"
        border = "1px solid rgba(255,255,255,0.02)"
        scrollbar = "#263033"
        panel_gloss = "linear-gradient(to bottom, rgba(255,255,255,0.02), rgba(0,0,0,0.18))"

    else:
        # transparent / glassy (default)
        accent = "#7CC1FF"
        bg_main = "transparent"
        bg_panel = "rgba(28,30,32,0.62)"
        dock_bg = "rgba(20,22,24,0.55)"
        text = "#FFFFFF"
        muted = "rgba(255,255,255,0.72)"
        border = "1px solid rgba(255,255,255,0.06)"
        scrollbar = "rgba(255,255,255,0.12)"
        panel_gloss = "linear-gradient(to bottom, rgba(255,255,255,0.02), rgba(0,0,0,0.06))"

    # Build the final stylesheet (common rules + theme-specific values)
    style = f"""
    /* --- Global base --- */
    QMainWindow, QDialog {{
        background: {bg_main};
        color: {text};
        font-family: "Segoe UI", "San Francisco", "Helvetica Neue", Roboto, Arial, sans-serif;
        font-size: 13px;
    }}

    /* Cards & Subwindows: rounded + soft shadow (macOS-like) */
    QWidget#card, QMdiSubWindow {{
        background: {bg_panel};
        color: {text};
        border: {border};
        border-radius: 12px;
        padding: 10px;
        background-image: {panel_gloss};
    }}
    QMdiSubWindow {{
        /* subtle shadow for floating windows */
        qproperty-windowOpacity: 1.0;
    }}

    /* Sidebar / dock */
    QWidget#sidebar {{
        background: {dock_bg};
        border-right: {border};
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
        padding-top: 12px;
    }}
    QLabel#sidebar_title {{
        font-weight: 700;
        padding: 6px 12px;
        margin-bottom: 6px;
        color: {text};
    }}

    /* Sidebar buttons (icon buttons) */
    QToolButton.sidebar-btn {{
        background: transparent;
        border: none;
        margin: 6px 8px;
        padding: 8px;
        min-width: 48px;
        min-height: 48px;
        max-width: 64px;
        max-height: 64px;
        border-radius: 12px;
    }}
    QToolButton.sidebar-btn:hover {{
        background: rgba(255,255,255,0.04);
        transform: scale(1.02);
    }}
    QToolButton.sidebar-btn:pressed {{
        background: rgba(255,255,255,0.02);
    }}
    QToolButton.sidebar-btn[active="true"] {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {accent}22, stop:1 {accent}11);
        border-left: 4px solid {accent};
        padding-left: 6px;
    }}
    QToolButton.sidebar-btn QAbstractButton, QToolButton.sidebar-btn QLabel {{
        color: {text};
    }}

    /* Buttons and toolbar: clean rounded buttons */
    QPushButton, QToolButton {{
        background: transparent;
        color: {text};
        border: {border};
        border-radius: 8px;
        padding: 6px 10px;
        min-height: 30px;
        font-weight: 600;
    }}
    QPushButton:hover, QToolButton:hover {{
        background: rgba(255,255,255,0.03);
    }}
    QPushButton:pressed {{
        background: rgba(0,0,0,0.06);
    }}

    /* Accent / primary action button (Continue etc.) */
    QPushButton#continue_btn, QPushButton.accent {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {accent}, stop:1 {accent}cc);
        color: #fff;
        border: none;
        padding: 8px 14px;
        min-height: 34px;
        border-radius: 10px;
        font-weight: 700;
    }}
    QPushButton#continue_btn:hover, QPushButton.accent:hover {{
        filter: brightness(1.04);
    }}
    QPushButton#continue_btn:disabled {{
        background: rgba(255,255,255,0.06);
        color: {muted};
    }}

    /* Inputs */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background: {bg_panel};
        color: {text};
        border: {border};
        border-radius: 8px;
        padding: 8px;
        selection-background-color: {accent};
        selection-color: #fff;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {accent};
        outline: none;
    }}

    /* Radios / checkboxes */
    QRadioButton, QCheckBox {{
        color: {text};
        spacing: 6px;
        font-size: 13px;
    }}
    QRadioButton::indicator, QCheckBox::indicator {{
        width: 14px; height: 14px;
        border-radius: 4px;
        border: 1px solid rgba(0,0,0,0.12);
        background: transparent;
    }}
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {{
        background: {accent};
        border: 1px solid {accent};
    }}

    /* Scrollbars: thin & subtle */
    QScrollBar:horizontal {{
        height: 8px; background: transparent; margin: 8px 12px;
    }}
    QScrollBar::handle:horizontal {{
        background: {scrollbar}; min-width: 20px; border-radius: 4px;
    }}
    QScrollBar:vertical {{
        width: 8px; background: transparent; margin: 12px 8px;
    }}
    QScrollBar::handle:vertical {{
        background: {scrollbar}; min-height: 20px; border-radius: 4px;
    }}

    /* Toolbars & docks */
    QToolBar, QDockWidget {{
        background: {dock_bg};
        border: {border};
        border-radius: 8px;
    }}

    /* handy helper classes */
    .muted {{ color: {muted}; font-size: 12px; }}
    .small {{ padding: 4px 8px; min-height: 26px; font-size: 12px; border-radius: 6px; }}
    """

    # Apply stylesheet safely
    try:
        qapp.setStyleSheet(style)
    except Exception:
        try:
            qapp.setStyleSheet("")  # fallback no style
        except Exception:
            pass

class StartScreen(QDialog):
    MIN_WAIT_SECONDS = 1

    def __init__(self, app: QApplication, app_state: dict, parent=None):
        super().__init__(parent)
        self.app = app
        self.app_state = app_state or {}
        self.app_state.setdefault('settings', {})

        # internal state
        self._min_time_passed = False
        self._countdown = self.MIN_WAIT_SECONDS
        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._tick_countdown)

        # window flags & sizing
        self.setObjectName("start_root")
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(880, 560)
        self.setMaximumSize(1400, 900)

        # central panel (shadowed card)
        self.card = QWidget(self)
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(26, 22, 26, 22)
        card_layout.setSpacing(14)

        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(38)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.card.setGraphicsEffect(shadow)

        # scroll container so long content never overlaps
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(0)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(self.card)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        # widgets
        self.title = QLabel("Welcome to Luxxer OS")
        self.title.setObjectName("title")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Educational · Ethical · Open-source")
        self.subtitle.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.subtitle)

        # license box
        self.license_box = QTextEdit()
        self.license_box.setObjectName("license")
        self.license_box.setReadOnly(True)
        self.license_box.setFont(QFont("Segoe UI", 13))
        # (trimmed for brevity in this snippet — replace or keep your long_notice content)
        long_notice = (
            "⚠️ IMPORTANT - Ethical Use & Responsible Learning Notice ⚠️\n\n"
            "Welcome to Luxxer OS, an educational and ethical platform designed for learners, researchers, and cybersecurity enthusiasts. "
            "This environment provides a safe space to practice, experiment, and understand system security without causing harm.\n\n"

            "Before proceeding, please read, understand, and agree to the following guidance carefully:\n\n"

            "1) LEGAL & AUTHORIZATION - Always obtain explicit written or verbal permission before interacting with systems, networks, "
            "or devices you do not own. Unauthorized access is illegal and unethical. Respect all laws applicable in your region. ⚖️\n\n"

            "2) RESPECT PRIVACY - Never collect, store, or share personal or private data without proper authorization. If you "
            "accidentally access sensitive information, stop immediately and notify the owner. Privacy is paramount. 🔒🧑‍💻\n\n"

            "3) NON-MALICIOUS USE - Luxxer OS is designed for education and research. Do not attempt malware creation, fraud, "
            "intrusion, denial-of-service attacks, or anything that could harm people, infrastructure, or property. 🚫🛡️\n\n"

            "4) RESPONSIBLE DISCLOSURE - If you identify security vulnerabilities, follow responsible disclosure: document findings, "
            "notify the owner securely, and avoid public exploitation. Contribute to safer systems. 📝🔁\n\n"

            "5) SAFETY & ETHICS - Always consider the real-world impact of your actions. Avoid harm to users, devices, and services. "
            "Test in isolated environments where possible. ⚖️🧯\n\n"

            "6) DOCUMENTATION & LEARNING - Maintain detailed notes of all your experiments. Understand what you did, why, and what the outcome was. "
            "Documenting is critical for learning and teaching others responsibly. 📚🧪\n\n"

            "7) PROFESSIONALISM & RESPECT - Treat all systems, data, and peers with respect. Obtain consent, honor requests, and "
            "engage in supervised learning if necessary. Ask mentors when unsure. 🤝💡\n\n"

            "8) USE CASES & LIMITATIONS - Some tools in Luxxer OS can modify system states. Avoid running destructive actions on "
            "production systems. Always verify the target and intent before elevating privileges. 🛠️⚠️\n\n"

            "9) PRIVACY INCIDENTS - If sensitive information is accessed unintentionally, document the incident, stop immediately, "
            "and contact the system owner. Never copy or expose data. Protect all individuals' privacy. 🚨🔒\n\n"

            "10) COMMUNITY & CONTRIBUTION - Share your improvements and insights responsibly. Include documentation, context, "
            "and guidance to help others learn ethically. 🤝📢\n\n"

            "11) CUSTOMIZATION & PERSONALIZATION - Luxxer OS allows you to choose themes, interface layouts, and display settings. "
            "Use these options to create a comfortable, productive, and visually appealing environment. Your choices can impact usability and focus. 🎨💻\n\n"

            "12) BACKUP & DATA SAFETY - Always back up your important files before testing or experimenting. Use snapshots, version "
            "control, or virtual machine checkpoints. Backup culture is a habit of professional practitioners. 💾🖥️\n\n"

            "13) VIRTUALIZATION & ISOLATION - Use virtual machines, containers, or lab networks for experimentation. "
            "Isolated environments prevent accidental damage and provide safe testing grounds. 🖥️🔧\n\n"

            "14) LEARNING PATHS - Start with beginner-friendly exercises, then progress to more complex scenarios. "
            "Focus on understanding fundamentals before attempting advanced techniques. Learning is iterative. 📘🧠\n\n"

            "15) MONITORING & ANALYSIS - Track your experiments, capture logs, and analyze outcomes. Understanding results "
            "is as important as performing actions. 📊🔍\n\n"

            "16) ETHICAL MINDSET - Ethics are non-negotiable. Always ask: Is this legal? Is this ethical? Could this harm someone? "
            "If any answer is NO or UNCERTAIN, stop and reconsider. 🛡️⚖️\n\n"

            "17) COMMUNITY GUIDELINES - Participate respectfully in forums, documentation, and collaborative exercises. "
            "Mentor, ask questions, and contribute positively. 💬🤝\n\n"

            "18) TROUBLESHOOTING & SUPPORT - If Luxxer OS behaves unexpectedly or bugs occur, document steps to reproduce the issue, "
            "and report clearly to maintainers. This ensures fast resolution and improves the platform. 🐛📩\n\n"

            "19) CONTINUOUS IMPROVEMENT - Cybersecurity is constantly evolving. Keep learning, updating your skills, and refining your "
            "knowledge base. Stay curious and responsible. 🔄🧠\n\n"

            "20) FINAL ACKNOWLEDGEMENT - By checking the box and clicking Continue, you confirm that you understand and accept "
            "the ethical, legal, and professional guidelines above. If unsure, exit and review documentation or seek mentorship.\n\n"

            "Thank you for using Luxxer OS responsibly. Explore, learn, and grow ethically! 🚀🔧🧑‍💻"
        )

        self.license_box.setPlainText(long_notice)
        self.license_box.setMinimumHeight(260)
        self.license_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card_layout.addWidget(self.license_box)

        # name
        name_row_label = QLabel("Display name (optional):")
        name_row_label.setFont(QFont("Segoe UI", 13))
        card_layout.addWidget(name_row_label)

        self.name_edit = QLineEdit(self.app_state['settings'].get('username', ""))
        self.name_edit.setFont(QFont("Segoe UI", 13))
        self.name_edit.setPlaceholderText("Enter your name (optional)...")
        self.name_edit.setMinimumHeight(36)
        card_layout.addWidget(self.name_edit)

        theme_label = QLabel("Choose initial app background style:")
        theme_label.setFont(QFont("Segoe UI", 13))
        card_layout.addWidget(theme_label)

        # radio buttons
        self.rb_transparent = QRadioButton("Transparent (recommended)")
        self.rb_white = QRadioButton("White (classic)")
        self.rb_dark = QRadioButton("Dark (recommended)")
        for rb in (self.rb_transparent, self.rb_white, self.rb_dark):
            rb.setFont(QFont("Segoe UI", 13))

        # pick initial theme from state (default to transparent)
        cur_theme = self.app_state['settings'].get('theme', 'transparent')
        if cur_theme == 'white':
            self.rb_white.setChecked(True)
        elif cur_theme == 'dark':
            self.rb_dark.setChecked(True)
        else:
            self.rb_transparent.setChecked(True)

        bg_group = QButtonGroup(self)
        bg_group.addButton(self.rb_transparent)
        bg_group.addButton(self.rb_white)
        bg_group.addButton(self.rb_dark)

        rb_layout = QHBoxLayout()
        rb_layout.setSpacing(12)
        rb_layout.addWidget(self.rb_transparent)
        rb_layout.addWidget(self.rb_white)
        rb_layout.addWidget(self.rb_dark)
        card_layout.addLayout(rb_layout)

        # checkboxes
        self.chk_agree = QCheckBox("I have read and agree to the ethical use statement above.")
        self.chk_agree.setFont(QFont("Segoe UI", 13))
        self.chk_agree.toggled.connect(self._update_continue_state)
        card_layout.addWidget(self.chk_agree)

        self.chk_hide = QCheckBox("Don't show this on startup again")
        self.chk_hide.setFont(QFont("Segoe UI", 13))
        self.chk_hide.setChecked(not self.app_state['settings'].get('show_start', True))
        card_layout.addWidget(self.chk_hide)

        self.countdown_label = QLabel(f"Please wait {self._countdown} s to enable Continue")
        self.countdown_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Light))
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.countdown_label)

        # buttons row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_cancel = QPushButton("Exit")
        self.btn_cancel.setObjectName("cancel_btn")
        self.btn_cancel.setFont(QFont("Segoe UI", 13))
        self.btn_cancel.setMinimumHeight(42)

        self.btn_continue = QPushButton("Continue")
        self.btn_continue.setObjectName("continue_btn")
        self.btn_continue.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        self.btn_continue.setMinimumHeight(42)
        self.btn_continue.setEnabled(False)
        self.btn_continue.setProperty("active", False)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_continue)
        card_layout.addLayout(btn_layout)

        # general stylesheet (keeps other rules, but card visuals are set per-theme below)
        self.setStyleSheet("""
            QWidget#start_root { background: transparent; }
            QPushButton#continue_btn[active="true"] {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #28a745, stop:1 #1f7f2d);
                color: white; font-weight:700;
            }
            QPushButton#continue_btn[active="false"] {
                background: rgba(160,160,160,0.5); color: rgba(255,255,255,0.85);
            }
            QPushButton#continue_btn:hover { transform: scale(1.02); }
            QPushButton#cancel_btn {
                background: transparent; color: #55636a; border: 1px solid #d8dfe4; padding:8px 14px; border-radius:10px;
            }
            QLineEdit { background:#fff; border:1px solid #e0e6eb; border-radius:8px; padding:8px; }
            QRadioButton::indicator:checked, QCheckBox::indicator:checked { background-color:#0d6efd; border:none; }
        """)

        # effects & connections: create BEFORE calling reset to avoid attribute errors
        self._continue_op = QGraphicsDropShadowEffect()  # temporary placeholder, replaced with opacity effect
        # we need a QGraphicsOpacityEffect for the button opacity control:
        try:
            from PyQt6.QtWidgets import QGraphicsOpacityEffect
            self._continue_op = QGraphicsOpacityEffect(self.btn_continue)
            self.btn_continue.setGraphicsEffect(self._continue_op)
            self._continue_op.setOpacity(0.45)
        except Exception:
            # if QGraphicsOpacityEffect isn't available for any reason, keep going without crashing
            self._continue_op = None

        # connect buttons and theme toggles
        self.btn_continue.clicked.connect(self._on_continue)
        self.btn_cancel.clicked.connect(self._on_cancel)
        self.rb_transparent.toggled.connect(self._update_theme_preview)
        self.rb_white.toggled.connect(self._update_theme_preview)
        self.rb_dark.toggled.connect(self._update_theme_preview)

        # animation bookkeeping
        self._animations = []
        self._continue_anim = None
        self._pulse_anim = None

        # Apply initial per-card theme now that widget tree exists
        initial_theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        self._apply_card_theme(initial_theme)
        try:
            apply_theme_global(initial_theme)
        except Exception:
            pass

    # showEvent: reset state & start countdown each time dialog is shown
    def showEvent(self, ev):
        super().showEvent(ev)
        self._center_to_parent()
        self._reset_state()
        self._countdown_timer.start()
        QTimer.singleShot(self.MIN_WAIT_SECONDS * 1000, self._on_min_time_elapsed)
        # small entrance animation
        QTimer.singleShot(60, self._animate_card_in)

    def _center_to_parent(self):
        screen = QApplication.primaryScreen()
        if not screen:
            self.resize(900, 700)
            return
        scr = screen.availableGeometry()
        w = min(1000, int(scr.width() * 0.72))
        h = min(820, int(scr.height() * 0.78))
        x = (scr.width() - w) // 2
        y = (scr.height() - h) // 2
        self.setGeometry(x, y, w, h)

    def _animate_card_in(self):
        try:
            scroll_widget = self.layout().itemAt(0).widget()
            card_widget = scroll_widget.widget()

            # always use QGraphicsOpacityEffect for fade animation
            from PyQt6.QtWidgets import QGraphicsOpacityEffect
            eff = QGraphicsOpacityEffect(card_widget)
            card_widget.setGraphicsEffect(eff)
            eff.setOpacity(0.0)  # this is now valid

            anim = QPropertyAnimation(eff, b"opacity")
            anim.setDuration(420)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.start()
            self._animations.append(anim)

            # optionally, keep the drop shadow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(38)
            shadow.setOffset(0, 12)
            shadow.setColor(QColor(0, 0, 0, 150))
            # combine opacity + shadow by wrapping shadow in a container if needed
            # but for simplicity, just keep opacity effect here
        except Exception:
            traceback.print_exc()

    def _tick_countdown(self):
        self._countdown -= 1
        if self._countdown <= 0:
            self.countdown_label.setText("You may now click Continue (if you agree).")
            self._countdown_timer.stop()
        else:
            self.countdown_label.setText(f"Please wait {self._countdown} s to enable Continue")

    def _on_min_time_elapsed(self):
        self._min_time_passed = True
        self._update_continue_state()

    def _update_continue_state(self):
        can_enable = self._min_time_passed and self.chk_agree.isChecked()
        self.btn_continue.setEnabled(can_enable)
        self.btn_continue.setProperty("active", True if can_enable else False)
        try:
            style = self.btn_continue.style()
            style.unpolish(self.btn_continue)
            style.polish(self.btn_continue)
        except Exception:
            pass
        self.btn_continue.update()

        try:
            if can_enable and self._continue_op is not None:
                self._continue_op.setOpacity(1.0)
                self.btn_continue.setFocus(Qt.FocusReason.TabFocusReason)
            elif self._continue_op is not None:
                self._continue_op.setOpacity(0.45)
        except Exception:
            pass

    def _update_theme_preview(self):
        theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        try:
            self._apply_card_theme(theme)
            try:
                apply_theme_global(theme)
            except Exception:
                pass
        except Exception:
            traceback.print_exc()

    def _apply_card_theme(self, theme: str):
        t = (theme or "transparent").lower()
        if t == "white":
            card_bg = "#ffffff"
            text_color = "#111827"
            license_bg = "#ffffff"
            license_border = "1px solid #e3e7ea"
            input_bg = "#ffffff"
            title_color = "#111827"
        elif t == "dark":
            card_bg = "#0f1417"
            text_color = "#e6f0f0"
            license_bg = "#0f1417"
            license_border = "1px solid rgba(255,255,255,0.04)"
            input_bg = "#0f1417"
            title_color = "#e6f0f0"
        else:  # transparent
            card_bg = "transparent"
            text_color = "#ffffff"
            license_bg = "rgba(255,255,255,0.04)"
            license_border = "1px solid rgba(255,255,255,0.06)"
            input_bg = "rgba(255,255,255,0.06)"
            title_color = "#ffffff"

        card_css = f"""
            QWidget#card {{
                background: {card_bg};
                color: {text_color};
                border-radius: 14px;
            }}
        """
        self.card.setStyleSheet(card_css)

        lic_css = f"""
            QTextEdit#license {{
                background: {license_bg};
                border: {license_border};
                padding:10px;
                border-radius:10px;
                color: {text_color};
                font-size:13px;
            }}
        """
        self.license_box.setStyleSheet(lic_css)

        inp_css = f"QLineEdit {{ background: {input_bg}; color: {text_color}; border-radius:8px; padding:8px; }}"
        self.name_edit.setStyleSheet(inp_css)

        self.title.setStyleSheet(f"color: {title_color};")
        self.subtitle.setStyleSheet(f"color: {text_color};")

    def _reset_state(self):
        """
        Reset dynamic state so dialog is 'fresh' each time it is shown.
        This is safe to call multiple times.
        """
        # Stop and reset countdown
        try:
            if self._countdown_timer.isActive():
                self._countdown_timer.stop()
        except Exception:
            pass

        self._countdown = self.MIN_WAIT_SECONDS
        self._min_time_passed = False
        try:
            self.countdown_label.setText(f"Please wait {self._countdown} s to enable Continue")
        except Exception:
            pass

        # Continue button visual + state
        try:
            self.btn_continue.setEnabled(False)
            self.btn_continue.setProperty("active", False)
            try:
                style = self.btn_continue.style()
                style.unpolish(self.btn_continue)
                style.polish(self.btn_continue)
            except Exception:
                pass
        except Exception:
            pass

        # Opacity effect guard
        if getattr(self, "_continue_op", None) is not None:
            try:
                self._continue_op.setOpacity(0.45)
            except Exception:
                pass

        # Checkboxes
        try:
            self.chk_agree.setChecked(False)
            self.chk_hide.setChecked(not self.app_state['settings'].get('show_start', True))
        except Exception:
            pass

        # Name field restore
        try:
            self.name_edit.setText(self.app_state['settings'].get('username', ""))
        except Exception:
            pass

        # Restore theme radios from saved settings (but don't re-apply global here;
        # showEvent will call _apply_card_theme and apply_theme_global)
        cur_theme = self.app_state['settings'].get('theme', 'transparent')
        try:
            if cur_theme == 'white':
                self.rb_white.setChecked(True)
            elif cur_theme == 'dark':
                self.rb_dark.setChecked(True)
            else:
                self.rb_transparent.setChecked(True)
        except Exception:
            pass

    def _on_continue(self):
        theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        self.app_state['settings']['theme'] = theme
        self.app_state['settings']['username'] = self.name_edit.text().strip() or self.app_state['settings'].get('username', '')
        self.app_state['settings']['show_start'] = not self.chk_hide.isChecked()
        try:
            from settings_utils import save_state
            save_state(self.app_state)
        except Exception:
            pass

        for w in (self.chk_agree, self.chk_hide, self.name_edit, self.rb_transparent, self.rb_white, self.rb_dark, self.btn_cancel):
            try:
                w.setEnabled(False)
            except Exception:
                pass

        self.btn_continue.setText("Accepted ✓")
        self.btn_continue.setEnabled(False)
        self.btn_continue.setProperty("active", False)
        try:
            style = self.btn_continue.style()
            style.unpolish(self.btn_continue)
            style.polish(self.btn_continue)
        except Exception:
            pass
        self.btn_continue.update()

        # pulse animation for feedback
        try:
            if self._pulse_anim:
                self._pulse_anim.stop()
        except Exception:
            pass

        try:
            g = self.btn_continue.geometry()
            enlarged = QRect(g.x()-6, g.y()-4, g.width()+12, g.height()+8)
            pulse = QPropertyAnimation(self.btn_continue, b"geometry")
            pulse.setDuration(360)
            pulse.setKeyValueAt(0, g)
            pulse.setKeyValueAt(0.5, enlarged)
            pulse.setKeyValueAt(1, g)
            pulse.setEasingCurve(QEasingCurve.Type.InOutQuad)
            pulse.start()
            self._pulse_anim = pulse
        except Exception:
            pass

        # apply theme globally and close
        try:
            apply_theme_global(theme)
        except Exception:
            pass

        QTimer.singleShot(120, self.accept)

    def _on_cancel(self):
        # reset but don't start timer here; dialog will be hidden
        try:
            self._reset_state()
        except Exception:
            pass
        self.reject()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and self.btn_continue.isEnabled():
            self._on_continue()
            return
        if event.key() == Qt.Key.Key_Escape:
            self._on_cancel()
            return
        super().keyPressEvent(event)

    def closeEvent(self, ev):
        for a in self._animations:
            try:
                a.stop()
            except Exception:
                pass
        try:
            if self._continue_anim:
                self._continue_anim.stop()
        except Exception:
            pass
        try:
            if self._pulse_anim:
                self._pulse_anim.stop()
        except Exception:
            pass
        super().closeEvent(ev)