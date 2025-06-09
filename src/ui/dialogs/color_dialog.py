import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from graphics.picture.brightness import adjust_brightness
from graphics.picture.utils import convert_to_pillow
from language.language_handler import lang_handler as lang 


class ColorAdjustmentDialog(tk.Toplevel):
    """Dialog for adjusting color settings such as brightness and contrast."""
    def __init__(self, parent, frame):
        super().__init__(parent.root)
        self.parent = parent
        self.frame = frame  
        self.img = frame.image_ref["pil"].copy()  
        self.original_img = self.img.copy()

        self.title(lang.get_text("color_settings"))
        self.geometry("300x300+100+100")  # Set a reasonable size and position

        # Brightness-Controller
        self.brightness_label = ttk.Label(self, text=lang.get_text("brightness"))
        self.brightness_label.pack(pady=0)
        self.brightness_slider = ttk.Scale(self, from_=-100, to=100, orient="horizontal", command=self.update_image)
        self.brightness_slider.pack(fill="x", expand=True)

        # Contrast-Controller
        self.contrast_label = ttk.Label(self, text=lang.get_text("contrast"))
        self.contrast_label.pack(pady=0)
        self.contrast_slider = ttk.Scale(self, from_=-100, to=100, orient="horizontal", command=self.update_image)
        self.contrast_slider.pack(fill="x", expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        #  Apply-Button
        self.apply_button = ttk.Button(button_frame, text=lang.get_text("apply_changes"), command=self.apply_changes)
        self.apply_button.pack(side="left",padx=5)
        #  Cancel-Button
        self.cancel_button = ttk.Button(button_frame, text=lang.get_text("cancel"), command=self.cancel_changes)
        self.cancel_button.pack(side="left",padx=5)

    
    def update_image(self, _):
        brightness_factor = (self.brightness_slider.get() / 100) + 1
        self.img = adjust_brightness(self.original_img, brightness_factor)

        tk_img = ImageTk.PhotoImage(self.img)
        self.frame.image_ref["tk"] = tk_img  
        self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=tk_img)  


    def cancel_changes(self):
        """Restore the original image and close the dialog."""
        if hasattr(self, "original_img"):
            self.img = self.original_img.copy()  
            tk_img = ImageTk.PhotoImage(self.img)

            # 🎨 Restore image in the frame
            self.frame.image_ref["tk"] = tk_img 
            self.frame.image_ref["pil"] = self.img.copy() 
            self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=tk_img) 

        self.destroy()  # 🔚 Close the dialog


    def apply_changes(self):
        self.frame.image_ref["pil"] = self.img.copy()  
        self.frame.image_ref["tk"] = ImageTk.PhotoImage(self.img)
        self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=self.frame.image_ref["tk"])
        self.destroy() 




 
