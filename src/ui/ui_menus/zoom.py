from PIL import ImageTk

class ZoomManager:
    def __init__(self, notebook):
        self.notebook = notebook
        self.zoom_level = 1.0  # ✅ Speichert den aktuellen Zoom-Level!

    def reset_zoom(self,event=None):
        """Setzt den Zoom-Level zurück und aktualisiert die Ansicht."""
        active_frame = self.notebook.get_active_frame()
        if not active_frame:
            return

        self.zoom_level = 1.0  # 🔥 Zurücksetzen auf den ursprünglichen Maßstab!
        original_img = active_frame.image_data.pil.copy()
        active_frame.image_data.tk = ImageTk.PhotoImage(original_img)
        active_frame.canvas.itemconfig(active_frame.image_on_canvas, image=active_frame.image_data.tk)

        active_frame.canvas.config(width=original_img.width, height=original_img.height)
        active_frame.canvas.config(scrollregion=active_frame.canvas.bbox("all"))

    def fit_to_frame(self, event=None):
        """Passt das Bild an die aktuelle Frame-Größe an."""
        active_frame = self.notebook.get_active_frame()
        if not active_frame:
            return

        img = active_frame.image_data.pil
        frame_width, frame_height = active_frame.canvas.winfo_width(), active_frame.canvas.winfo_height()
        
        img_ratio = img.width / img.height
        frame_ratio = frame_width / frame_height

        if img_ratio > frame_ratio:
            new_width, new_height = frame_width, int(frame_width / img_ratio)
        else:
            new_width, new_height = int(frame_height * img_ratio), frame_height

        resized_img = img.resize((new_width, new_height))
        active_frame.image_data.tk = ImageTk.PhotoImage(resized_img)

        active_frame.canvas.itemconfig(active_frame.image_on_canvas, image=active_frame.image_data.tk)
        active_frame.canvas.config(scrollregion=active_frame.canvas.bbox("all"))

    def zoom_in(self, event=None):
        """Vergrößert das aktive Bild um 20%."""
        self.adjust_zoom(1.2)

    def zoom_out(self, event=None):
        """Verkleinert das aktive Bild um 20%."""
        self.adjust_zoom(0.8)

    def adjust_zoom(self, scale_factor):
        """Passt den Zoom-Faktor des aktiven Bildes an."""
        active_frame = self.notebook.get_active_frame()
        if not active_frame:
            return

        original_img = active_frame.image_data.pil
        canvas_bbox = active_frame.canvas.bbox(active_frame.image_on_canvas)
        
        current_width = canvas_bbox[2] - canvas_bbox[0]
        current_height = canvas_bbox[3] - canvas_bbox[1]

        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)

        self.zoom_level *= scale_factor
        self.zoom_level = round(self.zoom_level, 2)

        min_width = max(100, new_width)
        min_height = max(100, new_height)

        resized_img = original_img.resize((min_width, min_height))
        active_frame.image_data.tk = ImageTk.PhotoImage(resized_img)
        active_frame.canvas.itemconfig(active_frame.image_on_canvas, image=active_frame.image_data.tk)
        active_frame.canvas.config(scrollregion=active_frame.canvas.bbox("all"))

        print(f"Aktueller Zoom: {self.zoom_level*100:.0f}% ✅")
