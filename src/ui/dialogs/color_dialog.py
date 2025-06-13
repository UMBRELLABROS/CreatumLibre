import tkinter as tk
from tkinter import ttk

from PIL import ImageTk

from graphics.picture.color_adjustments import (
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
)
from graphics.selection import Selection
from language.language_handler import lang_handler as lang


class ColorAdjustmentDialog(tk.Toplevel):
    """
    Dialog for adjusting color settings such as
    brightness, contrast, and saturation of an image.
    """

    def __init__(self, parent, frame, selection):
        super().__init__(parent.root)
        self.parent = parent
        self.frame = frame
        self.image_data = frame.image_data
        self.current_tk_size = (
            self.image_data.tk.width(),
            self.image_data.tk.height(),
        )  # avoid rescale
        self.img = self.image_data.pil.copy()
        self.original_img = self.img.copy()
        self.selection = selection or Selection(0, 0, self.img.width, self.img.height)

        self.title(lang.get_text("color_settings"))
        self.geometry("300x450+100+100")
        self.slider_data = {
            "brightness": ttk.Scale(
                self, from_=-100, to=100, orient="horizontal", command=self.update_image
            ),
            "contrast": ttk.Scale(
                self, from_=-100, to=100, orient="horizontal", command=self.update_image
            ),
            "saturation": ttk.Scale(
                self, from_=0, to=2, orient="horizontal", command=self.update_image
            ),
        }
        self.sliders = []

        self.create_controls()

    def create_controls(self):
        """Erstellt die Steuerelemente für Helligkeit, Kontrast und Sättigung."""

        for i in range(3):
            label_text = ["brightness", "contrast", "saturation"][i]
            label = ttk.Label(self, text=lang.get_text(label_text))
            label.pack(pady=0)
            self.sliders.append(self.slider_data[label_text])
            self.sliders[i].pack(pady=0)
            self.sliders[i].pack(fill="x", expand=True)
            if label_text == "saturation":
                self.sliders[i].set(1)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(
            button_frame,
            text=lang.get_text("apply_changes"),
            command=self.apply_changes,
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text=lang.get_text("cancel"), command=self.cancel_changes
        ).pack(side="left", padx=5)

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
        # self.image_data.tk = ImageTk.PhotoImage(self.img)
        # self.frame.canvas.itemconfig(self.frame.image_on_canvas, image=self.image_data.tk)
        self.image_data.tk = ImageTk.PhotoImage(self.img.resize(self.current_tk_size))
        self.frame.canvas.itemconfig(
            self.frame.image_on_canvas, image=self.image_data.tk
        )

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
