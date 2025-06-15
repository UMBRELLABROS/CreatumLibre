from PyQt6.QtWidgets import QDialog, QLabel, QSlider, QVBoxLayout


class ColorAdjustmentDialog(QDialog):
    """Dialog for adjusting brightness, saturation, contrast, and color balance."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Color Adjustments")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        # ✅ Define adjustment sliders
        self.sliders = {}

        adjustments = ["Brightness", "Contrast", "Saturation", "Red", "Green", "Blue"]
        for adjustment in adjustments:
            label = QLabel(adjustment)
            slider = QSlider()
            slider.setRange(-100, 100)  # Set limits
            slider.valueChanged.connect(
                lambda _, adj=adjustment: self.update_image(adj)
            )  # ✅ Apply update
            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders[adjustment] = slider

    def update_image(self, adjustment_type):
        """Apply the selected adjustment to the image."""
        value = self.sliders[adjustment_type].value()
        print(f"Updating {adjustment_type} with value: {value}")  #  Debugging info
