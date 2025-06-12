import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from graphics.picture.color_adjustments import adjust_brightness, adjust_contrast, adjust_saturation
from graphics.selection import Selection
from language.language_handler import lang_handler as lang 


class ColorAdjustmentDialogOLD(tk.Toplevel):
    """Dialog for adjusting color settings such as brightness and contrast."""
    def __init__(self, parent, frame, img, selection):
        super().__init__(parent.root)
        self.parent = parent
        self.frame = frame
        self.img = img.copy()
        self.original_img = img.copy()
        self.selection = selection

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

        # Saturation-Controller
        self.saturation_label = ttk.Label(self, text=lang.get_text("saturation"))
        self.saturation_label.pack(pady=0)
        self.saturation_slider = ttk.Scale(self, from_=0, to=2, orient="horizontal", command=self.update_image)
        self.saturation_slider.set(1) 
        self.saturation_slider.pack(fill="x", expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        #  Apply-Button
        self.apply_button = ttk.Button(button_frame, text=lang.get_text("apply_changes"), command=self.apply_changes)
        self.apply_button.pack(side="left",padx=5)
        #  Cancel-Button
        self.cancel_button = ttk.Button(button_frame, text=lang.get_text("cancel"), command=self.cancel_changes)
        self.cancel_button.pack(side="left",padx=5)

    
    def update_image(self, _):
        """Update the image based on the current slider values."""
        brightness_factor = (self.brightness_slider.get() / 100) + 1
        contrast_factor = (self.contrast_slider.get() / 100) + 1
        saturation_factor = self.saturation_slider.get()


        selection_area = self.original_img.crop(self.selection.to_tuple())
        modified_selection = adjust_brightness(selection_area, brightness_factor)
        modified_selection = adjust_contrast(modified_selection, contrast_factor)
        modified_selection = adjust_saturation(modified_selection, saturation_factor)
        self.img.paste(modified_selection, (self.selection.x, self.selection.y))

        tk_img = ImageTk.PhotoImage(self.img)

        self.frame.image_ref["tk"] = tk_img  
        self.frame.image_ref["pil"] = self.img.copy()
        self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=tk_img)  


    def cancel_changes(self):
        """Restore the original image and close the dialog."""
        if hasattr(self, "original_img"):
            self.img = self.original_img.copy()  
            tk_img = ImageTk.PhotoImage(self.img)

            self.frame.image_ref["tk"] = tk_img  
            self.frame.image_ref["pil"] = self.img.copy() 
            self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=tk_img)  
                      
        self.destroy() 


    def apply_changes(self):
        """Apply the changes to the image and update the canvas."""
        self.frame.image_ref["pil"] = self.img.copy() 
        self.frame.image_ref["tk"] = ImageTk.PhotoImage(self.img)  
        self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=self.frame.image_ref["tk"])
                   
        self.destroy()


class ColorAdjustmentDialog(tk.Toplevel):
    """Dialog zur Anpassung von Helligkeit, Kontrast und Sättigung."""
    def __init__(self, parent, frame, selection):
        super().__init__(parent.root)
        self.parent = parent
        self.frame = frame
        self.image_data = frame.image_data  # 🔥 Direkt auf `ImageData` zugreifen!
        self.img = self.image_data.pil.copy()
        self.original_img = self.img.copy()
        self.selection = selection or Selection(0, 0, self.img.width, self.img.height)  

        self.title(lang.get_text("color_settings"))
        self.geometry("300x450+100+100") 
        self.slider_data = {"brightness": ttk.Scale(self, from_=-100, to=100, orient="horizontal", command=self.update_image),
                        "contrast": ttk.Scale(self, from_=-100, to=100, orient="horizontal", command=self.update_image),
                        "saturation": ttk.Scale(self, from_=0, to=2, orient="horizontal", command=self.update_image)}
        self.sliders=[]
        

        self.create_controls()
    
    def create_controls(self):
        """Erstellt die Steuerelemente für Helligkeit, Kontrast und Sättigung."""

        for i in range(3):
            label_text = ["brightness", "contrast", "saturation"][i]
            label = ttk.Label(self, text=lang.get_text(label_text))
            label.pack(pady=0)
            self.sliders.append( self.slider_data[label_text])
            self.sliders[i].pack(pady=0)
            self.sliders[i].pack(fill="x", expand=True)
            if label_text == "saturation":
                self.sliders[i].set(1)
            

            
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text=lang.get_text("apply_changes"), command=self.apply_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text=lang.get_text("cancel"), command=self.cancel_changes).pack(side="left", padx=5)

    def update_image(self, _):
        """Aktualisiert das Bild basierend auf den aktuellen Schieberegler-Werten."""
        brightness_factor = (self.sliders[0].get() / 100) + 1
        contrast_factor = (self.sliders[1].get() / 100) + 1
        saturation_factor = self.sliders[2].get()

        selection_area = self.original_img.crop(self.selection.to_tuple())
        modified_selection = adjust_brightness(selection_area, brightness_factor)
        modified_selection = adjust_contrast(modified_selection, contrast_factor)
        modified_selection = adjust_saturation(modified_selection, saturation_factor)
        self.img.paste(modified_selection, (self.selection.x, self.selection.y))

        self.update_canvas()

    def update_canvas(self):
        """Aktualisiert das Bild auf dem Canvas."""
        self.image_data.tk = ImageTk.PhotoImage(self.img)
        self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=self.image_data.tk)

    def cancel_changes(self):
        """Setzt das Bild zurück und schließt den Dialog."""
        self.img = self.original_img.copy()
        self.update_canvas()
        self.destroy()

    def apply_changes(self):
        """Speichert die Änderungen in `image_data` und schließt den Dialog."""
        self.image_data.pil = self.img.copy()
        self.update_canvas()
        self.destroy()


 
