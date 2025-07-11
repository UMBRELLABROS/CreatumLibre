from PyQt6.QtGui import QAction, QKeySequence


class ZoomMenu:
    """Zoom funcitons to scale the image"""

    def __init__(self, parent):
        self.parent = parent
        zoom_menu = parent.menu_bar.addMenu("Zoom")

        zoom_actions = {
            "Zoom In": ("Ctrl++", parent.tab_manager.zoom_in),
            "Zoom Out": ("Ctrl+-", parent.tab_manager.zoom_out),
            "Fit to Frame": ("Ctrl+#", parent.tab_manager.fit_to_container),
            "Reset": ("Ctrl+.", parent.tab_manager.reset_zoom),
        }

        for name, (shortcut, function) in zoom_actions.items():
            action = QAction(name, parent)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(function)
            zoom_menu.addAction(action)

    def zoom_in(self):
        """Increase the zoom level of the active image."""
        active_tab = self.parent.tab_manager.get_active_tab()
        if active_tab:
            active_tab.apply_zoom(1.2)  # Scale up by 20%

    def zoom_out(self):
        """Decrease the zoom level of the active image."""
        active_tab = self.parent.tab_manager.get_active_tab()
        if active_tab:
            active_tab.apply_zoom(0.8)  # Scale down by 20%

    def fit_to_frame(self):
        """Resize image to fit within the tab without stretching."""
        print("Fitting image to frame")
        active_tab = self.parent.tab_manager.get_active_tab()
        if active_tab:
            active_tab.fit_to_container(self.parent.tab_manager)

    def reset_zoom(self):
        """Reset zoom level to default."""
        active_tab = self.parent.tab_manager.get_active_tab()
        if active_tab:
            active_tab.reset_zoom()
