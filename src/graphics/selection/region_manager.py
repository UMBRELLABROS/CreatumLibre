import numpy as np


class RegionManager:
    """Handles selection modifications, mask updates, and dynamic resizing."""

    def __init__(self):
        self.mask = None  # Stores selection mask (0-255)
        self.bounding_rect = None  # Stores current selection bounds

    def initialize_mask(self, image_shape):
        """Creates an empty mask matching the image dimensions."""
        self.mask = np.zeros((image_shape[0], image_shape[1]), dtype=np.uint8)

    def update_mask(self, selection):
        """Updates the mask based on selection coordinates."""
        x, y, width, height = selection.get_rect()
        self.mask[y : y + height, x : x + width] = (
            255  # Mark selection area as fully opaque
        )

        # Update bounding rect
        self.bounding_rect = (x, y, width, height)

    def modify_selection(self, selection, new_rect):  # pylint: disable=too-many-locals
        """Expands or modifies selection based on additional areas."""
        x, y, width, height = selection.get_rect()
        new_x, new_y, new_width, new_height = new_rect

        # Merge new selection area into existing mask
        self.mask[new_y : new_y + new_height, new_x : new_x + new_width] = 255

        # Calculate expanded bounding rect
        min_x = min(x, new_x)
        min_y = min(y, new_y)
        max_x = max(x + width, new_x + new_width)
        max_y = max(y + height, new_y + new_height)

        updated_rect = (min_x, min_y, max_x - min_x, max_y - min_y)  # New bounding box

        return updated_rect, self.mask  # Return updated selection rectangle & mask

    def apply_mask(self, image, mask):
        """Applies the mask onto the image, modifying selection visibility."""
        masked_image = image.copy()
        masked_image[mask == 0] = (0, 0, 0)  # Hide unselected regions

        return masked_image
