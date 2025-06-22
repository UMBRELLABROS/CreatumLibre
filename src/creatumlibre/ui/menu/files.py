# pylint: disable=too-few-public-methods

from PyQt6.QtGui import QAction, QKeySequence


class FileMenu:
    """Actions for file management, like load, and save"""

    def __init__(self, parent):
        file_menu = parent.menu_bar.addMenu("Files")

        file_actions = {
            "New": ("Ctrl+N", lambda: None),
            "Open": ("Ctrl+O", parent.load_new_image_dialog),
            "Save": ("Ctrl+S", lambda: None),
            "Save As": ("Ctrl+Shift+S", lambda: None),
            "Quit": ("Ctrl+Q", parent.close),
        }

        for name, (shortcut, function) in file_actions.items():
            action = QAction(name, parent)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(function)
            file_menu.addAction(action)
