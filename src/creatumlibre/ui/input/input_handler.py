from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QKeySequence

from creatumlibre.ui.dialogs.object_manager_dialog import ObjectManagerDialog
from creatumlibre.ui.manager.image_handler import ImageHandler
from creatumlibre.ui.mode.ui_input_mode import InputMode


class InputHandler(QObject):
    """Handles global key and mouse events."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  #  Reference to UI mode for event interpretation
        self.start_pos = None
        self.end_pos = None
        self.clipboard = None
        self.active_tab = None

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
        self.active_tab = self.parent.tab_manager.get_active_tab()
        if self.active_tab is None:
            return False

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
        mode = self.parent.ui_input_mode.get_mode()
        print(f"General MODE:  {mode}")
        modifiers = event.modifiers()
        if mode == InputMode.SELECT_REGION:
            self.start_pos = self.map_event_to_image_coordinates(event)
            # set the active index by the region clicked

            self.active_tab["manager"].set_selected_object_by_click(
                self.start_pos, modifiers
            )
            print(f"Selection started at {self.start_pos}")

        elif mode in [InputMode.IDLE, InputMode.MOVE_OBJECTS]:  # select objects
            self.start_pos = self.map_event_to_image_coordinates(event)
            if (
                modifiers & Qt.KeyboardModifier.ControlModifier
                or modifiers & Qt.KeyboardModifier.MetaModifier
            ):
                self.active_tab["manager"].set_selected_object_by_click(
                    self.start_pos, modifiers
                )
                self.parent.tab_manager.refresh_active_tab_display()
                print(f"IDLE Object Selection at {self.start_pos}, {mode}")
                self.parent.ui_input_mode.set_mode(InputMode.MOVE_OBJECTS)

        elif mode == InputMode.MOVE_OBJECTS:
            self.start_pos = self.map_event_to_image_coordinates(event)

    def handle_mouse_move(self, event):
        """Handles mouse movement feedback."""
        mode = self.parent.ui_input_mode.get_mode()
        print(f"MOVE MODE: {mode}")
        if mode == InputMode.SELECT_REGION and self.start_pos:
            self.end_pos = self.map_event_to_image_coordinates(event)
            self.parent.update()
            # just to show the rect
            tmp_object = self.create_new_image_object_from_selection()
            self.parent.tab_manager.refresh_active_tab_display()
            self.active_tab["manager"].delete_object(tmp_object)

        elif mode == InputMode.MOVE_OBJECTS and self.start_pos:
            # paint everything
            self.end_pos = self.map_event_to_image_coordinates(event)
            # update pos of dragged objects
            dx = self.end_pos[0] - self.start_pos[0]
            dy = self.end_pos[1] - self.start_pos[1]

            self.active_tab["manager"].update_selected_position(dx, dy)
            self.parent.tab_manager.refresh_active_tab_display()

    def handle_mouse_release(self, event):
        """Handles mouse release actions."""
        mode = self.parent.ui_input_mode.get_mode()
        if mode == InputMode.SELECT_REGION:
            self.end_pos = self.map_event_to_image_coordinates(
                event
            )  # Set final end position
            self.create_new_image_object_from_selection()
            self.parent.ui_input_mode.set_mode(InputMode.IDLE)
            print(f"selection end: {self.end_pos}")
        elif mode == InputMode.MOVE_OBJECTS:
            self.active_tab["manager"].set_new_position()

    def create_new_image_object_from_selection(self) -> ImageHandler:
        """create new image object from selection"""
        x, y, w, h = self.process_rect_selection()  # to base-image
        ## create image (ImageHandler)
        parent_object = self.active_tab["manager"].get_parent()

        # set the selection mask
        parent_object.region_manager.set_bounding_rect(x, y, w, h)

        new_image_object = parent_object.extract_selection_as_new_image()
        self.active_tab["manager"].add_object(
            new_image_object
        )  # new object in ObjectList
        return new_image_object

    def handle_key_press(self, event):
        """Handles key interactions based on mode."""
        print("Key press detected")

        modifiers = event.modifiers().value
        key_seq = QKeySequence(event.key() | modifiers)

        if (
            is_cut := key_seq.matches(QKeySequence.StandardKey.Cut)
            == QKeySequence.SequenceMatch.ExactMatch
        ) or key_seq.matches(
            QKeySequence.StandardKey.Copy
        ) == QKeySequence.SequenceMatch.ExactMatch:

            # copy or cut object without "promoted" flag
            self.clipboard = self.active_tab["manager"].copy_promoted_to_clipboard(
                is_cut
            )
            print(f"Clipboard: {self.clipboard}")
            self.active_tab["manager"].clear_promoted()
            self.parent.tab_manager.refresh_active_tab_display()

        if (
            key_seq.matches(QKeySequence.StandardKey.Paste)
            == QKeySequence.SequenceMatch.ExactMatch
        ):
            if self.clipboard is None:
                return
            self.active_tab["manager"].paste_clipboard(self.clipboard)
            print("Opening Object Manager Dialog (Cmd+V)")

            self.parent.dialog_manager.show(
                ObjectManagerDialog(self.active_tab["manager"])
            )
            self.parent.dialog_manager.update(ObjectManagerDialog)
            mode = self.parent.ui_input_mode.get_mode()
            print(f"mode after CUT OUT {mode}")

            self.parent.tab_manager.refresh_active_tab_display()

    def process_rect_selection(self):
        """Convert QPoint to integers and ensure correct ordering."""
        x1, y1 = self.start_pos[0], self.start_pos[1]
        x2, y2 = self.end_pos[0], self.end_pos[1]

        # Ensure coordinates are ordered correctly
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])
        width, height = x_end - x_start, y_end - y_start
        return x_start, y_start, width, height

    def set_clipboard(self, image_object: ImageHandler):
        """add selection to clopboard"""
        self.clipboard = image_object

    def get_clipboard(self) -> ImageHandler:
        """return image object from clipboard"""
        return self.clipboard
