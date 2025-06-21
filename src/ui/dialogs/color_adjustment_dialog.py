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
from ui.dialogs.color_adjustment_dialog_css import BTN_APPLY, BTN_CANCEL, MAIN_DIALOG


class ColorAdjustmentDialog(QDialog):
    """Dialog for adjusting brightness, saturation, contrast, and color balance."""

    def __init__(self, parent, tab_manager):
        super().__init__(parent)
        self.tab_manager = tab_manager  # Reference to the tab manager
        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")
        self.sliders = {}
        self.labels = {}
        self.base_image_snapshot = None  # unchanged image

        self._init_layout()

    def _init_layout(self):

        self.setWindowTitle("Color Adjustments")
        self.setFixedSize(300, 480)
        self.setStyleSheet(MAIN_DIALOG)

        button_layout = QHBoxLayout()

        self.apply_button.setStyleSheet(BTN_APPLY)
        self.apply_button.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_button)

        self.cancel_button.setStyleSheet(BTN_CANCEL)
        self.cancel_button.clicked.connect(self.cancel_changes)
        button_layout.addWidget(self.cancel_button)

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

        dialog_layout = QVBoxLayout(self)

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

            dialog_layout.addWidget(label)
            dialog_layout.addWidget(slider)
            self.sliders[adjustment] = slider

        dialog_layout.addLayout(button_layout)  # add buttons
        self.setLayout(dialog_layout)

    def showEvent(self, event):
        """Runs logic when the dialog is shown."""
        super().showEvent(event)

        promoted = self.get_promoted_object()
        if promoted:
            self.base_image_snapshot = promoted.get_image().copy()
            self.apply_all_adjustments()

            return  # Already has a promoted object

        # Promote base image if no selection is active
        active_tab = self.tab_manager.get_active_tab()
        if not active_tab:
            return

        manager = active_tab.get("manager")
        base_object = manager.get_base_object()

        if base_object:
            # Promote full image as fallback
            height, width = base_object.get_image().shape[:2]
            fake_selection = (0, 0, width, height)

            # Make RegionManager believe the full image is selected
            base_object.region_manager.set_bounding_rect(*fake_selection)
            base_object.region_manager.initialize_mask(base_object.get_image().shape)

            new_obj = base_object.extract_selection_as_new_image()
            if new_obj:
                manager.add_object(new_obj)
                self.base_image_snapshot = new_obj.get_image().copy()
                self.apply_all_adjustments()
                self.tab_manager.refresh_tab_display(
                    self.tab_manager.get_active_tab_index()
                )

    def apply_all_adjustments(self):
        promoted = self.get_promoted_object()
        if promoted is None:
            return

        image = self.base_image_snapshot.copy()  # Work on a copy for preview

        for name, config in self.slider_settings.items():
            value = self.sliders[name].value()
            scale = config["scale_function"](value)
            image = config["apply_function"](image, scale)
            mapped_value = config["scale_function"](value)
            self.labels[name].setText(f"{name} [{mapped_value:.2f}]")

        promoted.set_image(image)

        self.tab_manager.refresh_tab_display(self.tab_manager.get_active_tab_index())

    def get_promoted_object(self):
        """Finds the promoted object in the current tab's object manager."""
        active_tab = self.tab_manager.get_active_tab()
        if not active_tab:
            return None

        object_manager = active_tab.get("manager")
        if not object_manager:
            return None

        for obj in object_manager.object_list:
            if getattr(obj, "is_promoted", False):
                return obj
        return None

    def apply_changes_old(self):
        """Apply adjustments permanently to the real image."""
        promoted = self.get_promoted_object()
        if promoted:
            promoted.is_promoted = False
            active_tab = self.tab_manager.get_active_tab()
            object_manager = active_tab.get("manager")
            object_manager.object_list.remove(promoted)
            self.tab_manager.refresh_tab_display(
                self.tab_manager.get_active_tab_index()
            )
            self.accept()

    def apply_changes(self):
        obj_manager = self.tab_manager.get_active_tab().get("manager")
        obj_manager.merge_selection()
        self.tab_manager.refresh_tab_display(self.tab_manager.get_active_tab_index())
        self.accept()

    def cancel_changes(self):
        """Cancel adjustments, delete the promoted layer"""
        promoted = self.get_promoted_object()
        if promoted:
            active_tab = self.tab_manager.get_active_tab()
            object_manager = active_tab.get("manager")
            object_manager.object_list.remove(promoted)
            self.tab_manager.refresh_tab_display(
                self.tab_manager.get_active_tab_index()
            )
            self.reject()
