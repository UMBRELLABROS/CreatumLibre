# pylint: disable=no-member

import cv2
from PyQt6.QtGui import QImage, QPixmap

from creatumlibre.graphics.boolean_operations.image_boolean import merge
from creatumlibre.ui.manager.image_handler import ImageHandler
from creatumlibre.ui.mode.ui_input_mode import TransformMode


class ObjectManager:
    """Manages rectangular images (with optional masks) to produce one composited picture."""

    def __init__(self, file_path: str):
        self.object_list = []
        self.actual_object_index = 0
        self.zoom_factor = 1.0

        self._add_new_image_by_filename(file_path)

    def get_active_object_index(self):
        """be sure, the index is valid"""
        if not self.object_list:
            return None
        return min(self.actual_object_index, len(self.object_list) - 1)

    def _add_new_image_by_filename(self, file_path):
        new_np_image = cv2.imread(file_path)
        image_instance = ImageHandler(new_np_image, (0, 0), False)
        self.object_list.append(image_instance)

    def get_base_image(self):
        return self.object_list[0].get_image() if self.object_list else None

    def get_active_image(self):
        if (idx := self.get_active_object_index()) is None:
            return None
        return self.object_list[idx].get_image()

    def get_promoted_object(self):
        """get the promoted image by flag"""
        for image_object in self.object_list:
            if image_object.is_promoted:
                return image_object
        return None

    def get_active_object(self):
        if (idx := self.get_active_object_index()) is None:
            return None
        return self.object_list[idx]

    def get_base_object(self):
        return self.object_list[0] if self.object_list else None

    def show_resulting_image(self) -> QPixmap:
        """Composites all objects into a final image and returns it as QPixmap."""
        if not self.object_list:
            return QPixmap()

        base_image = self.object_list[0].copy()

        for image_obj in self.object_list[1:]:
            overlay_obj = image_obj.copy()
            if image_obj.is_promoted:
                overlay_obj.draw_selection_frame(TransformMode.NONE, self.zoom_factor)
            if image_obj.is_selected:
                overlay_obj.draw_selection_frame(TransformMode.SCALE, self.zoom_factor)
            merge(overlay_obj, base_image)

        return self._to_qpixmap(base_image.get_image())

    def _to_qpixmap(self, image) -> QPixmap:
        """Converts cv2 image (BGR) to QPixmap with zoom applied."""
        zoomed = cv2.resize(image, (0, 0), fx=self.zoom_factor, fy=self.zoom_factor)
        rgb = cv2.cvtColor(zoomed, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb.shape
        q_image = QImage(
            rgb.data, width, height, channel * width, QImage.Format.Format_RGB888
        )
        return QPixmap.fromImage(q_image)

    def delete_object(self, image_object: ImageHandler):
        """Deletes object from list by value"""
        if image_object in self.object_list:
            index = self.object_list.index(image_object)
            self.object_list.remove(image_object)
            self.actual_object_index = max(0, index - 1)

    def add_object(self, image_handler: ImageHandler, position: int | None = None):
        """Adds a new object at the specified index or end."""
        insert_at = self.actual_object_index + 1 if position is None else position
        self.object_list.insert(insert_at, image_handler)
        self.actual_object_index = insert_at

    def select_object(self, index: int):
        """Sets the active object to manipulate."""
        if 0 <= index < len(self.object_list):
            self.actual_object_index = index

    def set_selected_object_by_click(self, position: tuple[int, int]) -> bool:
        """scan all objects from top to bottom it is hit"""
        for image_object in reversed(self.object_list[1:]):
            if image_object.contains_point(position):
                image_object.is_selected = True
                image_object.position_before_drag = image_object.position
                return True
        return False

    def update_selected_position(self, dx: int, dy: int):
        """update all selected posiitons"""
        for image_object in reversed(self.object_list[1:]):
            if image_object.is_selected:
                print(f"dx: {dx}, dy: {dy}")
                image_object.set_position(
                    (
                        image_object.position_before_drag[0] + dx,
                        image_object.position_before_drag[1] + dy,
                    )
                )

    def clear_selection(self):
        """release all selections i.e: by Esc"""
        for image_object in reversed(self.object_list):
            image_object.is_selected = False

    def copy_promoted(self, is_cut: bool):
        """create a new object from the promoted image
        param is_cut: if is cut: erase the underlying image
        """
        new_object = self.get_promoted_object().copy()
        self.add_object(new_object)
        print(is_cut)

    def delete_promoted(self):
        """create a new object from the promoted image
        param is_cut: if is cut: erase the underlying image
        """
        self.delete_object(self.get_promoted_object())

    def get_tab_pixmap(self) -> QPixmap:
        """Convenience method for tab manager to retrieve full composition."""
        return self.show_resulting_image()

    def merge_selection(self):
        """Finds the promoted object and merges it into the layer below."""
        # Find promoted ImageHandler
        promoted = next(
            (obj for obj in self.object_list if getattr(obj, "is_promoted", False)),
            None,
        )
        if not promoted:
            return

        index = self.object_list.index(promoted)
        if index == 0:
            # No underlying layer to merge into
            return

        target = self.object_list[index - 1]

        merge(from_obj=promoted, to_obj=target)

        # Remove promoted selection from stack
        self.object_list.remove(promoted)
