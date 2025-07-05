from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QKeySequence

from creatumlibre.graphics.boolean_operations.image_boolean import Vector2D
from creatumlibre.ui.dialogs.object_manager_dialog import ObjectManagerDialog
from creatumlibre.ui.input.intersection_state import InteractionState
from creatumlibre.ui.manager.image_handler import ImageHandler
from creatumlibre.ui.mode.ui_input_mode import InputMode


class InputHandler(QObject):
    """Handles global key and mouse events."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent  #  Reference to UI mode for event interpretation
        self.clipboard = None
        self.active_tab = None
        self.interaction = InteractionState()
        self.point_cloud_points: list[Vector2D] = []
        self.mode = InputMode.IDLE

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
        self.mode = self.parent.ui_input_mode.get_mode()

        self.active_tab = self.parent.tab_manager.get_active_tab()
        if self.active_tab is None:
            return False
        self.parent.tab_manager.tab_widget.setMouseTracking(
            self.mode == InputMode.POINT_CLOUD
        )
        # print(widget.hasMouseTracking())

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
        pos = Vector2D.from_tuple(self.map_event_to_image_coordinates(event))
        clicked_object = self.active_tab["manager"].get_object_at(pos.to_tuple())
        self.interaction.begin(pos, clicked_object)

    def handle_mouse_move(self, event):
        """Handles mouse movement feedback."""

        pos = Vector2D.from_tuple(self.map_event_to_image_coordinates(event))
        print(pos.to_tuple())
        delta = self.interaction.update(pos)

        if self.interaction.drag_started:
            self.active_tab["manager"].update_selected_position(delta)
        else:
            if self.mode in [InputMode.POINT_CLOUD]:
                # trick to just to show the rect
                print("....")
                tmp_object = self.create_new_image_object_from_selection()
                tmp_object.region_manager.set_mask_points(self.point_cloud_points)
                self.parent.tab_manager.refresh_active_tab_display()
                self.active_tab["manager"].delete_object(tmp_object)

            return

        if self.mode == InputMode.SELECT_REGION:
            # trick to just to show the rect
            tmp_object = self.create_new_image_object_from_selection()
            self.parent.tab_manager.refresh_active_tab_display()
            self.active_tab["manager"].delete_object(tmp_object)

        elif self.mode == InputMode.MOVE_OBJECTS:
            self.active_tab["manager"].update_selected_position(delta)
            print(delta.to_tuple())
            # paint everything
            self.parent.tab_manager.refresh_active_tab_display()

    def handle_mouse_release(self, event):
        """Handles mouse release actions."""

        if self.interaction.drag_started:
            self.active_tab["manager"].set_new_position()
        else:
            if self.mode == InputMode.IDLE:
                self.active_tab["manager"].set_selected_object_by_click(
                    self.interaction.start_pos.to_tuple(), event.modifiers()
                )
                self.parent.ui_input_mode.set_mode(InputMode.MOVE_OBJECTS)

        if self.mode == InputMode.SELECT_REGION:
            self.create_new_image_object_from_selection()
            self.parent.ui_input_mode.set_mode(InputMode.IDLE)
        elif self.mode == InputMode.MOVE_OBJECTS:
            self.active_tab["manager"].set_new_position()
        elif self.mode == InputMode.POINT_CLOUD:
            pos = Vector2D.from_tuple(self.map_event_to_image_coordinates(event))

            # Kurve schließen, wenn erster Punkt getroffen
            if (
                self.point_cloud_points
                and (pos - self.point_cloud_points[0]).length() < 5
            ):
                self.finish_point_cloud()
            else:
                self.point_cloud_points.append(pos)

        self.parent.tab_manager.refresh_active_tab_display()
        self.interaction.reset()

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

        elif (
            key_seq.matches(QKeySequence.StandardKey.Paste)
            == QKeySequence.SequenceMatch.ExactMatch
        ):
            if self.clipboard is None:
                return
            self.active_tab["manager"].paste_clipboard(self.clipboard)
            print("Opening Object Manager Dialog (Cmd+V)")

            if ObjectManagerDialog not in self.parent.dialog_manager.dialogs:
                dialog = ObjectManagerDialog(self.active_tab["manager"])
                self.parent.dialog_manager.show(dialog)
            else:
                self.parent.dialog_manager.show(
                    self.parent.dialog_manager.dialogs[ObjectManagerDialog]
                )

            self.parent.dialog_manager.update(ObjectManagerDialog)
            mode = self.parent.ui_input_mode.get_mode()
            print(f"mode after CUT OUT {mode}")

            self.parent.tab_manager.refresh_active_tab_display()

        elif self.mode == InputMode.POINT_CLOUD and event.key() == Qt.Key.Key_Return:
            self.finish_point_cloud()
            self.parent.tab_manager.refresh_active_tab_display()

    def process_rect_selection(self):
        """Convert QPoint to integers and ensure correct ordering."""
        x1, y1 = self.interaction.start_pos.to_tuple()
        x2, y2 = self.interaction.last_pos.to_tuple()
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

    def finish_point_cloud(self):
        if len(self.point_cloud_points) < 3:
            print("Nicht genug Punkte für eine Maske.")
            self.point_cloud_points.clear()
            return

        print(f"Punktwolke abgeschlossen mit {len(self.point_cloud_points)} Punkten")
        for p in self.point_cloud_points:
            print(f"Punkt: {p.to_tuple()}")
        self.point_cloud_points.clear()
        self.parent.ui_input_mode.set_mode(InputMode.IDLE)
        self.parent.tab_manager.refresh_active_tab_display()
