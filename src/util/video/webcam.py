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

    def __init__(self, input=0, debug=False):
        self.frame = None
        self.video_capture = VideoCapture(input, CAP_DSHOW)
        self.debug = debug
        super(Webcam, self).__init__(target=self.__run)

    def __run(self):
        while True:
            ret, self.frame = self.video_capture.read()

            # If escape key is pressed, or we have called the exit
            # function then break
            if waitKey(1) == self.key_escape or self.exit_flag:
                break

            if self.debug:
                imshow(self.window_name, self.frame)

            # If the window is closed then break out
            if getWindowProperty(self.window_name, WND_PROP_VISIBLE) < 1:
                break

        destroyAllWindows()

    def get_frame(self) -> Optional[Any]:
        return self.frame

    def exit(self):
        self.exit_flag = True
