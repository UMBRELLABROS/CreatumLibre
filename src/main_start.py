import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class ImageTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(
            True
        )  # Ensure the image scales inside the tab


class CreatumLibre(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CreatumLibre")
        self.setGeometry(100, 100, 1200, 800)  # Default window size

        self.init_menu()
        self.init_layout()

    def init_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("Files")
        file_actions = {
            "New": ("Ctrl+N", lambda: None),
            "Open": ("Ctrl+O", self.load_new_image),  # Directly bind function here
            "Save": ("Ctrl+S", lambda: None),
            "Save As": ("Ctrl+Shift+S", lambda: None),
            "Quit": ("Ctrl+Q", self.close),  # Close the app on Quit
        }

        for name, (shortcut, function) in file_actions.items():
            action = QAction(name, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(function)  # Assign the function
            file_menu.addAction(action)

        # Zoom Menu
        zoom_menu = menu_bar.addMenu("Zoom")
        zoom_actions = [
            ("Zoom In", "Ctrl++"),
            ("Zoom Out", "Ctrl+-"),
            ("Fit to Frame", "Ctrl+#"),
            ("Reset", "Ctrl+."),
        ]
        for name, shortcut in zoom_actions:
            action = QAction(name, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(
                self.load_new_image if name == "Open" else lambda: None
            )
            zoom_menu.addAction(action)

    def init_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab())
        self.tab_widget.setMovable(True)
        main_layout.addWidget(self.tab_widget)

        # Top Layout (~90% of height)
        top_layout = QHBoxLayout()
        left_sidebar = QWidget()  # Placeholder for left sidebar
        right_sidebar = QWidget()  # Placeholder for colors

        left_sidebar.setMinimumWidth(200)
        right_sidebar.setMinimumWidth(200)

        top_layout.addWidget(left_sidebar)
        top_layout.addWidget(self.tab_widget, stretch=1)
        top_layout.addWidget(right_sidebar)

        # Bottom Layout (~10% of height)
        bottom_info_bar = QWidget()  # Placeholder for additional information
        bottom_info_bar.setFixedHeight(80)

        main_layout.addLayout(top_layout, stretch=9)
        main_layout.addWidget(bottom_info_bar, stretch=1)

        central_widget.setLayout(main_layout)

    def load_new_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.bmp)"
        )

        if file_path:
            image_tab = ImageTabWidget()
            image_tab.load_image(file_path)
            self.tab_widget.addTab(image_tab, f"Image {self.tab_widget.count() + 1}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreatumLibre()
    window.show()
    sys.exit(app.exec())
