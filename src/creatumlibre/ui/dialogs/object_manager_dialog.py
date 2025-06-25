from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from creatumlibre.ui.manager.object_manager import ObjectManager


class ObjectManagerDialog(QDialog):
    """A dialog to show and manipulate the layers"""

    def __init__(self, object_manager: ObjectManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Object Manager")
        self.object_manager = object_manager

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Layer Stack (Top → Bottom)")
        self.layout.addWidget(self.label)

        self.layer_list = QListWidget()
        self.populate_layer_list()
        self.layout.addWidget(self.layer_list)

        # Placeholder button bar (can be removed or extended later)
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("↑ Move Up"))
        button_layout.addWidget(QPushButton("↓ Move Down"))
        button_layout.addWidget(QPushButton("✕ Delete"))
        self.layout.addLayout(button_layout)
        self.setMinimumSize(250, 400)

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        dialog_width = self.width()  # or self.width() after layout
        dialog_height = self.height()  # or self.height()

        x = screen_geometry.right() - dialog_width
        y = screen_geometry.top() + 100  # Offset from top for style

        self.setGeometry(x, y, dialog_width, dialog_height)

    def populate_layer_list(self):
        self.layer_list.clear()
        for idx, obj in enumerate(reversed(self.object_manager.object_list)):
            item = QListWidgetItem(
                f"Object {len(self.object_manager.object_list) - idx - 1}"
            )
            pixmap = obj.get_pixmap().scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
            item.setIcon(QIcon(pixmap))
            self.layer_list.addItem(item)

    def refresh(self):
        """external refrsh trigger"""
        self.populate_layer_list()
