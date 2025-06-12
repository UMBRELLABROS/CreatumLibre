from pathlib import Path
import tkinter.filedialog
from PIL import ImageTk
from graphics.selection import Selection
from ui.dialogs.color_dialog import ColorAdjustmentDialog

from ui.left_sidebar import LeftSidebar
from ui.ui_menus.zoom import ZoomManager
from ui.ui_structure.notebook_data import ImageNotebook 

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

        # tabs
        self.notebook = ImageNotebook(self.root)
        self.zoom_manager = ZoomManager(self.notebook)
        # left sidebar
        self.sidebar = LeftSidebar(self)

        self.sidebar.grid(column=0, row=0, sticky="ns")
        self.notebook.grid(column=1, row=0, sticky="nsew")

        # Key input bindings
        self.root.bind("<Control-BackSpace>", self.notebook.close_active_tab())
        self.root.bind("<Control-Delete>", self.notebook.close_active_tab())
        self.root.bind("<KeyPress>", self.debug_keypress)

        self.root.bind("<Control-period>", self.zoom_manager.reset_zoom) 
        self.root.bind("<Control-plus>", self.zoom_manager.zoom_in) 
        self.root.bind("<Control-minus>", self.zoom_manager.zoom_out)  
        self.root.bind("<Control-#>", self.zoom_manager.fit_to_frame) 


        if TEST_IMAGE_FILE:
            self.notebook.add_image_tab(TEST_IMAGE_FILE)
            self.sidebar.show_bitmap_mode()

    def load_picture(self):
        filepath = tkinter.filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
        if filepath:
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
        original_path = Path(active_frame.image_data.path)  

        suggested_filename = f"{original_path.stem}_modified{original_path.suffix}"

        file_path = tkinter.filedialog.asksaveasfilename(
            initialdir=original_path.parent,
            initialfile=suggested_filename,
            defaultextension=original_path.suffix,
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if not file_path:
            print("Error: No file selected!")
            return

        file_path = Path(file_path)
        if file_path.suffix == "":
            file_path = file_path.with_suffix(original_path.suffix) 

        img_to_save.save(file_path) 
        print(f"Image saved successfully: {file_path}")


    # sidebar functions
    def open_filter_dialog(self, selection=None):
       pass


    def open_colors_dialog(self, selection=None):
        """Open a dialog to adjust color settings of the active image."""
        active_frame = self.notebook.get_active_frame()  
        if not active_frame:
            print("Error: No active tab found!")
            return

        img = active_frame.image_data.pil  
        selection = selection or Selection(0, 0, img.width, img.height) 
        ColorAdjustmentDialog(self, active_frame, selection) 



    def debug_keypress(self, event):
        print(f"Key: {event.keysym}")
