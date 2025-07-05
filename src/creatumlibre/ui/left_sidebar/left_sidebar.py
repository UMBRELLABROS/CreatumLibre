from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QSizePolicy, QToolButton, QVBoxLayout, QWidget

from creatumlibre.ui.dialogs.color_adjustment_dialog import ColorAdjustmentDialog
from creatumlibre.ui.left_sidebar.left_sidebar_css import LEFT_SIDEBAR_SIMPLE_BUTTON
from creatumlibre.ui.mode.ui_input_mode import InputMode

BUTTON_WIDTH = 40
BUTTON_HEIGHT = 40


class LeftSidebar(QWidget):
    """Sidebar with multiple tool buttons."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.color_adjustment_dialog = ColorAdjustmentDialog(
            self, self.parent.tab_manager
        )

        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(20)

        # Create and add tool buttons
        self.btn_color_adjustment = self._create_tool_button(
            "src/creatumlibre/assets/color.png", self.color_adjustment_dialog.show
        )
        self.btn_region = self._create_tool_button(
            "src/creatumlibre/assets/region.png",
            lambda: self.parent.ui_input_mode.set_mode(InputMode.SELECT_REGION),
        )
        self.btn_select_point_cloud = self._create_tool_button(
            "src/creatumlibre/assets/cloud_select.png",
            lambda: self.parent.ui_input_mode.set_mode(InputMode.POINT_CLOUD),
        )

        sidebar_layout.addWidget(self.btn_color_adjustment)
        sidebar_layout.addWidget(self.btn_region)
        sidebar_layout.addWidget(self.btn_select_point_cloud)

        self.setLayout(sidebar_layout)

        # Add buttons to parent's sidebar layout
        for button in [
            self.btn_color_adjustment,
            self.btn_region,
            self.btn_select_point_cloud,
        ]:
            parent.left_sidebar_layout.addWidget(button)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _create_tool_button(self, icon_path, callback):
        """Creates a styled tool button with an icon."""
        button = QToolButton(self)
        button.setIcon(QIcon(QPixmap(icon_path).scaled(BUTTON_WIDTH, BUTTON_HEIGHT)))
        button.setIconSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))
        button.setStyleSheet(LEFT_SIDEBAR_SIMPLE_BUTTON)
        if callback:
            button.clicked.connect(callback)
        return button
