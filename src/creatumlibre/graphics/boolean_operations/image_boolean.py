# pylint: disable=no-member


import cv2
import numpy as np

from creatumlibre.graphics.math.vector2d import Vector2D
from creatumlibre.ui.manager.image_handler import ImageHandler


def merge(
    from_obj: ImageHandler, to_obj: ImageHandler
):  # pylint: disable=too-many-locals
    """Composites the 'from' image into the 'to' image using its mask and position."""
    overlay = from_obj.get_image()
    mask = from_obj.get_mask()
    act_postion = from_obj.get_position()

    base = to_obj.get_image()
    h, w = overlay.shape[:2]
    if h < 1 or w < 1:
        return

    base_h, base_w = base.shape[:2]

    # Begrenzung berechnen
    print(f"--- Act position: {act_postion.to_tuple()}")
    posTopLeft = act_postion.max_vector(Vector2D(0, 0))
    posRightBottom = (act_postion + (Vector2D(w, h))).min_vector(
        Vector2D(base_w, base_h)
    )

    # Falls komplett außerhalb: abbrechen
    if posTopLeft.x >= posRightBottom.x or posTopLeft.y >= posRightBottom.y:
        return

    # Offset im Overlay berechnen
    overlay_1 = posTopLeft - act_postion
    overlay_2 = overlay_1 + (posRightBottom - posTopLeft)

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
