# pylint: disable=no-member
import cv2
import numpy as np

from creatumlibre.ui.manager.image_handler import ImageHandler


def merge(from_obj: ImageHandler, to_obj: ImageHandler):
    """Composites the 'from' image into the 'to' image using its mask and position."""
    overlay = from_obj.get_image()
    mask = from_obj.get_mask()
    x, y = from_obj.get_position()

    base = to_obj.get_image()
    h, w = overlay.shape[:2]
    if h < 1 or w < 1:
        return
    roi = base[y : y + h, x : x + w].astype(np.float32)
    overlay = overlay.astype(np.float32)

    if mask is not None:
        alpha = mask.astype(np.float32)
        if len(alpha.shape) == 2:
            alpha = cv2.merge([alpha] * 3)
    else:
        alpha = np.ones_like(overlay, dtype=np.float32)

    blended = overlay * alpha + roi * (1 - alpha)
    base[y : y + h, x : x + w] = blended.astype(np.uint8)

    to_obj.set_image(base)
