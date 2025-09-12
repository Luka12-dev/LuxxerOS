from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt6.QtCore import Qt

class StartMenu(QWidget):
    def __init__(self, main_ref):
        super().__init__()
        self.main_ref = main_ref
        self.setWindowTitle("Start - Luxxer")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.welcome_label = QLabel("Welcome")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.welcome_label)

        self.scroll = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        self.buttons = {}
        for app_name in self.apps:
            btn = QPushButton(app_name)  # više nema tr()
            btn.clicked.connect(lambda checked, name=app_name: self.launch_app(name))
            self.scroll_layout.addWidget(btn)
            self.buttons[app_name] = btn

    def launch_app(self, app_name):
        if hasattr(self.main_ref, 'launch_app'):
            self.main_ref.launch_app(app_name)

    def update_texts(self):
        self.setWindowTitle("Start - Luxxer")
        self.welcome_label.setText("Welcome")
        for app_name, btn in self.buttons.items():
            btn.setText(app_name)