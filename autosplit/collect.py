from cv2 import imwrite
from pynput.keyboard import KeyCode
from threading import Thread, Lock
from typing import List

from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer
from util.keyboard.trigger_listener import TriggerListener
from util.video.webcam import Webcam

DEBUG = 1
PRESET_NUM = 59
STARTING_COUNT = 0
DATASET_PATH = 'dataset/360/'  # TODO: Separate this out into a config


class AutoSplitDataCollect():
    frame_list: List[SpongeFrame] = []

    def __init__(self, spatula: bool, count: int = 0) -> None:
        self.count = count
        self.spatula: bool = spatula
        self.prefix: str = "spatula" if spatula else "sock"
        self.__start_listener()
        self.__start_webcam()

        self.trigger_listener.join()

    def __start_webcam(self):
        self.thread_webcam: Webcam = Webcam(input=0, debug=DEBUG)
        self.thread_webcam.start()

    def __start_listener(self):
        self.trigger_listener = TriggerListener(KeyCode.from_char('\\'),
                                                self.__trigger_callback,
                                                self.__exit_callback)
        self.trigger_listener.start()

    def __exit_callback(self):
        self.thread_webcam.exit()

    def __trigger_callback(self):
        frame = self.thread_webcam.get_frame()
        if frame is not None:
            sponge_frame = SpongeFrame(frame)
            saved_file = "%s%s/%s-%d-%d.jpg" % (
                DATASET_PATH, self.prefix, self.prefix, PRESET_NUM, self.count)
            imwrite(saved_file, frame)
            print('Frame saved to file %s.' % (saved_file))

            self.count += 1


if __name__ == '__main__':
    autosplit = AutoSplitDataCollect(
        True,
        STARTING_COUNT,
    )
