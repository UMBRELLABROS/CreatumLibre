from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from PIL import Image, ImageTk
from ui.dialogs.color_dialog import ColorAdjustmentDialog
from ui.left_sidebar import LeftSidebar 

TEST_IMAGE_FILE = '/Users/martinstottmeister/Library/CloudStorage/OneDrive-Personal/Bilder/Eigene Aufnahmen/860.jpg'

class CreatumLibreApp:
    """Main application class for CreatumLibre, handling the main window and tabs."""
    def __init__(self, root):
        self.root = root
        self.root.title("CreatumLibre")
        self.root.geometry("1200x800+100+50") # start with a reasonable size and position
        self.root.minsize(800, 600)  # set a minimum size for the window

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # left sidebar
        self.sidebar = LeftSidebar(self)
        self.sidebar.grid(column=0, row=0, sticky="ns")

        # tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(column=1, row=0, sticky="nsew")

        self.image_cache = {}

        # Key input bindings
        self.root.bind("<BackSpace>", self.close_active_tab)
        self.root.bind("<Delete>", self.close_active_tab)
        self.root.bind("<KeyPress>", self.debug_keypress)

        if TEST_IMAGE_FILE:
            self.add_image_tab(TEST_IMAGE_FILE)
            self.sidebar.show_bitmap_mode()

    def load_picture(self):
        filepath = tkinter.filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
        if filepath:
            self.add_image_tab(filepath)
            if filepath.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                self.sidebar.show_bitmap_mode()
            elif filepath.lower().endswith(".svg"):
                self.sidebar.show_vector_mode()




    def save_picture(self):
        """Save the active image with correct extension handling."""
        img_to_save = self.get_active_image()

        if img_to_save is None:
            print("Error: No active image found!")
            return

        # Get the original file path from the active tab
        active_tab = self.notebook.select()
        if not active_tab:
            print("Error: No active tab found!")
            return

        for frame in self.notebook.winfo_children():
            if str(frame) == active_tab:
                original_path = Path(frame.image_ref["path"])  
                break
        else:
            print("Error: No image path found in active tab!")
            return

        # 🔍 Extract filename & extension dynamically
        suggested_filename = original_path.stem + "_modified" + original_path.suffix

        # Open save dialog with suggested filename
        file_path = tkinter.filedialog.asksaveasfilename(
            initialdir=original_path.parent,  # Suggest saving in the same folder
            initialfile=suggested_filename,  # Use modified name
            defaultextension=original_path.suffix,  # Keep original extension
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        # Ensure the extension is present
        file_path = Path(file_path)
        if file_path.suffix == "":
            file_path = file_path.with_suffix(original_path.suffix)  # Force correct extension

        if file_path:
            img_to_save.save(file_path)  # 💾 Save image
            print(f"Image saved successfully: {file_path}")




    def add_image_tab(self, filepath):
        frame = ttk.Frame(self.notebook)
        tab_title = filepath.split("/")[-1]
        self.notebook.add(frame, text=tab_title)

        if filepath not in self.image_cache:
            img = Image.open(filepath)
            img.thumbnail((800, 600))
            self.image_cache[filepath] = {
                "pil": img,  # Store PIL image
                "tk": ImageTk.PhotoImage(img),  # Store PhotoImage
                "path": filepath
            }

        # Create and store the canvas inside the frame
        frame.canvas = tk.Canvas(frame, width=800, height=600)
        frame.canvas.pack()
        frame.image_on_canvas = frame.canvas.create_image(0, 0, anchor="nw", image=self.image_cache[filepath]["tk"])

        frame.image_ref = self.image_cache[filepath]  # Store both images inside the frame


    def close_active_tab(self, _):
        active_tab = self.notebook.select()
        if active_tab:
            self.notebook.forget(active_tab)

    def get_active_image(self):
        active_tab = self.notebook.select()
        if not active_tab:
            return None  

        for frame in self.notebook.winfo_children():
            if str(frame) == active_tab:
                return frame.image_ref["pil"]  
        return None


    # sidebar functions
    def apply_filter(self):
        print("Applying filter...")

    def adjust_colors(self):
        print("Adjusting colors...")
        active_tab = self.notebook.select()
        if not active_tab:
            print("Error: No active tab found!")
            return

        for frame in self.notebook.winfo_children():
            if str(frame) == active_tab:
                ColorAdjustmentDialog(self, frame) 
                break


    def debug_keypress(self, event):
        print(f"Key: {event.keysym}")
