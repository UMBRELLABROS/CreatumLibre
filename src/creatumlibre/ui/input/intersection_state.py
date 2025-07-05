from creatumlibre.graphics.boolean_operations.image_boolean import Vector2D
from creatumlibre.ui.manager.image_handler import ImageHandler


class InteractionState:
    """Tracks the state of a mouse interaction (click, drag, release)."""

    def __init__(self):
        self.start_pos: Vector2D | None = None
        self.last_pos: Vector2D | None = None
        self.drag_started: bool = False
        self.clicked_object: ImageHandler | None = None
        self.drag_threshold: int = 2

    def begin(self, pos: Vector2D, clicked_object: ImageHandler | None):
        self.start_pos = pos
        self.last_pos = pos
        self.drag_started = False
        self.clicked_object = clicked_object

    def update_old(self, current_pos: Vector2D) -> Vector2D:
        if not self.last_pos:
            return Vector2D(0, 0)

        delta = current_pos - self.last_pos
        if abs(delta.x) > self.drag_threshold or abs(delta.y) > self.drag_threshold:
            self.drag_started = True
        self.last_pos = current_pos
        return delta

    def update(self, current_pos: Vector2D) -> Vector2D:
        if not self.start_pos:
            return Vector2D(0, 0)

        delta = current_pos - self.start_pos
        if abs(delta.x) > self.drag_threshold or abs(delta.y) > self.drag_threshold:
            self.drag_started = True

        self.last_pos = current_pos
        return delta

    def is_click_on_selected_object(self) -> bool:
        return self.clicked_object is not None and self.clicked_object.is_selected

    def reset(self):
        self.start_pos = None
        self.last_pos = None
        self.drag_started = False
        self.clicked_object = None
