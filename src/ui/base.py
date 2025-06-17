from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLayout,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.input.input_handler import InputHandler
from ui.left_sidebar.left_sidebar import LeftSidebar
from ui.manager.image_manager import ImageManager
from ui.menu.files import FileMenu
from ui.menu.zoom import ZoomMenu
from ui.mode.ui_input_mode import UiMode


class CreatumLibre(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_opened_folder = str(Path.home())

        self.setWindowTitle("CreatumLibre")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1200, 800)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.resize(1200, 800)

        self.ui_input_mode = UiMode("Base")
        self.input_handler = InputHandler(self)
        self.installEventFilter(self.input_handler)

        self.menu_bar = self.menuBar()
        self.workspace_layout = QVBoxLayout()
        self.left_sidebar_layout = None

        # Create Tab Widget
        self.image_manager = ImageManager(self)

        self.init_layout()

        self.file_menu = FileMenu(self)  # Initialize File Menu
        self.zoom_menu = ZoomMenu(self)  # Initialize Zoom Menu

        # debug
        test_file_path = (
            Path("/Users/martinstottmeister/Library")
            / "CloudStorage"
            / "OneDrive-Personal"
            / "Bilder"
            / "Screenshots"
            / "Screenshot_20221225_162528.png"
        )

        # debug
        self.image_manager.load_new_image(test_file_path)

        activeImage = self.image_manager.get_active_image()
        activeImage.set_screen_rect(300, 300, 400, 500)

    def init_layout(self):
        workspace_widget = QWidget()
        self.setCentralWidget(workspace_widget)

        # Ensure the main layout is fully expandable
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(0)
        self.workspace_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        workspace_widget.setLayout(self.workspace_layout)

        # Top Layout (~90% of height)
        editor_panel_layout = QHBoxLayout()
        right_sidebar_widget = QWidget()

        left_sidebar_widget = QWidget()
        left_sidebar_widget.setFixedWidth(40)
        left_sidebar_widget.setStyleSheet(
            "background-color: #f0fff0;"
        )  # Placeholder for left sidebar
        self.left_sidebar_layout = QVBoxLayout(left_sidebar_widget)
        self.left_sidebar_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove sidebar padding
        self.left_sidebar_layout.setSpacing(0)  # Remove extra spacing
        self.left_sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        right_sidebar_widget.setFixedWidth(40)
        right_sidebar_widget.setStyleSheet(
            "background-color: #f0f0ff;"
        )  # Placeholder for colors

        editor_panel_layout.addWidget(left_sidebar_widget, stretch=1)
        editor_panel_layout.addWidget(self.image_manager.tab_widget, stretch=9)
        editor_panel_layout.addWidget(right_sidebar_widget, stretch=1)

        # Force the tab widget itself to be expandable
        self.image_manager.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Bottom Layout (~10% of height)
        status_bar_widget = QWidget()
        status_bar_widget.setFixedHeight(80)
        status_bar_widget.setStyleSheet("background-color: #fff0f0;")

        self.workspace_layout.addLayout(editor_panel_layout, stretch=9)
        self.workspace_layout.addWidget(status_bar_widget, stretch=1)

        LeftSidebar(self)

        self.debug_sizes()

    def load_new_image_dialog(self):
        """Open a file dialog to load a new image and let ImageManager handle the rest."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", self.last_opened_folder, "Images (*.png *.jpg *.bmp)"
        )

        if file_path:
            self.last_opened_folder = str(Path(file_path).parent)
            self.image_manager.load_new_image(file_path)

    def debug_sizes(self):
        print(f"Main Window Height: {self.height()}")
        print(f"Central Widget Height: {self.centralWidget().height()}")
        print(f"Main Layout Height: {self.workspace_layout.geometry()}")
        print(f"Tab Widget Geometry: {self.image_manager.tab_widget.geometry()}")
