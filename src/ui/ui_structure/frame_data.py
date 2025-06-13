import tkinter as tk
from tkinter import ttk


class ImageFrame(ttk.Frame):
    def __init__(self, parent, image_data):
        super().__init__(parent)
        self.image_data = image_data

        self.canvas = self.setup_canvas_with_scrollbars()
        self.image_on_canvas = None  # 📌 Wird in `display_image()` gesetzt

        self.display_image()  # 🚀 Jetzt wird das Bild direkt geladen!

    def setup_canvas_with_scrollbars(self):
        """Erstellt das Canvas mit horizontalen und vertikalen Scrollbalken."""
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(canvas_frame)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        return canvas

    def display_image(self):
        """Zeigt das Bild auf dem Canvas und passt die Scrollregion an."""
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor="nw", image=self.image_data.tk
        )
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
