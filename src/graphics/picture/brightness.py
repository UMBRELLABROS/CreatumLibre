from PIL import ImageEnhance

def adjust_brightness(img, brightness_factor):
    """Adjust the brightness of an image."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(brightness_factor)