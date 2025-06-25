# pylint: disable=no-member
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from creatumlibre.ui.manager.object_manager import ObjectManager


class TabManager:
    """Manages loading new image to object list (positon[0]), tab creation, and scrolling."""

    def __init__(self, parent):
        self.parent = parent
        self.tab_widget = QTabWidget()
        self.object_manager_instances = {}  # Track objectManagers by tab index

        self._init_layout()

    def _init_layout(self):
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        # self.tab_widget.installEventFilter(self.parent.input_handler)
        self.tab_widget.setMovable(True)
        self.tab_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tab_widget.setFocus()
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.parent.workspace_layout.addWidget(self.tab_widget)

    def _add_scroll_container(self, filename):
        """Add a scroll container around the objects"""
        scroll_area_widget = QScrollArea()
        scroll_area_widget.setWidgetResizable(True)
        scroll_area_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        scroll_area_widget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        # Fixed image/object-manger container inside the scroll area
        object_manager_container_widget = QWidget()
        object_manager_container_layout = QVBoxLayout(object_manager_container_widget)
        object_manager_container_layout.setContentsMargins(0, 0, 0, 0)

        object_manager_label_widget = QLabel()
        object_manager_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        object_manager_container_layout.addWidget(object_manager_label_widget)
        object_manager_container_widget.setLayout(object_manager_container_layout)

        # Place fixed widget inside the scrollable area
        scroll_area_widget.setWidget(object_manager_container_widget)
        tab_index = self.tab_widget.addTab(scroll_area_widget, filename)
        return tab_index, object_manager_label_widget

    def load_new_image(self, file_path):
        """Load a new image with scroll support inside a fixed widget."""
        object_manager_instance = ObjectManager(file_path)
        filename = Path(file_path).name

        tab_index, object_manager_label_widget = self._add_scroll_container(filename)
        self.object_manager_instances[tab_index] = {
            "manager": object_manager_instance,
            "widget": object_manager_label_widget,  # Store label reference per tab
            "file_apth": file_path,  # saved for saving
        }

        self.refresh_tab_display(tab_index)
        self.tab_widget.setCurrentIndex(tab_index)

    def refresh_tab_display(self, tab_index):
        """Redraws the image for a specific tab by requesting a refreshed pixmap."""
        if tab_index not in self.object_manager_instances:
            return

        obj_ref = self.object_manager_instances[tab_index]

        tab_pixmap = obj_ref[
            "manager"
        ].get_tab_pixmap()  # Get final image with all objects/layers
        self._refresh_widget(widget=obj_ref["widget"], pixmap=tab_pixmap)

    def refresh_active_tab_display(self):
        """Convinience methot to update the tab"""
        active_tab = self.get_active_tab_index()
        self.refresh_tab_display(active_tab)

    def _refresh_widget(self, widget: QWidget, pixmap):
        """update widget"""
        widget.setPixmap(pixmap)
        widget.repaint()

    def get_active_tab(self):
        """Retrieves the current ObjectManager instance safely."""
        if (current_index := self.tab_widget.currentIndex()) == -1:
            return None

        return self.object_manager_instances.get(current_index, None)

    def get_active_tab_index(self):
        return self.tab_widget.currentIndex()

    def zoom_in(self):
        """Increase the zoom level of the active image."""
        self.apply_zoom(1.2)

    def zoom_out(self):
        """Decrease the zoom level of the active image."""
        self.apply_zoom(0.8)

    def apply_zoom(self, factor: float):
        """Zoom in or out while maintaining aspect ratio."""
        if (active_tab := self.get_active_tab()) is None:
            return
        active_tab["manager"].zoom_factor = max(
            0.1, min(3.0, active_tab["manager"].zoom_factor * factor)
        )  # Prevent extreme zoom
        self._refresh_widget(
            active_tab["widget"], active_tab["manager"].get_tab_pixmap()
        )

    def fit_to_container(self):
        """Resize the image while preserving aspect ratio."""
        print("Fitting image to container with aspect ratio")

        if (active_tab := self.get_active_tab()) is None:
            return

        container_width = self.tab_widget.width()
        container_height = self.tab_widget.height()

        image_width, image_height = (
            active_tab["manager"].get_base_image().shape[1],
            active_tab["manager"].get_base_image().shape[0],
        )

        # Calculate the best zoom factor
        scale_x = container_width / image_width
        scale_y = container_height / image_height
        active_tab["manager"].zoom_factor = max(
            scale_x, scale_y
        )  #  Ensures aspect ratio is preserved

        print(
            f" Calculated zoom factor: {active_tab["manager"].zoom_factor}, {scale_x=}, {scale_y=}"
        )
        # Resize the image
        self.apply_zoom(
            active_tab["manager"].zoom_factor
        )  #  Use zoom logic to resize properly

    def reset_zoom(self):
        """Reset zoom level for active image."""
        if (active_tab := self.get_active_tab()) is None:
            return

        active_tab["manager"].zoom_factor = 1.0
        self._refresh_widget(
            active_tab["widget"], active_tab["manager"].get_tab_pixmap()
        )
