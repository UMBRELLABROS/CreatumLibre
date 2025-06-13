from tkinter import ttk

from ui.ui_structure.frame_data import ImageFrame
from ui.ui_structure.image_data import ImageData


class ImageNotebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_cache = {}

    def add_image_tab(self, filepath):
        """Adds a new tab with an image to the notebook."""
        image_data = ImageData(filepath)
        frame = ImageFrame(self, image_data)
        tab_title = filepath.name
        self.add(frame, text=tab_title)

        self.image_cache[filepath] = image_data

    def close_active_tab(self):
        """Closes the currently active tab in the notebook."""
        active_tab = self.select()
        if active_tab:
            self.forget(active_tab)

    def get_active_frame(self):
        """Returns the currently active `ImageFrame` in the notebook."""
        active_tab = self.select()
        if not active_tab:
            return None

        for frame in self.winfo_children():
            if str(frame) == active_tab:
                return frame
        return None
