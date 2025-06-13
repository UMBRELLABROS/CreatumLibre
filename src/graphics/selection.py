from dataclasses import dataclass


@dataclass
class Selection:
    x: int
    y: int
    width: int
    height: int

    def to_tuple(self):
        """Convert the selection to a tuple of coordinates."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
