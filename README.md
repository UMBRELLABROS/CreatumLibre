
## create wheel
uv pip install -e .

## activate venv
source .venv/bin/activate

## run programms from exploration
python -m exploration.first_ui


CreatumLibre (QMainWindow)
│
├── Central Widget (QWidget)
│   │
│   ├── Main Layout (QVBoxLayout)
│   │   │
│   │   ├── Top Layout (QHBoxLayout)  ← Handles main content
│   │   │   │
│   │   │   ├── Left Sidebar (QWidget)  ← Fixed width
│   │   │   ├── ImageManager (QTabWidget)  ← Main image area
│   │   │   │   ├── Scroll Area (QScrollArea)  ← Handles image scrolling?
│   │   │   │   ├── Image Instances (Dict)  ← Stores opened images
│   │   │   │   ├── SelectionOverlay (QWidget)  ← Overlay for selection masks
│   │   │   │
│   │   │   ├── Right Sidebar (QWidget)  ← Fixed width
│   │   │
│   │   ├── Bottom Info Bar (QWidget)  ← Status area
│   │
│   ├── SelectionOverlay (QWidget)  ← Overlay, attached to tab_widget
│
├── Menu Bar (QMenuBar)
│   ├── File Menu (QMenu)  ← Handles file operations
│   ├── Zoom Menu (QMenu)  ← Handles zoom functionality
│
├── InputHandler (Event Filter)  ← Handles user interaction
