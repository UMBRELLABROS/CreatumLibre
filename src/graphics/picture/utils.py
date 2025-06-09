from PIL import Image
import io

def convert_to_pillow(photo_img):
    """Converts `PhotoImage` back into `PIL.Image`."""
    try:
        # Convert PhotoImage to a byte stream
        byte_stream = io.BytesIO(photo_img)
        return Image.open(byte_stream)
    except Exception as e:
        print(f"Conversion failed: {e}")
        return None