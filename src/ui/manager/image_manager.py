from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QScrollArea, QTabWidget, QVBoxLayout, QWidget

from ui.manager.image_handler import ImageHandler


class ImageManager:
    """Manages image loading, tab creation, and scrolling."""

    def __init__(self, parent):
        self.parent = parent
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab())
        self.tab_widget.setMovable(True)
        self.parent.main_layout.addWidget(self.tab_widget)

        self.image_instances = {}  # Track images by tab index

    def load_new_image(self, file_path):
        """Load a new image with scroll support inside a fixed widget."""
        image_instance = ImageHandler(file_path)

        # Scrollable container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Fixed image container inside the scroll area
        image_container = QWidget()
        layout = QVBoxLayout(image_container)
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load image while keeping aspect ratio
        pixmap = image_instance.get_pixmap()
        image_label.setPixmap(pixmap)

        layout.addWidget(image_label)
        image_container.setLayout(layout)

        # Place fixed widget inside the scrollable area
        scroll_area.setWidget(image_container)

        filename = Path(file_path).name

        tab_index = self.tab_widget.addTab(scroll_area, filename)
        self.image_instances[tab_index] = image_instance

    def get_active_image(self):
        """Retrieve the current image handler."""
        current_index = self.tab_widget.currentIndex()
        return self.image_instances.get(current_index, None)
