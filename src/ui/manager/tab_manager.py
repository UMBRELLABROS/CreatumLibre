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

from ui.manager.object_manager import ObjectManager


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
        self.tab_widget.setMovable(True)
        self.tab_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.parent.workspace_layout.addWidget(self.tab_widget)

    def _add_scroll_container(self, filename):
        """Add a scroll container arounf the objects"""
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
        }

        self.refresh_tab_display(tab_index)

    def refresh_tab_display(self, tab_index):
        # should happen in Object Mannager, but called here
        pass

    def get_active_tab(self):
        """Retrieves the current ObjectManager instance safely."""
        if (current_index := self.tab_widget.currentIndex()) == -1:
            return None

        return self.object_manager_instances.get(current_index, None)
