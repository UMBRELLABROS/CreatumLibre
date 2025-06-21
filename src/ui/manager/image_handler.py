import numpy as np

from graphics.selection.region_manager import RegionManager


class ImageHandler:
    """Handles a single image object: pixel data, selection, and position."""

    def __init__(self, image_array: np.ndarray, position=(0, 0), is_promoted=False):
        self.original_image = image_array  # BGR format
        self.position = position  # Absolute position in scene (e.g., top-left)
        self.is_promoted = is_promoted
        self.region_manager = RegionManager()
        self.region_manager.initialize_mask(self.original_image.shape)

    def copy(self):
        new = ImageHandler(self.original_image.copy())
        new.position = self.position  # Assuming it's immutable (like a tuple)
        new.is_promoted = self.is_promoted
        new.region_manager = self.region_manager.copy()
        return new

    def get_image(self) -> np.ndarray:
        """Returns the raw image array."""
        return self.original_image

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
