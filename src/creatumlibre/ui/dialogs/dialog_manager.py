from PyQt6.QtWidgets import QDialog


class DialogManager:
    """handle the open dialogs"""

    def __init__(self):
        self.dialog_list = []

    def add_dialog(self, dialog: QDialog):
        """add a dialog so, it keeps showing"""
        self.dialog_list.append(dialog)

    def remove_dialog(self, dialog: QDialog):
        """remove the doalog from the open list"""
        self.dialog_list.remove(dialog)

    def show(self, dialog: QDialog):
        """show or raise modeless, depending on already open"""
        if dialog not in self.dialog_list:
            self.add_dialog(dialog)
            dialog.show()
        else:
            dialog.raise_()
            dialog.activateWindow()

    def exec(self, dialog: QDialog):
        """Executes the dialog modally if not already shown."""
        if dialog not in self.dialog_list:
            self.add_dialog(dialog)
            dialog.exec()
        else:
            dialog.raise_()
            dialog.activateWindow()

    def update(self, dialog_type: type):
        """update the selcted dialog"""
        for dialog in self.dialog_list:
            if isinstance(dialog, dialog_type):
                if hasattr(dialog, "refresh"):
                    dialog.refresh()
