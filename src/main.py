import sys

from PyQt6.QtWidgets import QApplication  # pylint: disable = no-name-in-module

from ui.base import CreatumLibre


def main():
    app = QApplication(sys.argv)
    window = CreatumLibre()
    window.show()
    sys.exit(app.exec())
