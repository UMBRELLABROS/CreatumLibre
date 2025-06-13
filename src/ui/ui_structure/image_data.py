from PIL import Image, ImageTk


class ImageData:  # pylint: disable=too-few-public-methods
    """Class to handle image data for caching in a Tkinter application."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.pil = Image.open(filepath)  # Original PIL image object
        self.tk = ImageTk.PhotoImage(self.pil)  # Tkinter- compatible image object
