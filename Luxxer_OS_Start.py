from PyQt6.QtWidgets import (
    QDialog, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QRadioButton, QLineEdit, QCheckBox, QTextEdit, QButtonGroup, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
try:
    from settings_utils import save_state
except Exception:
    save_state = None


def apply_theme_global(theme: str):
    qapp = QApplication.instance()
    if qapp is None:
        return

    t = (theme or "transparent").lower()
    if t == "dark":
        style = """
            QMainWindow { background-color: #121212; color: #fff; }
            QMdiSubWindow { background-color: #1e1e1e; color: #fff; border: 1px solid #444; }
            QPushButton, QToolButton { background-color: #2c2c2c; border-radius: 6px; color: #fff; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: #3c3c3c; }
        """
    elif t == "white":
        style = """
            QMainWindow { background-color: #ffffff; color: #000; }
            QMdiSubWindow { background-color: #ffffff; color: #000; border: 1px solid #e6e6e6; }
            QPushButton, QToolButton { background-color: #f0f0f0; border-radius: 6px; color: #000; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: #e8e8e8; }
        """
    else:  # transparent
        style = """
            QMainWindow { background-color: transparent; color: #fff; }
            QMdiSubWindow { background-color: rgba(255,255,255,0.02); color: #fff; border: 1px solid rgba(255,255,255,0.04); }
            QPushButton, QToolButton { background-color: rgba(0,0,0,0.55); border-radius: 6px; color: #fff; padding: 4px 8px; }
            QPushButton:hover, QToolButton:hover { background-color: rgba(0,0,0,0.65); }
        """
    qapp.setStyleSheet(style)


class StartScreen(QDialog):
    """
    Start dialog with mandatory ethical disclaimer.
    Shows only once (if accepted) by persisting show_start flag in app_state.
    """

    def __init__(self, app: QApplication, app_state: dict, parent=None):
        super().__init__(parent)
        self.app = app
        self.app_state = app_state
        self.app_state.setdefault('settings', {})

        self.setObjectName("start_root")
        self.setModal(True)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.setGraphicsEffect(shadow)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        # title
        title = QLabel("Welcome to Luxxer OS")
        title.setObjectName("title")

        subtitle = QLabel("Educational • Ethical • Open-source")
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        # License / disclaimer text
        license_box = QTextEdit()
        license_box.setObjectName("license")
        license_box.setReadOnly(True)
        license_box.setPlainText(
            "⚠️ Important Notice ⚠️\n\n"
            "Luxxer OS is provided strictly for educational, ethical, and research purposes.\n"
            "This project demonstrates how an experimental operating environment with apps "
            "and tools can be built using Python and PyQt.\n\n"
            "❌ Any use for malicious, harmful, or criminal activity is strictly forbidden.\n"
            "✅ You may use Luxxer OS for:\n"
            "   • Learning programming and cybersecurity concepts\n"
            "   • Ethical hacking practice in controlled environments\n"
            "   • Personal projects and experimentation\n\n"
            "By proceeding, you acknowledge responsibility for your actions and agree "
            "to use this project only in a safe and legal way."
        )
        license_box.setMinimumHeight(180)
        license_box.setMaximumHeight(240)

        # Name input
        name_label = QLabel("Display name (optional):")
        self.name_edit = QLineEdit()
        if self.app_state['settings'].get('username'):
            self.name_edit.setText(self.app_state['settings']['username'])

        # Theme selection
        theme_label = QLabel("Choose initial app background style:")
        self.rb_transparent = QRadioButton("Transparent (recommended)")
        self.rb_white = QRadioButton("White (classic)")
        self.rb_dark = QRadioButton("Dark")

        cur_theme = self.app_state['settings'].get('theme', 'transparent')
        if cur_theme == 'white':
            self.rb_white.setChecked(True)
        elif cur_theme == 'dark':
            self.rb_dark.setChecked(True)
        else:
            self.rb_transparent.setChecked(True)

        _bg = QButtonGroup(self)
        _bg.addButton(self.rb_transparent)
        _bg.addButton(self.rb_white)
        _bg.addButton(self.rb_dark)

        rb_layout = QHBoxLayout()
        rb_layout.addWidget(self.rb_transparent)
        rb_layout.addWidget(self.rb_white)
        rb_layout.addWidget(self.rb_dark)

        self.rb_transparent.toggled.connect(self._update_theme_preview)
        self.rb_white.toggled.connect(self._update_theme_preview)
        self.rb_dark.toggled.connect(self._update_theme_preview)

        # agreement checkbox (mandatory)
        self.chk_agree = QCheckBox("I have read and agree to the ethical use statement above.")
        self.chk_agree.setChecked(False)

        # hide forever
        self.chk_hide = QCheckBox("Don’t show this again on startup")
        self.chk_hide.setChecked(not self.app_state['settings'].get('show_start', True))

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_cancel = QPushButton("Exit")
        self.btn_cancel.setObjectName("cancel_btn")
        self.btn_continue = QPushButton("Continue")
        self.btn_continue.setObjectName("continue_btn")
        self.btn_continue.setEnabled(False)  # disabled until agreement checked
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_continue)

        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)
        root_layout.addWidget(license_box)
        root_layout.addWidget(name_label)
        root_layout.addWidget(self.name_edit)
        root_layout.addWidget(theme_label)
        root_layout.addLayout(rb_layout)
        root_layout.addWidget(self.chk_agree)
        root_layout.addWidget(self.chk_hide)
        root_layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QWidget#start_root {
                background-color: #ffffff;
                border-radius: 12px;
            }
            QLabel#title { font-size: 22px; font-weight: 700; }
            QLabel#subtitle { font-size: 13px; color: #666666; }
            QPushButton#continue_btn, QPushButton#cancel_btn {
                padding: 6px 12px;
                border-radius: 6px;
            }
        """)

        # signals
        self.chk_agree.toggled.connect(self._toggle_continue_enabled)
        self.btn_continue.clicked.connect(self._on_continue)
        self.btn_cancel.clicked.connect(self._on_cancel)

        self._center_to_parent()

    def _center_to_parent(self):
        screen = QApplication.primaryScreen()
        if not screen:
            self.resize(640, 420)
            return
        scr = screen.availableGeometry()
        w = min(720, int(scr.width() * 0.6))
        h = min(520, int(scr.height() * 0.6))
        x = (scr.width() - w) // 2
        y = (scr.height() - h) // 2
        self.setGeometry(x, y, w, h)

    def _update_theme_preview(self):
        theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        apply_theme_global(theme)

    def _toggle_continue_enabled(self, checked):
        self.btn_continue.setEnabled(checked)

    def _on_continue(self):
        theme = 'white' if self.rb_white.isChecked() else 'dark' if self.rb_dark.isChecked() else 'transparent'
        self.app_state['settings']['theme'] = theme
        self.app_state['settings']['username'] = self.name_edit.text().strip() or self.app_state['settings'].get('username', '')
        # Once agreed, force hide forever unless user unchecked manually
        self.app_state['settings']['show_start'] = not self.chk_hide.isChecked()

        if save_state:
            try:
                save_state(self.app_state)
            except Exception:
                pass

        apply_theme_global(theme)
        self.accept()

    def _on_cancel(self):
        self.reject()