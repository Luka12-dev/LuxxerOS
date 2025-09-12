import os
from PyQt6.QtWidgets import QMessageBox, QApplication
import sys

REQUIRED_FILES = [
    "Luxxer_OS.py",
    "apps_extra.py",
    "apps_extra2.py",
    "JokeGenerator.py",
    "MotivationAIChat.py",
    "ApplicationAdder.py",
    "games_all.py",
    "settings_utils.py",
    "start_menu_file.py",
    "Luxxer_OS_Start.py"
]

def check_files():
    missing = []
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for file in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(current_dir, file)):
            missing.append(file)

    return missing

def alert_missing_files(missing_files):
    app = QApplication.instance() or QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Luxxer OS - Missing Files")
    msg.setText(
        "⚠️ Luxxer OS cannot start properly.\n\n"
        "The following required file(s) are missing:\n\n"
        f"{', '.join(missing_files)}\n\n"
        "Please make sure all files are downloaded correctly, "
        "and check that your antivirus did not delete anything."
    )
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

def run_check():
    missing_files = check_files()
    if missing_files:
        alert_missing_files(missing_files)
        return False
    return True

if __name__ == "__main__":
    if not run_check():
        sys.exit(1)
