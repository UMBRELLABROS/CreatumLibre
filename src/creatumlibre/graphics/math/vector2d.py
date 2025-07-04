import math


class Vector2D:
    """2D vector class with basic operations."""

    def __init__(self, x: int, y: int | None = None):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, vector: tuple[int, int]) -> "Vector2D":
        return cls(vector[0], vector[1])

    def copy(self) -> "Vector2D":
        return Vector2D(self.x, self.y)

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __abs__(self) -> float:
        return self.length()

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def max_vector(self, ref: "Vector2D") -> "Vector2D":
        return Vector2D(max(self.x, ref.x), max(self.y, ref.y))

    def min_vector(self, ref: "Vector2D") -> "Vector2D":
        return Vector2D(min(self.x, ref.x), min(self.y, ref.y))
