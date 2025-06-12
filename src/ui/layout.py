
import tkinter as tk
from graphics.selection import Selection
from ui.dialogs.color_dialog import ColorAdjustmentDialog

from ui.left_sidebar import LeftSidebar
from ui.ui_menus.files import FilesManager
from ui.ui_menus.zoom import ZoomManager
from ui.ui_structure.notebook_data import ImageNotebook 
from language.language_handler import lang_handler as lang  

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

        # tabs & elements
        self.notebook = ImageNotebook(self.root)
        self.zoom_manager = ZoomManager(self.notebook)
        self.sidebar = LeftSidebar(self)
        self.files_manager = FilesManager(self.notebook, self.sidebar)

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

        self.create_menu(self.root)


        if TEST_IMAGE_FILE:
            self.notebook.add_image_tab(TEST_IMAGE_FILE)
            self.sidebar.show_bitmap_mode()


    def create_menu(self, root):
        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label=lang.get_text("new_file"))
        file_menu.add_command(label=lang.get_text("open_file"), command=self.files_manager.load_picture)
        file_menu.add_command(label=lang.get_text("save_file"), command=self.files_manager.save_picture)
        file_menu.add_separator()
        file_menu.add_command(label=lang.get_text("exit_application"), command=root.quit)
        menu.add_cascade(label=lang.get_text("file"), menu=file_menu)

        zoom_menu = tk.Menu(menu, tearoff=0)
        zoom_menu.add_command(label=lang.get_text("zoom_in"), accelerator="Ctrl++", command=self.zoom_manager.zoom_in)
        zoom_menu.add_command(label=lang.get_text("zoom_out"), accelerator="Ctrl+-", command=self.zoom_manager.zoom_out)
        zoom_menu.add_command(label=lang.get_text("reset_zoom"), accelerator="Ctrl+.", command=self.zoom_manager.reset_zoom)
        zoom_menu.add_command(label=lang.get_text("fit_to_frame"), accelerator="Ctrl+#",command=self.zoom_manager.fit_to_frame)
        menu.add_cascade(label=lang.get_text("zoom"), menu=zoom_menu)

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
