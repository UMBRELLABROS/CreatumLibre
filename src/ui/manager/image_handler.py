# pylint: disable=no-member
import cv2  # OpenCV for image processing
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

from graphics.selection.region_manager import RegionManager
from graphics.selection.selection import Selection


class ImageHandler:
    def __init__(self, file_path):
        self.original_image = cv2.imread(file_path)  # Load with OpenCV
        self.processing_image = self.original_image.copy()  # Editable version
        self.processing_masked_image = (
            self.original_image.copy()
        )  # Editable version with selction edges

        self.selection = Selection()
        self.region_manager = RegionManager()
        self.region_manager.initialize_mask(self.original_image.shape)
        self.region_rect_image = None  #

        self.blink_timer = QTimer()
        # self.blink_timer.timeout.connect(self._toggle_ant_line)
        # self.blink_timer.start(300)  # ✅ Change every 300ms for a smooth effect

        self.undo_stack = []  # Stores previous states
        self.redo_stack = []  # Stores undone states

    def get_selected_region(self):
        """get the rect with the selction boundaries"""
        self.region_rect_image = self.original_image.copy()
        return self.selection.get_region(self.region_rect_image)

    def set_selected_region(self, selected_region):
        self.region_rect_image = self.selection.set_region(
            self.region_rect_image, selected_region
        )  #  Merge changes back
        self.processing_image = self.region_rect_image
        # Generate mask overlay with ant-line effect
        self.processing_masked_image = (
            self.processing_image.copy()
        )  # Start from modified image
        self._draw_ant_lines()

    def _draw_ant_lines(self):
        """Draws a blinking ant-line effect on processing_masked_image."""
        if not self.region_manager.bounding_rect:
            return

        x, y, width, height = self.region_manager.bounding_rect
        interval = 5  # Space between dashes

        # Draw alternating pixels along the border
        for i in range(x, x + width, interval):
            self.processing_masked_image[y, i] = (255, 255, 255)  # Top border
            self.processing_masked_image[y + height - 1, i] = (
                255,
                255,
                255,
            )  # Bottom border

        for j in range(y, y + height, interval):
            self.processing_masked_image[j, x] = (255, 255, 255)  # Left border
            self.processing_masked_image[j, x + width - 1] = (
                255,
                255,
                255,
            )  # Right border

    def _toggle_ant_line(self):
        """Updates the ant-line effect by shifting pixel intensity."""
        self.processing_masked_image = cv2.bitwise_not(
            self.processing_masked_image
        )  # Toggle intensity for blinking effect
        self.image_manager.update_image_display()  # Refresh UI dynamically

    def get_pixmap(self):
        """Convert OpenCV BGR image to RGB before displaying in QPixmap."""
        rgb_image = cv2.cvtColor(
            self.processing_masked_image, cv2.COLOR_BGR2RGB
        )  # Convert to RGB

        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        qt_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        return QPixmap.fromImage(qt_image)

    def get_zoomed_pixmap_dimension(self):
        pixmap = self.get_pixmap()
        return int(pixmap.width() * self.zoom_factor), int(
            pixmap.height() * self.zoom_factor
        )

    def set_screen_rect(self, x, y, width, height):
        """do zoom transformaiton"""
        # do transformation here
        self.selection.set_rect(x, y, width, height)
        self.region_manager.update_mask(self.selection)

    def apply_selection_change(self, new_rect):
        """Modify the selection based on additional areas."""
        # Adjust selection using RegionManager logic
        modified_rect, updated_mask = self.region_manager.modify_selection(
            self.selection, new_rect
        )

        # Store updated selection & mask
        self.selection.set_rect(*modified_rect)
        self.processing_image = self.region_manager.apply_mask(
            self.processing_image, updated_mask
        )
