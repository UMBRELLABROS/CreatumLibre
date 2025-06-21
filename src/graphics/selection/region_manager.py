import numpy as np


class RegionManager:
    """Handles selection modifications, mask updates, and dynamic resizing."""

    def __init__(self):
        self.mask = None  # Stores selection mask (0-255)
        self.bounding_rect = None  # Stores current selection bounds

    def copy(self):
        new = RegionManager()
        new.mask = self.mask.copy()
        new.bounding_rect = self.bounding_rect
        return new

    def set_bounding_rect(self, x: int, y: int, width: int, height: int):
        self.bounding_rect = (x, y, width, height)

    def get_bounding_rect(self):
        return self.bounding_rect

    def get_mask(self):
        return self.mask

    def initialize_mask(self, image_shape):
        """Creates an empty mask matching the image dimensions.
        0: transparent, 1: opaque (visible)
        """
        self.mask = np.ones((image_shape[0], image_shape[1]), dtype=np.float32)

    def update_mask(self, selection):
        """Updates the mask based on selection coordinates."""
        x, y, width, height = selection.get_rect()
        self.mask[y : y + height, x : x + width] = (
            1  # Mark selection area as fully opaque
        )

        # Update bounding rect
        self.bounding_rect = (x, y, width, height)

    def apply_mask(self, image, mask):
        """Applies the mask onto the image, modifying selection visibility."""
        masked_image = image.copy()
        masked_image[mask == 0] = (0, 0, 0)  # Hide unselected regions

        return masked_image
