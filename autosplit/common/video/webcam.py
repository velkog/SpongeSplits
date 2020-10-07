from cv2 import (
    CAP_DSHOW,
    WND_PROP_VISIBLE,
    destroyAllWindows,
    getWindowProperty,
    imshow,
    rectangle,
    VideoCapture,
    waitKey,
)
from threading import Thread
from typing import Any, List, Optional

from common.colors import RED, GREEN, BLUE
from config import (
    get_sock_coordinates,
    get_spatula_coordinates,
    get_textbox_coordinates,
    Identity,
)


class Webcam(Thread):
    window_name = 'Video Stream'
    key_escape = 27
    exit_flag = False

    def __init__(self,
                 args,
                 debug=False,
                 input=0,
                 states: List[Identity] = []):
        self.debug = debug
        self.frame = None
        self.input = input
        self.states = states
        super(Webcam, self).__init__(target=self._run, args=args)

    def _run(self, exit_flag):
        self.video_capture = VideoCapture(self.input, CAP_DSHOW)

        while True:
            if exit_flag():
                break

            ret, self.frame = self.video_capture.read()
            if self.debug:
                self.draw_rectangle()
                imshow(self.window_name, self.frame)
                waitKey(1)

        self.video_capture.release()
        destroyAllWindows()

    def draw_rectangle(self):
        if Identity.NONE in self.states:
            return

        if Identity.SPATULA in self.states or Identity.ALL in self.states:
            coord_0, coord_1 = get_spatula_coordinates()
            rectangle(self.frame, coord_0, coord_1, BLUE.rgb, 2)

        if Identity.SOCK in self.states or Identity.ALL in self.states:
            coord_0, coord_1 = get_sock_coordinates()
            rectangle(self.frame, coord_0, coord_1, GREEN.rgb, 2)

        if Identity.TEXTBOX in self.states or Identity.ALL in self.states:
            coord_0, coord_1 = get_textbox_coordinates()
            rectangle(self.frame, coord_0, coord_1, RED.rgb, 2)

    def get_frame(self):
        return self.frame

    def set_states(self, states: List[Identity]) -> None:
        self.states = states