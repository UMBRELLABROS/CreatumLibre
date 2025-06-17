# pylint: disable=no-member
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.manager.image_handler import ImageHandler


class ImageManager:
    """Manages image loading, tab creation, and scrolling."""

    def __init__(self, parent):
        self.parent = parent

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        self.tab_widget.setMovable(True)
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.parent.workspace_layout.addWidget(self.tab_widget)

        self.image_container_widget = None
        self.pixmap = None

        self.image_instances = {}  # Track images by tab index

    def load_new_image(self, file_path):
        """Load a new image with scroll support inside a fixed widget."""
        image_instance = ImageHandler(file_path)

        # Scrollable container
        scroll_area_widget = QScrollArea()
        scroll_area_widget.setWidgetResizable(True)
        scroll_area_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        scroll_area_widget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        # Fixed image container inside the scroll area
        self.image_container_widget = QWidget()
        image_container_layout = QVBoxLayout(self.image_container_widget)
        image_label_widget = QLabel()
        image_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load image while keeping aspect ratio
        pixmap = image_instance.get_pixmap()
        image_label_widget.setPixmap(pixmap)

        image_container_layout.addWidget(image_label_widget)
        self.image_container_widget.setLayout(image_container_layout)

        # Place fixed widget inside the scrollable area
        scroll_area_widget.setWidget(self.image_container_widget)

        filename = Path(file_path).name

        tab_index = self.tab_widget.addTab(scroll_area_widget, filename)
        self.image_instances[tab_index] = image_instance

    def get_widget_offset(self):
        """Find the top-left corner of the image widget relative to the application."""
        point = self.image_container_widget.mapTo(
            self.parent, self.image_container_widget.rect().topLeft()
        )
        return point.x(), point.y()

    def get_image_offset(self):
        """Find the padding/margin of the image inside its widget."""
        widget_rect = (
            self.image_container_widget.geometry()
        )  # Get actual size of the widget
        offset_x = 0
        offset_y = 0
        activeImage = self.get_active_image()
        if activeImage:

            image_width, image_height = activeImage.get_zoomed_pixmap_dimension()

            offset_x = (widget_rect.width() - image_width) // 2  # Centering effect
            offset_y = (widget_rect.height() - image_height) // 2

            print(f"Contianer dimension: {widget_rect}")
            print(f"Image dimension: {image_width, image_height}")

        return offset_x, offset_y  # Padding inside the widget

    def update_image_display(self):
        """Update the QLabel with the latest processed image."""
        active_image = self.get_active_image()
        if not active_image:
            print("⚠️ No active image found!")
            return

        zoom_factor = active_image.zoom_factor  # ✅ Ensure zoom_factor is considered
        pixmap = active_image.get_pixmap()

        if zoom_factor != 1.0:  # ✅ Resize only if zoom is applied
            new_width = int(pixmap.width() * zoom_factor)
            new_height = int(pixmap.height() * zoom_factor)
            pixmap = pixmap.scaled(
                new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
            )

        # Find the correct image label inside the active tab
        tab_index = self.tab_widget.currentIndex()
        scroll_area = self.tab_widget.widget(tab_index)
        image_label = scroll_area.findChild(QLabel)

        if image_label:
            image_label.setPixmap(pixmap)
            image_label.repaint()  # Force UI refresh

    def zoom_in(self):
        """Increase the zoom level of the active image."""
        self.apply_zoom(1.2)

    def zoom_out(self):
        """Decrease the zoom level of the active image."""
        self.apply_zoom(0.8)

    def apply_zoom(self, factor):
        """Zoom in or out while maintaining aspect ratio."""
        active_image = self.get_active_image()
        if not active_image:
            print("⚠️ No active image found!")
            return

        active_image.zoom_factor = max(
            0.1, min(3.0, active_image.zoom_factor * factor)
        )  # Prevent extreme zoom

        self.update_image_display()  #  Refresh UI

    def fit_to_container(self):
        """Resize the image while preserving aspect ratio."""
        print("🔍 Fitting image to container with aspect ratio")

        active_image = self.get_active_image()
        if not active_image:
            print("⚠️ No active image found!")
            return

        container_width = self.tab_widget.width()
        container_height = self.tab_widget.height()

        image_width, image_height = (
            active_image.original_image.shape[1],
            active_image.original_image.shape[0],
        )

        # Calculate the best zoom factor
        scale_x = container_width / image_width
        scale_y = container_height / image_height
        active_image.zoom_factor = max(
            scale_x, scale_y
        )  #  Ensures aspect ratio is preserved

        print(
            f" Calculated zoom factor: {active_image.zoom_factor}, {scale_x=}, {scale_y=}"
        )
        # Resize the image
        self.apply_zoom(active_image.zoom_factor)  #  Use zoom logic to resize properly
        self.update_image_display()  #  Refresh UI

    def reset_zoom(self):
        """Reset zoom level for active image."""
        active_image = self.get_active_image()
        if not active_image:
            print("⚠️ No active image found!")
            return

        active_image.processing_image = active_image.original_image.copy()
        active_image.zoom_factor = 1.0

        self.update_image_display()  # Refresh UI

    def get_active_image(self):
        """Retrieve the current image handler."""
        current_index = self.tab_widget.currentIndex()
        print(f"Current tab index: {current_index}")
        if current_index == -1:
            return None

        return self.image_instances.get(current_index, None)
