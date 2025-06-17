from PyQt6.QtCore import QEvent, QObject, QTimer

from ui.mode.ui_input_mode import InputMode


class InputHandler(QObject):
    """Handles global key and mouse events."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  #  Reference to UI mode for event interpretation
        self.start_pos = None
        self.end_pos = None
        self.blink_state = True  #  For fluctuating effect
        self.timer = QTimer()  #  Timer for blinking effect
        self.timer.timeout.connect(self.toggle_blink)  #  Toggle state
        self.timer.start(500)

    def eventFilter(self, _, event):
        """Intercept global events and delegate handling."""
        if self.parent.ui_input_mode.get_mode() != InputMode.IDLE:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.handle_mouse_press(event)
            elif event.type() == QEvent.Type.MouseMove:
                self.handle_mouse_move(event)
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.handle_mouse_release(event)
            elif event.type() == QEvent.Type.KeyPress:
                self.handle_key_press(event)
        return False  #  Allows event to propagate if unhandled

    def handle_mouse_press(self, event):
        """Handles mouse press based on current mode."""
        if self.parent.ui_input_mode.get_mode() == InputMode.SELECT_REGION:
            self.start_pos = event.pos()
            print(f"Selection started at {self.start_pos}")

    def handle_mouse_move(self, event):
        """Handles mouse movement feedback."""
        if (
            self.parent.ui_input_mode.get_mode() == InputMode.SELECT_REGION
            and self.start_pos
        ):
            self.end_pos = event.pos()
            self.parent.update()

    def handle_mouse_release(self, event):
        """Handles mouse release actions."""
        if self.parent.ui_input_mode.get_mode() == InputMode.SELECT_REGION:
            self.end_pos = event.pos()  # Set final end position

            activeImage = self.parent.image_manager.get_active_image()
            if activeImage:
                x_start, y_start, width, height = self.process_rect_selection()
                if width > 0 and height > 0:
                    widget_x, widget_y = self.parent.image_manager.get_widget_offset()
                    image_x, image_y = self.parent.image_manager.get_image_offset()
                    print(f"Widget offset: {widget_x, widget_y}")
                    print(f"Image offset: {image_x, image_y}")
                    x, y, w, h = self.get_zoom_corrected_values(
                        x_start - widget_x - image_x,
                        y_start - widget_y - image_y,
                        width,
                        height,
                    )
                    activeImage.set_screen_rect(x, y, w, h)
                else:
                    print("Selection is empty!")
            print(f"Selection completed: {self.start_pos} → {self.end_pos}")

    def get_zoom_corrected_values(self, x, y, width, height):
        activeImage = self.parent.image_manager.get_active_image()
        zoom_factor = activeImage.zoom_factor  # ✅ Get current zoom level
        orig_x_start = int((x) / zoom_factor)
        orig_y_start = int((y) / zoom_factor)
        orig_width = int(width / zoom_factor)
        orig_height = int(height / zoom_factor)
        return orig_x_start, orig_y_start, orig_width, orig_height

    def handle_key_press(self, _):
        """Handles key interactions based on mode."""
        print("Key press detected")

    def process_rect_selection(self):
        """Convert QPoint to integers and ensure correct ordering."""
        x1, y1 = self.start_pos.x(), self.start_pos.y()
        x2, y2 = self.end_pos.x(), self.end_pos.y()

        # Ensure coordinates are ordered correctly
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])
        width, height = x_end - x_start, y_end - y_start
        return x_start, y_start, width, height

    def toggle_blink(self):
        """Fluctuates selection visibility."""
        self.blink_state = not self.blink_state
        self.parent.update()
