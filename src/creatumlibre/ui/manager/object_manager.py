# pylint: disable=no-member

import cv2
from PyQt6.QtGui import QImage, QPixmap

from creatumlibre.graphics.boolean_operations.image_boolean import merge
from creatumlibre.ui.manager.image_handler import ImageHandler


class ObjectManager:
    """Manages rectangular images (with optional masks) to produce one composited picture."""

    def __init__(self, file_path: str):
        self.object_list = []
        self.actual_object_index = 0
        self.zoom_factor = 1.0

        self._add_new_image_by_filename(file_path)

    def _add_new_image_by_filename(self, file_path):
        new_np_image = cv2.imread(file_path)
        image_instance = ImageHandler(new_np_image, (0, 0), False)
        self.object_list.append(image_instance)

    def get_base_image(self):
        return self.object_list[0].get_image() if self.object_list else None

    def get_active_image(self):
        return (
            self.object_list[self.actual_object_index].get_image()
            if self.object_list
            else None
        )

    def get_active_object(self):
        return self.object_list[self.actual_object_index] if self.object_list else None

    def get_base_object(self):
        return self.object_list[0] if self.object_list else None

    def show_resulting_image(self) -> QPixmap:
        """Composites all objects into a final image and returns it as QPixmap."""
        if not self.object_list:
            return QPixmap()

        base_image = self.object_list[0].copy()

        for image_obj in self.object_list[1:]:
            overlay_obj = image_obj.copy()
            if overlay_obj.is_promoted:
                promoted_overlay_obj = overlay_obj.copy()
                h, w = promoted_overlay_obj.get_image().shape[:2]
                cv2.rectangle(
                    promoted_overlay_obj.get_image(),
                    (0, 0),
                    (w - 1, h - 1),
                    (255, 0, 255),
                    thickness=int(1 / self.zoom_factor),
                )
                merge(promoted_overlay_obj, base_image)
            else:
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

    def delete_object(self, index=None):
        """Deletes object by index or active one."""
        idx = self.actual_object_index if index is None else index
        if 0 <= idx < len(self.object_list):
            del self.object_list[idx]
            self.actual_object_index = max(0, self.actual_object_index - 1)

    def add_object(self, image_handler: ImageHandler, position: int | None = None):
        """Adds a new object at the specified index or end."""
        insert_at = self.actual_object_index + 1 if position is None else position
        self.object_list.insert(insert_at, image_handler)
        self.actual_object_index = insert_at

    def select_object(self, index: int):
        """Sets the active object to manipulate."""
        if 0 <= index < len(self.object_list):
            self.actual_object_index = index

    def get_pixmap(self) -> QPixmap:
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
