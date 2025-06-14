# pylint: disable=too-few-public-methods

from PyQt6.QtGui import QAction, QKeySequence


class ZoomMenu:
    def __init__(self, parent):
        zoom_menu = parent.menu_bar.addMenu("Zoom")

        zoom_actions = {
            "Zoom In": ("Ctrl++", lambda: None),
            "Zoom Out": ("Ctrl+-", lambda: None),
            "Fit to Frame": ("Ctrl+#", lambda: None),
            "Reset": ("Ctrl+.", lambda: None),
        }

        for name, (shortcut, function) in zoom_actions.items():
            action = QAction(name, parent)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(function)  # Assign function properly
            zoom_menu.addAction(action)
