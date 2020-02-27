from os import listdir

from cv2 import imread, imshow, waitKey, destroyAllWindows
from image.frame import SpongeFrame

DATASET_PATH = 'dataset/'
SPATULA_PATH = 'spatula/'
SOCK_PATH = 'sock/'


def color_difference(color1, color2):
    return sum([
        abs(component1 - component2)
        for component1, component2 in zip(color1, color2)
    ])


class FrameHash():

    def __init__(self):
        self.__build_hash()
        print("hello")

    def __build_hash(self):
        for file in listdir(DATASET_PATH + SPATULA_PATH):
            filepath = DATASET_PATH + SPATULA_PATH + file
            frame = imread(filepath)
            sponge_frame = SpongeFrame(frame)
            spatula_img = sponge_frame.get_spatula_img()

            h = spatula_img.shape[0]
            w = spatula_img.shape[1]

            hash_dict = {}
            for y in range(0, h):
                for x in range(0, w):
                    color = spatula_img[y, x]

                    # going for more strict bounds here on 'what is yellow', but might need loosen up
                    if not (color[2] > 200 and color[1] > 200 and
                            color[0] < 50):
                        spatula_img[y, x] = [0, 0, 0]

            #print(len(spatula_img))
            #print(len(len(spatula_img)))
