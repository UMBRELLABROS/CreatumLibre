import tkinter.filedialog
from pathlib import Path


class FilesManager:
    """Handles file operations such as loading and saving images in the application."""

    def __init__(self, notebook, sidebar):
        self.notebook = notebook
        self.sidebar = sidebar

    def load_picture(self):
        """Open a file dialog to select an image file and add it to the notebook."""
        filepath = tkinter.filedialog.askopenfilename(
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("Bitmap files", "*.bmp"),
                ("GIF files", "*.gif"),
                ("SVG files", "*.svg"),
            ]
        )

        if not filepath:
            print("Error: No file selected!")
            return

        self.notebook.add_image_tab(filepath)

        if filepath.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            self.sidebar.show_bitmap_mode()
        elif filepath.lower().endswith(".svg"):
            self.sidebar.show_vector_mode()

    def save_picture(self):
        """Saves the currently active image to a file."""
        active_frame = self.notebook.get_active_frame()
        if not active_frame:
            print("Error: No active image found!")
            return

        img_to_save = active_frame.image_data.pil
        original_path = Path(active_frame.image_data.filepath)

        suggested_filename = f"{original_path.stem}_modified{original_path.suffix}"

        file_path = tkinter.filedialog.asksaveasfilename(
            initialdir=original_path.parent,
            initialfile=suggested_filename,
            defaultextension=original_path.suffix,
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            print("Error: No file selected!")
            return

        file_path = Path(file_path)
        if file_path.suffix == "":
            file_path = file_path.with_suffix(original_path.suffix)

        img_to_save.save(file_path)
        print(f"Image saved successfully: {file_path}")
