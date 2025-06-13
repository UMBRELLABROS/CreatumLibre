# pylint: disable=redefined-outer-name

import tkinter as tk
from unittest.mock import MagicMock

import pytest
from PIL import Image

from ui.ui_menus.zoom import ZoomManager

# Create a hidden Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the window


@pytest.fixture
def mock_zoom():
    """Fixture für einen Mock-Notebook mit ZoomManager-Instanz."""
    mock_notebook = MagicMock()
    mock_frame = MagicMock()
    mock_notebook.get_active_frame.return_value = mock_frame

    # Dummy-Bild für Tests erstellen
    mock_frame.image_data = MagicMock()
    mock_frame.image_data.pil = Image.new("RGB", (500, 500))
    mock_frame.canvas = MagicMock()

    return ZoomManager(mock_notebook)


def test_reset_zoom(mock_zoom):
    """Testet, ob `reset_zoom()` das Zoom-Level zurücksetzt."""
    mock_zoom.zoom_level = 2.0
    mock_zoom.reset_zoom()
    assert mock_zoom.zoom_level == 1.0


def test_fit_to_frame(mock_zoom):
    """Testet, ob das Bild korrekt auf den Frame skaliert wird."""
    mock_frame = mock_zoom.notebook.get_active_frame()
    mock_frame.canvas.winfo_width.return_value = 300
    mock_frame.canvas.winfo_height.return_value = 400

    mock_zoom.fit_to_frame()

    resized_img = mock_frame.image_data.tk
    assert resized_img is not None


def test_zoom_in(mock_zoom):
    """Testet, ob das Zoom-Level korrekt vergrößert wird."""
    mock_zoom.zoom_level = 1.0
    mock_zoom.zoom_in()
    assert mock_zoom.zoom_level > 1.0


def test_zoom_out(mock_zoom):
    """Testet, ob das Zoom-Level korrekt verkleinert wird."""
    mock_zoom.zoom_level = 1.0
    mock_zoom.zoom_out()
    assert mock_zoom.zoom_level < 1.0
