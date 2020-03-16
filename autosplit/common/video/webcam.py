from cv2 import (
    CAP_DSHOW,
    WND_PROP_VISIBLE,
    destroyAllWindows,
    getWindowProperty,
    imshow,
    VideoCapture,
    waitKey,
)
from threading import Thread
from typing import Any, Optional


class Webcam(Thread):
    window_name = 'Video Stream'
    key_escape = 27
    exit_flag = False

    def __init__(self, input=0, args=None, debug=False):
        self.input = input
        self.frame = None
        self.debug = debug
        super(Webcam, self).__init__(target=self.__run, args=args)

    def __run(self, exit_flag):
        self.video_capture = VideoCapture(self.input, CAP_DSHOW)

        while True:
            if exit_flag():
                break

            ret, self.frame = self.video_capture.read()
            if self.debug:
                imshow(self.window_name, self.frame)
                waitKey(1)

        self.video_capture.release()
        destroyAllWindows()

    def get_frame(self):
        return self.frame
