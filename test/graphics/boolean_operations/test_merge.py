import numpy as np

from creatumlibre.graphics.boolean_operations.image_boolean import merge
from creatumlibre.graphics.math.vector2d import Vector2D
from creatumlibre.ui.manager.image_handler import ImageHandler


def test_merge_with_negative_position():
    # Zielbild (base): 100x100, weiß
    base_image = np.full((100, 100, 3), 255, dtype=np.uint8)
    base_handler = ImageHandler(base_image.copy(), Vector2D(0, 0))

    # Overlay: 20x20, rot
    overlay_image = np.zeros((20, 20, 3), dtype=np.uint8)
    overlay_image[:, :] = [0, 0, 255]  # Rot
    overlay_handler = ImageHandler(overlay_image, Vector2D(-10, 90))

    # Merge aufrufen
    merge(overlay_handler, base_handler)

    # Ergebnisbild holen
    result = base_handler.get_image()

    # Erwartung: Nur der rechte Teil des Overlays (10x10) wurde unten links eingefügt
    inserted_region = result[90:100, 0:10]
    assert np.all(inserted_region[:, :, 2] == 255)  # Roter Kanal
    assert np.all(inserted_region[:, :, 0:2] == 0)  # Blau & Grün = 0

    # Rest des Bildes bleibt weiß
    untouched_region = result[0:80, 0:100]
    assert np.all(untouched_region == 255)
