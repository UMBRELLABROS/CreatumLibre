from PyQt6.QtWidgets import QDialog


class DialogManager:
    """Handles all sorts of non-modal dialogs"""

    def __init__(self):
        self.dialogs: dict[type, QDialog] = {}

    def show(self, dialog: QDialog):
        dialog_type = type(dialog)
        if dialog_type not in self.dialogs:
            self.dialogs[dialog_type] = dialog
            dialog.show()
        else:
            existing = self.dialogs[dialog_type]
            existing.raise_()
            existing.activateWindow()

    def exec(self, dialog: QDialog):
        dialog_type = type(dialog)
        if dialog_type not in self.dialogs:
            self.dialogs[dialog_type] = dialog
            dialog.exec()
        else:
            existing = self.dialogs[dialog_type]
            existing.raise_()
            existing.activateWindow()

    def update(self, dialog_type: type):
        if dialog_type in self.dialogs:
            dialog = self.dialogs[dialog_type]
            if hasattr(dialog, "refresh"):
                dialog.refresh()

    def remove(self, dialog_type: type):
        if dialog_type in self.dialogs:
            del self.dialogs[dialog_type]
