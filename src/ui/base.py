from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLayout,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.manager.image_manager import ImageManager
from ui.menu.files import FileMenu
from ui.menu.zoom import ZoomMenu


class CreatumLibre(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_opened_folder = str(Path.home())

        self.setWindowTitle("CreatumLibre")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1200, 800)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.resize(1200, 800)

        self.menu_bar = self.menuBar()
        self.main_layout = QVBoxLayout()

        # Create Tab Widget
        self.image_manager = ImageManager(self)

        FileMenu(self)  # Initialize File Menu
        ZoomMenu(self)  # Initialize Zoom Menu

        self.init_layout()

    def init_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ✅ Ensure the main layout is fully expandable
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        central_widget.setLayout(self.main_layout)

        # Top Layout (~90% of height)
        top_layout = QHBoxLayout()
        left_sidebar = QWidget()
        right_sidebar = QWidget()

        left_sidebar.setFixedWidth(80)
        left_sidebar.setStyleSheet(
            "background-color: #f0fff0;"
        )  # Placeholder for left sidebar
        right_sidebar.setFixedWidth(80)
        right_sidebar.setStyleSheet(
            "background-color: #f0f0ff;"
        )  # Placeholder for colors

        top_layout.addWidget(left_sidebar, stretch=1)
        top_layout.addWidget(
            self.image_manager.tab_widget, stretch=9
        )  # ✅ Ensure full expansion
        top_layout.addWidget(right_sidebar, stretch=1)

        # ✅ Force the tab widget itself to be expandable
        self.image_manager.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Bottom Layout (~10% of height)
        bottom_info_bar = QWidget()
        bottom_info_bar.setFixedHeight(80)
        bottom_info_bar.setStyleSheet("background-color: #fff0f0;")

        self.main_layout.addLayout(top_layout, stretch=9)
        self.main_layout.addWidget(bottom_info_bar, stretch=1)

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
        print(f"Main Layout Height: {self.main_layout.geometry().height()}")
        print(f"Tab Widget Height: {self.image_manager.tab_widget.height()}")
