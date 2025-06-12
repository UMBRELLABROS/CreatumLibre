from tkinter import Image
from PIL import Image, ImageTk

class ImageData:
    """ Class to handle image data for caching in a Tkinter application. """
    def __init__(self, filepath):
        self.filepath = filepath
        self.pil = Image.open(filepath)  # Originalbild laden
        self.tk = ImageTk.PhotoImage(self.pil)  # Tkinter-kompatibles Bild



