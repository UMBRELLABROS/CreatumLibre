from ui.manager.image_handler import ImageHandler


class ObjectManager:
    """Manages rectengulat images to result in one picture"""

    def __init__(self, file_path: str):
        # load the initial image
        self.object_list = []
        self.zoom_factor = 1.0

        image_instance = ImageHandler(file_path)
        self.object_list.append(image_instance)

    def show_resulting_image(self):
        """show all images in the given order"""

    def delete_object(self):
        pass

    def add_object(self):
        pass

    def select_object(self):
        """Selct the object, to manipulate it"""
