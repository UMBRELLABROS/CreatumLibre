# pylint: disable=no-member

import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap

from ui.manager.image_handler import ImageHandler


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

        base_image = self.object_list[0].get_image().copy()

        for image_obj in self.object_list[1:]:
            overlay = image_obj.get_image()
            if image_obj.is_promoted:
                h, w = overlay.shape[:2]
                cv2.rectangle(
                    overlay,
                    (0, 0),
                    (w - 1, h - 1),
                    (255, 0, 255),
                    thickness=int(1 / self.zoom_factor),
                )
            mask = image_obj.get_mask()
            x, y = image_obj.get_position()

            base_image = self._blend_layer(base_image, overlay, mask, (x, y))

        return self._to_qpixmap(base_image)

    def _blend_layer(self, base, overlay, mask, position):
        """Blends an overlay image onto the base using an optional alpha mask."""
        x, y = position
        h, w = overlay.shape[:2]
        roi = base[y : y + h, x : x + w].astype(np.float32)
        overlay = overlay.astype(np.float32)

        if mask is not None:
            alpha = mask.astype(np.float32)
            if len(alpha.shape) == 2:  # Convert to 3-channel alpha if needed
                alpha = cv2.merge([alpha, alpha, alpha])
        else:
            alpha = np.ones_like(overlay, dtype=np.float32)

        blended = overlay * alpha + roi * (1 - alpha)
        base[y : y + h, x : x + w] = blended.astype(np.uint8)
        return base

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
