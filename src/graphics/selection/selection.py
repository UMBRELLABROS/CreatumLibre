class Selection:
    """Handles selection areas within an image."""

    def __init__(self, x=100, y=100, width=300, height=200):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        """Returns the selection rectangle as a tuple."""
        return (self.x, self.y, self.width, self.height)

    def set_rect(self, x, y, width, height):
        """Update the selection rectangle."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_region(self, image):
        """Extract the selected region from an image."""
        x, y, w, h = self.get_rect()
        return image[y : y + h, x : x + w].copy()  # Encapsulated selection extraction

    def set_region(self, image, modified_region):
        """Place the modified region back into the image."""
        x, y, w, h = self.get_rect()
        image[y : y + h, x : x + w] = modified_region  # Encapsulated region placement

    def contains_point(self, px, py):
        """Check if a point is inside the selection."""
        return (
            self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height
        )
