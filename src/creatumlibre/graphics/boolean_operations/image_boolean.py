# pylint: disable=no-member


import cv2
import numpy as np

from creatumlibre.ui.manager.image_handler import ImageHandler


def merge(
    from_obj: ImageHandler, to_obj: ImageHandler
):  # pylint: disable=too-many-locals
    """Composites the 'from' image into the 'to' image using its mask and position."""
    overlay = from_obj.get_image()
    mask = from_obj.get_mask()
    act_postion = XY.from_tuple(from_obj.get_position())

    base = to_obj.get_image()
    h, w = overlay.shape[:2]
    if h < 1 or w < 1:
        return

    base_h, base_w = base.shape[:2]

    # Begrenzung berechnen
    posTopLeft = act_postion.max_XY(XY(0, 0))
    posRightBottom = posTopLeft.add(XY(w, h)).min_XY(XY(base_w, base_h))

    # Falls komplett außerhalb: abbrechen
    if posTopLeft.x >= posRightBottom.x or posTopLeft.y >= posRightBottom.y:
        return

    # Offset im Overlay berechnen
    overlay_1 = posTopLeft.sub(act_postion)
    overlay_2 = overlay_1.add(posRightBottom.sub(posTopLeft))

    roi = base[posTopLeft.y : posRightBottom.y, posTopLeft.x : posRightBottom.x].astype(
        np.float32
    )
    overlay_crop = overlay[overlay_1.y : overlay_2.y, overlay_1.x : overlay_2.x].astype(
        np.float32
    )

    if mask is not None:
        alpha = mask[overlay_1.y : overlay_2.y, overlay_1.x : overlay_2.x].astype(
            np.float32
        )
        if len(alpha.shape) == 2:
            alpha = cv2.merge([alpha] * 3)
    else:
        alpha = np.ones_like(overlay_crop, dtype=np.float32)

    blended = overlay_crop * alpha + roi * (1 - alpha)
    base[posTopLeft.y : posRightBottom.y, posTopLeft.x : posRightBottom.x] = (
        blended.astype(np.uint8)
    )

    to_obj.set_image(base)


class XY:
    """2D vector class with basic operations."""

    def __init__(self, x: int, y: int | None = None):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, vector: tuple[int, int]) -> "XY":
        return cls(vector[0], vector[1])

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def add(self, other: "XY") -> "XY":
        return XY(self.x + other.x, self.y + other.y)

    def sub(self, other: "XY") -> "XY":
        return XY(self.x - other.x, self.y - other.y)

    def max_XY(self, ref: "XY") -> "XY":
        return XY(max(self.x, ref.x), max(self.y, ref.y))

    def min_XY(self, ref: "XY") -> "XY":
        return XY(min(self.x, ref.x), min(self.y, ref.y))

    def __repr__(self):
        return f"XY(x={self.x}, y={self.y})"
