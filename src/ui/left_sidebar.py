import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from language.language_handler import lang_handler as lang  


ASSETS_PATH = Path(__file__).parent.parent.parent / "assets"
SIDEBAR_WIDTH = 40

def load_icon(file, size=(SIDEBAR_WIDTH, SIDEBAR_WIDTH)):
    img = Image.open(file)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

class LeftSidebar(tk.Frame):
    """Sidebar for the CreatumLibre application, containing tools and menu options."""
    def __init__(self, parent):
        super().__init__(parent.root, width=SIDEBAR_WIDTH, bg="lightgray")
        self.parent = parent
        self.pack(side="left", fill="y")

        self.vector_tools = tk.Frame(self, bg="lightgray")
        self.bitmap_tools = tk.Frame(self, bg="lightgray")

        
        self.create_vector_ui()
        self.create_bitmap_ui()


    def create_vector_ui(self):
        pass  

    def create_bitmap_ui(self):
        filter_icon = load_icon(ASSETS_PATH / "icons" / "filter.png")
        color_icon = load_icon(ASSETS_PATH / "icons" / "colors.png")

        tk.Label(self.bitmap_tools, text="").pack()
        tk.Button(self.bitmap_tools, image=filter_icon, command=self.parent.open_filter_dialog).pack()
        tk.Button(self.bitmap_tools, image=color_icon, command=self.parent.open_colors_dialog).pack()

        # Set the image references to prevent garbage collection
        self.bitmap_tools.image_filter = filter_icon
        self.bitmap_tools.image_color = color_icon

    def show_vector_mode(self):
        self.bitmap_tools.pack_forget()
        self.vector_tools.pack(fill="y")

    def show_bitmap_mode(self):
        self.vector_tools.pack_forget()
        self.bitmap_tools.pack(fill="y")
