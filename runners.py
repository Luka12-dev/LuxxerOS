from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class _DesktopItemRunner(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        layout = QVBoxLayout(self)
        label = QLabel(f"Runner for:\n{path}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)