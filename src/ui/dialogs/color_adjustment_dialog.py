from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from graphics.filters.enhancers import (
    adjust_brightness,
    adjust_contrast,
    adjust_rgb,
    adjust_saturation,
)


class ColorAdjustmentDialog(QDialog):
    """Dialog for adjusting brightness, saturation, contrast, and color balance."""

    def __init__(self, parent, image_manager):
        super().__init__(parent)
        self.image_manager = image_manager  # Reference to the image manager

        self.setWindowTitle("Color Adjustments")
        self.setFixedSize(300, 480)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #222831;  /* Dark background */
                color: white;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                color: #EEEEEE; /* Soft contrast */
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #393E46; /* Groove color */
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #00ADB5; /* Handle color */
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """
        )

        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet(
            """
            QPushButton {
                background-color: #00ADB5;
                color: white;
                border-radius: 5px;
                height: 30px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #007F8F;
            }
        """
        )
        self.apply_button.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_button)

        # Cancel Button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #F05454;
                color: white;
                border-radius: 5px;
                height: 30px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #D43C3C;
            }
        """
        )
        self.cancel_button.clicked.connect(self.cancel_changes)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)

        self.sliders = {}
        self.labels = {}
        self.slider_settings = {
            "Brightness": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: 1 + (value / 100 * 1),
                "apply_function": adjust_brightness,
            },
            "Saturation": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: 1 + (value / 100 * 2),
                "apply_function": adjust_saturation,
            },
            "Contrast": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: 1 + (value / 100 * 1.0),
                "apply_function": adjust_contrast,
            },
            "Red": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: value / 100,
                "apply_function": lambda img, value: adjust_rgb(img, value, "Red"),
            },
            "Green": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: value / 100,
                "apply_function": lambda img, value: adjust_rgb(img, value, "Green"),
            },
            "Blue": {
                "default": 0,
                "range": (-100, 100),
                "tick_interval": 10,
                "scale_function": lambda value: value / 100,
                "apply_function": lambda img, value: adjust_rgb(img, value, "Blue"),
            },
        }

        for adjustment, config in self.slider_settings.items():
            label = QLabel(
                adjustment
            )  #  This will be replaced with translation support later
            self.labels[adjustment] = label
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(config["tick_interval"])
            slider.setRange(*config["range"])  #  Uses dict values
            slider.setValue(config["default"])
            self.labels[adjustment].setText(f"{adjustment} [{slider.value():.2f}]")

            slider.valueChanged.connect(self.apply_all_adjustments)

            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders[adjustment] = slider

        layout.addLayout(button_layout)  # add buttons
        self.setLayout(layout)
        self.apply_all_adjustments()

    def apply_all_adjustments(self):
        """Applies enhancements directly to the selection area or full image."""
        if (active_image := self.image_manager.get_active_image()) is None:
            return

        selected_region = active_image.get_selected_region()

        for adjustment, config in self.slider_settings.items():
            raw_value = self.sliders[adjustment].value()
            mapped_value = config["scale_function"](raw_value)
            self.labels[adjustment].setText(f"{adjustment} [{mapped_value:.2f}]")
            selected_region = config["apply_function"](
                selected_region, mapped_value
            )  #  Modify selection

        active_image.set_selected_region(selected_region)

        self.image_manager.update_image_display()  # zoom and stuff

    def apply_changes(self):
        """Apply adjustments permanently to the real image."""
        active_image = self.image_manager.get_active_image()
        if active_image:
            active_image.original_image = (
                active_image.processing_image.copy()
            )  # Save modifications

    def cancel_changes(self):
        """Restore the original image before edits."""
        active_image = self.image_manager.get_active_image()
        if active_image:
            active_image.processing_image = (
                active_image.original_image.copy()
            )  # ✅ Undo changes
            self.image_manager.update_image_display()  # ✅ Refresh UI
