from cv2 import imwrite
from cv2 import INTER_CUBIC, imwrite, resize
from keras.preprocessing.image import img_to_array
from numpy import array, ndarray

from image.diglet.specifications import get_num_cols, get_num_rows


class SpongeFrame():
    def __init__(self, frame):
        # TODO: move these into the config
        self.frame = frame
        spatula = frame[45:85, 325:380]
        spatula = img_to_array(spatula)
        self.spatula = resize(spatula, (get_num_cols(), get_num_rows()),
                              interpolation=INTER_CUBIC)
        self.sock = frame[380:420, 530:585]

    def save_frame(self, file_name):
        imwrite(file_name, self.frame)

    @property
    def spatula_array(self) -> ndarray:
        return array([self.spatula], dtype='float') / 255.0

    @property
    def spatula_img(self):
        return self.spatula
