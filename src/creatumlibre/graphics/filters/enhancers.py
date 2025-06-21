# pylint: disable = no-member
import cv2
import numpy as np


def adjust_brightness(image, factor):
    """Adjust brightness of the image."""
    image = cv2.convertScaleAbs(
        image, alpha=factor, beta=0
    )  # Proper brightness scaling
    return image


def adjust_saturation(image, factor):
    """Adjust saturation of the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * factor, 0, 255)  # Adjust saturation channel
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def adjust_contrast(image, factor):
    """Adjust contrast of the image."""
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)  # Adjust contrast


def adjust_rgb(image, value, channel):
    """Adjust RGB channels of the image."""
    if channel == "Red":
        image[..., 2] = np.clip(
            image[..., 2] + value * 255, 0, 255
        )  # Adjust Red channel
    elif channel == "Green":
        image[..., 1] = np.clip(
            image[..., 1] + value * 255, 0, 255
        )  # Adjust Green channel
    elif channel == "Blue":
        image[..., 0] = np.clip(
            image[..., 0] + value * 255, 0, 255
        )  # Adjust Blue channel
    return image
