# pylint: disable=no-member
# pylint: disable=redefined-outer-name
import cv2
import numpy as np
import pytest

from creatumlibre.ui.manager.image_handler import ImageHandler
from creatumlibre.ui.manager.object_manager import ObjectManager


@pytest.fixture
def dummy_image():
    return np.zeros((10, 10, 3), dtype=np.uint8)


@pytest.fixture
def image_handler(dummy_image):
    return ImageHandler(dummy_image, position=(0, 0), is_promoted=False)


@pytest.fixture
def manager(dummy_image, tmp_path):
    # Simulate an image file
    file_path = tmp_path / "dummy.png"

    cv2.imwrite(str(file_path), dummy_image)
    return ObjectManager(str(file_path))


def test_get_base_image_is_not_none(manager):
    assert manager.get_base_image() is not None


def test_add_object_increases_list(manager, image_handler):
    initial_len = len(manager.object_list)
    manager.add_object(image_handler)
    assert len(manager.object_list) == initial_len + 1


def test_delete_object_removes_item(manager, image_handler):
    manager.add_object(image_handler)
    length_before = len(manager.object_list)
    manager.delete_object()
    assert len(manager.object_list) == length_before - 1


def test_select_object_sets_index(manager, image_handler):
    manager.add_object(image_handler)
    manager.select_object(1)
    assert manager.actual_object_index == 1


def test_get_active_object_bounds(manager):
    # Manually break it
    manager.actual_object_index = 999
    obj = manager.get_active_object()
    assert obj is not None
