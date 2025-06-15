from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QToolButton, QVBoxLayout, QWidget

from ui.dialogs.color_adjustment_dialog import ColorAdjustmentDialog


class LeftSidebar(QWidget):
    """Sidebar with an icon to open the color adjustment dialog."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.color_adjustment_dialog = ColorAdjustmentDialog(
            self, self.parent.image_manager
        )  # Pass image manager to dialog

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # ✅ Remove all margins
        layout.setSpacing(0)  # ✅ Remove spacing

        # ✅ Create button with fully covering icon
        self.color_adjustment_button = QToolButton(self)
        icon_path = "src/assets/color.png"
        pixmap = QPixmap(icon_path).scaled(80, 80)  # ✅ Scale icon to fit button size
        self.color_adjustment_button.setIcon(QIcon(pixmap))

        self.color_adjustment_button.setIconSize(
            QSize(80, 80)
        )  # ✅ Make icon match button size
        self.color_adjustment_button.setStyleSheet(
            "border: none; padding: 0px;"
        )  # ✅ Remove borders & padding

        layout.addWidget(self.color_adjustment_button)

        self.setLayout(layout)

        self.color_adjustment_button.clicked.connect(
            self.color_adjustment_dialog.show
        )  # Opens dialog

        # Add button to sidebar layout
        parent.left_sidebar_layout.addWidget(self.color_adjustment_button)
