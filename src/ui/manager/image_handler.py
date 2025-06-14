# pylint: disable=no-member
import cv2  # OpenCV for image processing
from PyQt6.QtGui import QImage, QPixmap


class ImageHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_image = cv2.imread(file_path)  # Load with OpenCV
        self.processing_image = self.original_image.copy()  # Editable version

        self.zoom_factor = 1.0
        self.undo_stack = []  # Stores previous states
        self.redo_stack = []  # Stores undone states

    def get_pixmap(self):
        """Convert OpenCV BGR image to RGB before displaying in QPixmap."""
        rgb_image = cv2.cvtColor(
            self.processing_image, cv2.COLOR_BGR2RGB
        )  # Convert to RGB

        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        qt_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        return QPixmap.fromImage(qt_image)

    def apply_filter(self, filter_function):
        """Apply a modification and save the previous state for undo."""
        self.undo_stack.append(self.processing_image.copy())  # Store last state
        self.processing_image = filter_function(self.processing_image)  # Modify

        # Clear redo stack (new change invalidates redo history)
        self.redo_stack.clear()

    def undo(self):
        """Undo last change if available."""
        if self.undo_stack:
            self.redo_stack.append(self.processing_image.copy())  # Save current state
            self.processing_image = self.undo_stack.pop()

    def redo(self):
        """Redo last undone change if available."""
        if self.redo_stack:
            self.undo_stack.append(self.processing_image.copy())  # Save current state
            self.processing_image = self.redo_stack.pop()
