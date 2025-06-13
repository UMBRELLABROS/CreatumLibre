# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

# Mock the entire ImageTk module globally BEFORE importing ZoomManager
with patch("ui.ui_menus.zoom.ImageTk") as mock_imagetk:
    mock_imagetk.PhotoImage = MagicMock()  # Ensure PhotoImage is fully mocked
    from ui.ui_menus.zoom import ZoomManager


@pytest.fixture
def mock_zoom():
    """Creates a mocked ZoomManager instance, including Tkinter dependencies."""
    with patch("ui.ui_menus.zoom.ImageTk.PhotoImage") as mock_photo:
        mock_photo.return_value = MagicMock()  # Fully mock PhotoImage

        mock_notebook = MagicMock()
        mock_frame = MagicMock()
        mock_notebook.get_active_frame.return_value = mock_frame

        mock_frame.image_data = MagicMock()
        mock_frame.image_data.pil = Image.new("RGB", (500, 500))
        mock_frame.image_data.tk = mock_photo.return_value  # Prevent Tkinter issues
        mock_frame.canvas = MagicMock()

        return ZoomManager(mock_notebook)


@patch("ui.ui_menus.zoom.ImageTk.PhotoImage")
def test_reset_zoom(mock_photoimage, mock_zoom):
    """Tests that reset_zoom correctly resets zoom level."""
    mock_zoom.zoom_level = 2.0
    mock_zoom.reset_zoom()
    assert mock_zoom.zoom_level == 1.0
    mock_photoimage.assert_called_once()  # Ensures PhotoImage was mocked


@patch("ui.ui_menus.zoom.ImageTk.PhotoImage")
def test_fit_to_frame(mock_photoimage, mock_zoom):
    """Tests that fit_to_frame scales images correctly."""
    mock_frame = mock_zoom.notebook.get_active_frame()
    mock_frame.canvas.winfo_width.return_value = 300
    mock_frame.canvas.winfo_height.return_value = 400

    mock_zoom.fit_to_frame()

    resized_img = mock_frame.image_data.tk
    assert resized_img is not None
    mock_photoimage.assert_called_once()


@patch("ui.ui_menus.zoom.ImageTk.PhotoImage", return_value=MagicMock())
def test_zoom_in(mock_photoimage, mock_zoom):
    """Tests zooming in increases zoom level while mocking ImageTk.PhotoImage."""
    mock_zoom.zoom_level = 1.0
    mock_zoom.zoom_in()
    assert mock_zoom.zoom_level > 1.0  # Ensure zoom level updates
    mock_photoimage.assert_called_once()  # Make sure PhotoImage was mocked


@patch("ui.ui_menus.zoom.ImageTk.PhotoImage", return_value=MagicMock())
def test_zoom_out(mock_photoimage, mock_zoom):
    """Tests zooming out decreases zoom level while mocking ImageTk.PhotoImage."""
    mock_zoom.zoom_level = 1.0
    mock_zoom.zoom_out()
    assert mock_zoom.zoom_level < 1.0  # Ensure zoom level updates
    mock_photoimage.assert_called_once()
