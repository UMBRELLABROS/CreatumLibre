from enum import Enum

from PyQt6.QtCore import QEvent, Qt


class InputMode(Enum):
    IDLE = 0
    SELECT_REGION = 1
    SELECT_POINT_CLOUD = 2  # ✅ Example new mode


class SELECT_REGION(Enum):
    IDLE = 0  # no mode
    START = 1  # mouse down
    DRAG = 2  # mouse move
    STOP = 3  # mouse up


class UiMode:
    """
    Handles UI interaction modes like selecting regions, point clouds, etc.
    """

    def __init__(self, name: str, init_key=None, key_action=None):
        self.name = name
        self.mode = InputMode.IDLE  # ✅ Use Enum for mode state
        self.init_key = init_key  # ✅ Store required key for mode activation
        self.key_action = key_action  # ✅ Store required key for action execution

    def set_mode(self, mode):
        """Set the UI mode."""
        self.mode = mode
        print(f"Active mode: {self.mode}")

    def get_mode(self):
        """Return the current UI mode."""
        return self.mode

    def key_interpretation(self):
        """Interpret key presses based on the active mode."""
        if self.mode == InputMode.IDLE:
            return None
        if self.mode == InputMode.SELECT_REGION:
            return (
                self.init_key or "Control"
            )  #  Default to Control unless explicitly set
        if self.mode == InputMode.SELECT_POINT_CLOUD:
            return self.init_key or "Shift"  #  Default to Shift for point clouds
        return None  #  Future modes can extend this logic

    def reset_mode(self):
        """Reset the mode to IDLE."""
        self.mode = InputMode.IDLE

    def key_action_handler(self, event):
        """Handle key actions based on the current mode."""
        if event.key() == Qt.Key_Escape:
            self.reset_mode()

        elif self.mode == InputMode.SELECT_REGION:
            if event.mouseButton() == Qt.MouseButton.LeftButton:
                if event.type() == QEvent.Type.MouseButtonPress:
                    self.set_mode(SELECT_REGION.START)
                elif event.type() == QEvent.Type.MouseMove:
                    self.set_mode(SELECT_REGION.DRAG)
                elif event.type() == QEvent.Type.MouseButtonRelease:
                    self.set_mode(SELECT_REGION.STOP)
        elif self.mode == InputMode.SELECT_POINT_CLOUD and event.key() == self.init_key:
            self.set_mode(InputMode.IDLE)
        elif self.key_action and event.key() == self.key_action:
            # Execute the action associated with the key
            print(f"Executing action for key: {self.key_action}")
            # Here you would call the actual function that handles the action
