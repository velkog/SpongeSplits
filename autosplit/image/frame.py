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
        self.spatula = resize(
            spatula, (get_num_cols(), get_num_rows()), interpolation=INTER_CUBIC
        )
        self.sock = frame
        # sock = frame[380:420, 530:585]
        # sock = img_to_array(sock)
        # self.sock = resize(sock, (get_num_cols(), get_num_rows()),
        #                    interpolation=INTER_CUBIC)

    def save_frame(self, file_name):
        imwrite(file_name, self.frame)

    @property
    def spatula_array(self) -> ndarray:
        return array([self.spatula], dtype="float") / 255.0

    # @property
    def sock_array(self, x, y) -> ndarray:
        x1 = x
        x2 = x + 50
        y1 = y
        y2 = y + 55
        socky = self.sock[x1:x2, y1:y2]
        socky = img_to_array(socky)
        socky = resize(
            socky, (get_num_cols(), get_num_rows()), interpolation=INTER_CUBIC
        )

        return array([socky], dtype="float") / 255.0

    @property
    def spatula_img(self):
        return self.spatula
