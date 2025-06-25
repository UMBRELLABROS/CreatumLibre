# pylint: disable=no-member

import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap

from creatumlibre.graphics.selection.region_manager import RegionManager
from creatumlibre.ui.mode.ui_input_mode import TransformMode


class ImageHandler:
    """Handles a single image object: pixel data, selection, and position."""

    def __init__(self, image_array: np.ndarray, position=(0, 0), is_promoted=False):
        self.original_image = image_array  # BGR format
        self.position = position  # Absolute position in scene (e.g., top-left)
        self.position_before_drag = position  # reference to add dx,dy while dragging
        self.is_promoted = is_promoted
        self.is_selected = False
        self.region_manager = RegionManager()
        self.region_manager.initialize_mask(self.original_image.shape)

    def copy(self):
        new = ImageHandler(self.original_image.copy())
        new.position = self.position  # Assuming it's immutable (like a tuple)
        new.is_promoted = False
        new.is_selected = False
        new.region_manager = self.region_manager.copy()
        return new

    def get_image(self) -> np.ndarray:
        """Returns the raw image array."""
        return self.original_image

    def contains_point(self, click_position: tuple[int, int]) -> bool:
        """hit test in object coordinates"""
        x, y = click_position
        px, py = self.get_position()
        h, w = self.original_image.shape[:2]
        return px <= x <= px + w and py <= y <= py + h

    def get_pixmap(self) -> QPixmap:
        """Converts the image array (BGR) to a QPixmap for UI display."""
        image = self.get_image()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width

        q_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )
        return QPixmap.fromImage(q_image)

    def set_image(self, image):
        self.original_image = image

    def set_position(self, position: tuple):
        """set global position"""
        self.position = position

    def get_position(self) -> tuple:
        """Returns the (x, y) position in global scene space."""
        return self.position

    def get_mask(self) -> np.ndarray:
        """Returns the current alpha mask (0-255)."""
        return self.region_manager.mask

    def extract_selection_as_new_image(self) -> "ImageHandler | None":
        """Extracts the currently selected region as a new ImageHandler instance."""
        selection_mask = self.region_manager.get_mask()
        if selection_mask is None:
            return None

        x, y, w, h = self.region_manager.get_bounding_rect()

        # Clip region safely from image
        selected_region = self.original_image[y : y + h, x : x + w].copy()

        # Optional: clip selection mask too
        # cropped_mask = selection_mask[y:y+h, x:x+w].copy()

        new_object = ImageHandler(
            image_array=selected_region, position=(x, y), is_promoted=True
        )

        return new_object

    def draw_selection_frame(
        self, transform_mode: TransformMode, zoom_factor: float = 1.0
    ):
        """Draws a selection frame with optional handles on this image."""
        img = self.original_image
        h, w = img.shape[:2]
        if h < 4 or w < 4:
            return
        color = (255, 0, 255)  # magenta
        thickness = int(1 / zoom_factor)

        # Draw border
        cv2.rectangle(img, (0, 0), (w - 1, h - 1), color, thickness)
        print(transform_mode)

        # Add 9-resize handles, rotate pivot, etc.
        # For example, draw corner point:
        # cv2.circle(img, (0, 0), radius=4, color=color, thickness=-1)
