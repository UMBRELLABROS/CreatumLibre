from PyQt6.QtCore import QEvent, QObject

from creatumlibre.ui.mode.ui_input_mode import InputMode


class InputHandler(QObject):
    """Handles global key and mouse events."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  #  Reference to UI mode for event interpretation
        self.start_pos = None
        self.end_pos = None

    def map_event_to_image_coordinates(self, event) -> tuple[int, int] | None:
        """Get the real position of the mouse within the image QLabel."""
        if (active_tab := self.parent.tab_manager.get_active_tab()) is None:
            return None

        if (label_widget := active_tab.get("widget")) is None:
            return None

        global_pos = event.globalPosition().toPoint()
        local_pos = label_widget.mapFromGlobal(global_pos)

        # Center offset: compensate for QLabel centering the image
        pixmap = label_widget.pixmap()
        if pixmap is None:
            return None

        offset_x = max(0, (label_widget.width() - pixmap.width()) // 2)
        offset_y = max(0, (label_widget.height() - pixmap.height()) // 2)

        real_x = local_pos.x() - offset_x
        real_y = local_pos.y() - offset_y

        # Optional: also return unscaled pixel in original image space
        zoom = active_tab.get("manager").zoom_factor
        orig_x = int(real_x / zoom)
        orig_y = int(real_y / zoom)

        return orig_x, orig_y

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
            self.start_pos = self.map_event_to_image_coordinates(event)
            print(f"Selection started at {self.start_pos}")

    def handle_mouse_move(self, event):
        """Handles mouse movement feedback."""
        if (
            self.parent.ui_input_mode.get_mode() == InputMode.SELECT_REGION
            and self.start_pos
        ):
            self.end_pos = self.map_event_to_image_coordinates(event)
            self.parent.update()

    def handle_mouse_release(self, event):
        """Handles mouse release actions."""
        if self.parent.ui_input_mode.get_mode() == InputMode.SELECT_REGION:
            self.parent.ui_input_mode.set_mode(InputMode.IDLE)
            self.end_pos = self.map_event_to_image_coordinates(
                event
            )  # Set final end position
            x, y, w, h = self.process_rect_selection()  # to base-image

            if (active_tab := self.parent.tab_manager.get_active_tab()) is None:
                return

            ## create image (ImageHandler)
            parent_object = active_tab["manager"].get_active_object()

            # set the selection mask
            parent_object.region_manager.set_bounding_rect(x, y, w, h)

            new_image = parent_object.extract_selection_as_new_image()
            active_tab["manager"].add_object(new_image)  # new object in ObjectList

            print(f"Image selection : {x,y,w,h}")

    def handle_key_press(self, _):
        """Handles key interactions based on mode."""
        print("Key press detected")

    def process_rect_selection(self):
        """Convert QPoint to integers and ensure correct ordering."""
        x1, y1 = self.start_pos[0], self.start_pos[1]
        x2, y2 = self.end_pos[0], self.end_pos[1]

        # Ensure coordinates are ordered correctly
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])
        width, height = x_end - x_start, y_end - y_start
        return x_start, y_start, width, height
