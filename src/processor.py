from image.diglet.model import CnnModel
from image.diglet.image_processor import ImageSet

if __name__ == '__main__':
    image_set = ImageSet()

    cnn_model = CnnModel(image_set.get_num_classes())
    cnn_model.compile_model()
    cnn_model.fit_model(image_set)
