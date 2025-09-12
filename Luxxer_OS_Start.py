from PyQt6.QtWidgets import (
    QDialog, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QRadioButton, QLineEdit, QCheckBox, QTextEdit, QButtonGroup,
    QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QGraphicsBlurEffect,
    QWidget
)
from PyQt6.QtGui import QColor, QFont, QPalette, QBrush, QLinearGradient
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel
from PyQt6.QtCore import Qt

def apply_theme_global(theme: str):
    qapp = QApplication.instance()
    if qapp is None:
        return

    t = (theme or "transparent").lower()

    # Define palettes / accents per theme
    if t == "white":
        accent = "#2563eb"
        bg_main = "#ffffff"
        bg_panel = "#ffffff"
        dock_bg = "#111111"
        text = "#000000"
        muted = "#4b5563"
        border = "1px solid #e5e7eb"
        scrollbar = "#d1d5db"
    elif t == "dark":
        accent = "#00bfa6"
        bg_main = "#0b0f12"
        bg_panel = "#0f1417"
        dock_bg = "#0c1113"
        text = "#e6f0f0"
        muted = "#94a3a8"
        border = "1px solid #22282b"
        scrollbar = "#263033"
    else:
        accent = "#7cc1ff"
        bg_main = "transparent"
        bg_panel = "rgba(18,18,20,0.78)"
        dock_bg = "rgba(12,12,14,0.62)"
        text = "#ffffff"
        muted = "rgba(255,255,255,0.72)"
        border = "1px solid rgba(255,255,255,0.06)"
        scrollbar = "rgba(255,255,255,0.12)"

    style = f"""
    QMainWindow, QDialog {{
        background: {bg_main};
        color: {text};
        font-family: "Segoe UI", Roboto, Arial, sans-serif;
        font-size: 13px;
    }}

    QWidget#card, QMdiSubWindow {{
        background: {bg_panel};
        color: {text};
        border: {border};
        border-radius: 12px;
    }}

    QWidget#sidebar {{
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(255,255,255,0.02), stop:1 rgba(255,255,255,0.01));
        background-color: {dock_bg};
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

    QToolButton.sidebar-btn {{
        background: transparent;
        border: none;
        margin: 6px 8px;
        padding: 10px;
        min-width: 48px;
        min-height: 48px;
        max-width: 64px;
        max-height: 64px;
        border-radius: 12px;
    }}
    QToolButton.sidebar-btn:hover {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 rgba(255,255,255,0.03), stop:1 rgba(0,0,0,0.03));
        transform: scale(1.02);
    }}
    QToolButton.sidebar-btn:pressed {{
        background: rgba(0,0,0,0.06);
    }}
    QToolButton.sidebar-btn[active="true"] {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {accent}22, stop:1 {accent}11);
        border-left: 4px solid {accent};
        padding-left: 6px;
    }}

    QToolButton.sidebar-btn QAbstractButton, QToolButton.sidebar-btn QLabel {{
        color: {text};
    }}

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
        background: rgba(0,0,0,0.03);
    }}
    QPushButton:pressed {{
        background: rgba(0,0,0,0.06);
    }}

    QPushButton#continue_btn, QPushButton.accent {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {accent}, stop:1 {accent}cc);
        color: #fff;
        border: none;
        padding: 8px 14px;
        min-height: 34px;
    }}
    QPushButton#continue_btn:hover, QPushButton.accent:hover {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {accent}cc, stop:1 {accent}99);
    }}
    QPushButton#continue_btn:disabled {{
        background: rgba(255,255,255,0.06);
        color: {muted};
    }}

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

    QToolBar, QDockWidget {{
        background: {dock_bg};
        border: {border};
        border-radius: 8px;
    }}

    .muted {{ color: {muted}; font-size: 12px; }}
    .small {{ padding: 4px 8px; min-height: 26px; font-size: 12px; border-radius: 6px; }}
    """

    qapp.setStyleSheet(style)

from PyQt6.QtWidgets import QScrollArea, QSizePolicy

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

        # Much longer ethical notice (expanded & improved English)
        self.license_box = QTextEdit()
        self.license_box.setObjectName("license")
        self.license_box.setReadOnly(True)
        self.license_box.setFont(QFont("Segoe UI", 13))
        long_notice = (
            "⚠️ IMPORTANT - Ethical Use Notice ⚠️\n\n"
            "Luxxer OS includes tools, examples, and utilities intended for learning, research, and ethical experimentation. "
            "This software is designed to teach and help you practice responsible techniques - not to be used for harm.\n\n"
            "Before you continue, please read and agree to the following points carefully:\n\n"
            "1) LEGAL & AUTHORIZATION - Always obtain explicit permission before scanning, testing, or otherwise interacting "
            "with systems, devices, or networks that you do not own. Unauthorized access is illegal in many jurisdictions and is unethical.\n\n"
            "2) RESPECT PRIVACY - Do not collect, publish, or expose other people\u2019s private information. If you encounter "
            "sensitive data, stop immediately and notify the rightful owner or administrator. Respect people\u2019s privacy at all times. 🔒🧑‍💻\n\n"
            "3) NON-MALICIOUS USE - Do not use Luxxer OS to create, distribute, or facilitate malware, fraud, intrusion, denial-of-service, "
            "or any activity that harms people, infrastructure, or property. If you are unsure, do not proceed. 🚫🛡️\n\n"
            "4) RESPONSIBLE DISCLOSURE - If you discover security vulnerabilities, follow responsible disclosure practices: "
            "document what you found, contact the owner securely, and avoid public exploitation. Help make systems safer. 📝🔁\n\n"
            "5) SAFETY & ETHICS - Use these tools to learn, to teach, or to improve security. Avoid actions that could harm users, devices, "
            "or services. Consider the real-world consequences of your tests before you run them. ⚖️🧯\n\n"
            "6) DOCUMENTATION & LEARNING - Test in controlled, isolated environments where possible (virtual machines, lab networks, "
            "or dedicated testbeds). Keep clear notes of what you test and why. Share findings responsibly and with permission. 📚🧪\n\n"
            "7) PROFESSIONALISM & RESPECT - Treat other people's systems and data with respect. Obtain consent, honor requests, and act "
            "with integrity. If you\u2019re learning, ask mentors or instructors for supervised exercises. 🤝💡\n\n"
            "8) USE CASES & LIMITATIONS - Some Luxxer OS tools are powerful and can change system state. Do not run destructive actions on "
            "production systems. If a tool requests elevated privileges, double-check the intent and the target. 🛠️⚠️\n\n"
            "9) PRIVACY INCIDENTS - If you unintentionally access sensitive information, stop immediately, document what happened, and "
            "contact the system owner. Do not copy or share sensitive data. Protect people's privacy. 🚨🔒\n\n"
            "10) COMMUNITY & CONTRIBUTION - We welcome improvements and thoughtful contributions. If you propose changes, include clear "
            "documentation and ethical usage notes so others can learn safely. 🤝📢\n\n"
            "IMPORTANT NOTE ABOUT THEMES & UI\n"
            "If you choose the Transparent theme - on some systems or GPU/driver combinations a visual issue may occur where the UI "
            "falls back to a dark or unexpected background. If that happens, please go to Settings (or right-click on desktop) and set "
            "the Theme to Dark or White, then switch back to Transparent. This will refresh the rendering and resolve the display issue in "
            "most cases. If problems persist, use White or Dark for a stable experience and report the issue with details (OS, GPU, driver).\n\n"
            "ACKNOWLEDGMENT & AGREEMENT\n"
            "By checking the box below and clicking Continue you confirm that you have read, understood, and agree to follow the guidance "
            "above. If you do not agree with these terms or you are uncertain about legal/ethical implications, do not continue. Exit now.\n\n"
            "If you need help getting started - consider using deliberately isolated virtual machines or containers and review the docs. "
            "If you find a bug or unexpected behavior, please report it with reproduction steps so we can fix it.\n\n"
            "Have fun learning and experimenting - responsibly! 🎉🔧🧠\n\n"
            "Quick tips:\n"
            "- Use VMs for risky experiments. 🖥️\n"
            "- Backup important data before testing. 💾\n"
            "- When in doubt, ask for permission. ✅\n\n"
            "Thank you for being responsible and ethical with Luxxer OS."
        )
        self.license_box.setPlainText(long_notice)
        self.license_box.setMinimumHeight(260)
        self.license_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card_layout.addWidget(self.license_box)

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

        # pick initial theme from state (default to transparent for nicer look)
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

        # effects & connections
        self._continue_op = QGraphicsOpacityEffect(self.btn_continue)
        self.btn_continue.setGraphicsEffect(self._continue_op)
        self._continue_op.setOpacity(0.45)

        self.btn_continue.clicked.connect(self._on_continue)
        self.btn_cancel.clicked.connect(self._on_cancel)
        self.rb_transparent.toggled.connect(self._update_theme_preview)
        self.rb_white.toggled.connect(self._update_theme_preview)
        self.rb_dark.toggled.connect(self._update_theme_preview)

        # animation bookkeeping
        self._animations = []
        self._continue_anim = None
        self._pulse_anim = None

        # Apply initial per-card theme (ensures card + license color match selection)
        initial_theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        self._apply_card_theme(initial_theme)

    def showEvent(self, ev):
        super().showEvent(ev)
        self._center_to_parent()
        self._min_time_passed = False
        self._countdown = self.MIN_WAIT_SECONDS
        self.countdown_label.setText(f"Please wait {self._countdown} s to enable Continue")
        self._countdown_timer.start()
        QTimer.singleShot(self.MIN_WAIT_SECONDS * 1000, self._on_min_time_elapsed)
        self._continue_op.setOpacity(0.45)
        self.btn_continue.setEnabled(False)
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
        scroll_widget = self.layout().itemAt(0).widget()
        card_widget = scroll_widget.widget()
        eff = card_widget.graphicsEffect()
        if not isinstance(eff, QGraphicsOpacityEffect):
            eff = QGraphicsOpacityEffect(card_widget)
            card_widget.setGraphicsEffect(eff)
        try:
            eff.setOpacity(0.0)
        except Exception:
            pass
        anim = QPropertyAnimation(eff, b"opacity")
        anim.setDuration(420)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        self._animations.append(anim)

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

        # set dynamic prop so stylesheet immediately reflects enabled state
        self.btn_continue.setProperty("active", True if can_enable else False)
        try:
            style = self.btn_continue.style()
            style.unpolish(self.btn_continue)
            style.polish(self.btn_continue)
        except Exception:
            pass
        self.btn_continue.update()

        try:
            if can_enable:
                self._continue_op.setOpacity(1.0)
                self.btn_continue.setFocus(Qt.FocusReason.TabFocusReason)
            else:
                self._continue_op.setOpacity(0.45)
        except Exception:
            pass

    def _update_theme_preview(self):
        # Choose a theme string and apply to card immediately
        theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        try:
            self._apply_card_theme(theme)
            # also apply global theme if function available
            try:
                apply_theme_global(theme)
            except Exception:
                pass
        except Exception:
            pass

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

        # apply to card
        card_css = f"""
            QWidget#card {{
                background: {card_bg};
                color: {text_color};
                border-radius: 14px;
            }}
        """
        self.card.setStyleSheet(card_css)

        # apply license box style (readable background + text)
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

        # inputs (name edit) background + text
        inp_css = f"QLineEdit {{ background: {input_bg}; color: {text_color}; border-radius:8px; padding:8px; }}"
        self.name_edit.setStyleSheet(inp_css)

        # title color
        self.title.setStyleSheet(f"color: {title_color};")
        self.subtitle.setStyleSheet(f"color: {text_color};")

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
            try: w.setEnabled(False)
            except Exception: pass

        self.btn_continue.setText("Accepted ✓")
        self.btn_continue.setEnabled(False)
        self.btn_continue.setProperty("active", False)
        try:
            style = self.btn_continue.style()
            style.unpolish(self.btn_continue); style.polish(self.btn_continue)
        except Exception:
            pass
        self.btn_continue.update()

        # small pulse to show acceptance
        try:
            if self._pulse_anim: self._pulse_anim.stop()
        except Exception:
            pass
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

        apply_theme_global(theme)
        QTimer.singleShot(120, self.accept)

    def _on_cancel(self):
        self.reject()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and self.btn_continue.isEnabled():
            self._on_continue(); return
        if event.key() == Qt.Key.Key_Escape:
            self._on_cancel(); return
        super().keyPressEvent(event)

    def closeEvent(self, ev):
        for a in self._animations:
            try: a.stop()
            except Exception: pass
        try:
            if self._continue_anim: self._continue_anim.stop()
        except Exception: pass
        try:
            if self._pulse_anim: self._pulse_anim.stop()
        except Exception: pass
        super().closeEvent(ev)