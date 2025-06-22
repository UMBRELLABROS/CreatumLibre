import sys

from PyQt6.QtWidgets import QApplication

from creatumlibre.ui.root_ui import RootUi  # pylint: disable = no-name-in-module


def main():
    app = QApplication(sys.argv)
    window = RootUi()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
