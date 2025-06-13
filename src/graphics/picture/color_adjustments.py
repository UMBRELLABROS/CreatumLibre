from PIL import ImageEnhance


def adjust_brightness(img, brightness_factor):
    """Adjust the brightness of an image."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(brightness_factor)


def adjust_contrast(img, contrast_factor):
    """Adjust the contrast of an image."""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(contrast_factor)


def adjust_saturation(img, saturation_factor):
    """Adjust the saturation of an image."""
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(saturation_factor)
