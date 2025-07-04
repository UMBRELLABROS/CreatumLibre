# pylint: disable=no-member

import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap

from creatumlibre.graphics.boolean_operations.image_boolean import Vector2D, merge
from creatumlibre.ui.manager.image_handler import ImageHandler
from creatumlibre.ui.mode.ui_input_mode import TransformMode


class ObjectManager:
    """Manages rectangular images (with optional masks) to produce one composited picture."""

    def __init__(self, file_path: str):
        self.object_list = []
        self.zoom_factor = 1.0

        self._add_new_image_by_filename(file_path)

    def _add_new_image_by_filename(self, file_path):
        new_np_image = cv2.imread(file_path)
        image_instance = ImageHandler(new_np_image, Vector2D(0, 0), False)
        self.object_list.append(image_instance)

    def get_base_image(self):
        return self.object_list[0].get_image() if self.object_list else None

    def get_promoted_object(self):
        """get the promoted image by flag"""
        for image_object in self.object_list:
            if image_object.is_promoted:
                return image_object
        return None

    def get_parent(self):
        """get the activated object or the base image"""
        for image_object in self.object_list:
            if image_object.is_selected:
                return image_object
        return self.get_base_object()

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
            self.object_list.remove(image_object)

    def add_object(self, image_handler: ImageHandler):
        """Adds a new object"""
        self.object_list.append(image_handler)

    def get_object_at(self, position: Vector2D):
        """get image at clicked point"""
        for image_object in reversed(self.object_list[1:]):
            if image_object.contains_point(position) and not image_object.is_promoted:
                return image_object
        return None

    def set_selected_object_by_click(self, position: Vector2D, modifiers):
        """scan all objects from top to bottom it is hit"""
        count = 0
        for image_object in reversed(self.object_list[1:]):
            if image_object.contains_point(position) and not image_object.is_promoted:
                count += 1
                image_object.position_before_drag = image_object.position
                if (
                    modifiers & Qt.KeyboardModifier.ControlModifier
                    or modifiers & Qt.KeyboardModifier.MetaModifier
                ):
                    print("modifier: select")
                    image_object.is_selected = not image_object.is_selected
                else:
                    print("single: select")
                    self.clear_selection()
                    image_object.is_selected = True
        if count == 0:
            self.clear_selection()

    def set_new_position(self):
        """new posiotn of the moved object"""
        for image_object in reversed(self.object_list[1:]):
            if image_object.is_selected:
                image_object.position_before_drag = image_object.position

    def update_selected_position(self, delta: Vector2D):
        """update all selected posiitons"""
        selected_count = sum(obj.is_selected for obj in self.object_list[1:])
        print(f"{selected_count} objects selected.")

        for image_object in reversed(self.object_list[1:]):
            if image_object.is_selected:
                # print(f"dx: {dx}, dy: {dy}")
                print(image_object.position_before_drag.to_tuple())
                print("------")
                image_object.set_position(image_object.position_before_drag + delta)

    def clear_selection(self):
        """release all selections i.e: by Esc"""
        for image_object in reversed(self.object_list):
            image_object.is_selected = False

    def clear_promoted(self):
        """release all promotions i.e: by Esc"""
        for image_object in reversed(self.object_list):
            if image_object.is_promoted:
                self.delete_object(image_object)

    def copy_promoted_to_clipboard(self, is_cut: bool) -> ImageHandler:
        """create a new object from the promoted image
        param is_cut: if is cut: erase the underlying image
        """
        print(f"Cut mode: {is_cut}")
        if (promoted_object := self.get_promoted_object()) is not None:
            return promoted_object.copy()
        return None

    def paste_clipboard(self, clipboard: ImageHandler):
        """put clipboard image to object list"""
        image_object = clipboard.copy()
        image_object.is_selected = True
        image_object.is_promoted = False
        self.add_object(image_object)

    def merge_selection(self):
        """Finds the promoted object and merges it into the layer below."""
        # Find promoted ImageHandler
        promoted = self.get_promoted_object()

        index = self.object_list.index(promoted)
        if index == 0:
            # No underlying layer to merge into
            return

        target = self.object_list[index - 1]

        merge(from_obj=promoted, to_obj=target)

        # Remove promoted selection from stack
        self.object_list.remove(promoted)
