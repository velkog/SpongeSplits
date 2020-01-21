import cv2
from threading import Thread
import sys


class Webcam(Thread):
    window_name = 'Video Stream'
    key_escape = 27
    exit_flag = False

    def __init__(self, input):
        self.video_capture = cv2.VideoCapture(input, cv2.CAP_DSHOW)
        super(Webcam, self).__init__(target=self.__run)

    def __run(self):
        while True:
            ret, self.frame = self.video_capture.read()

            # If escape key is pressed, or we have called the exit
            # function then break
            if cv2.waitKey(1) == self.key_escape or self.exit_flag:
                break

            cv2.imshow(self.window_name, self.frame)
            # If the window is closed then break out
            if cv2.getWindowProperty(self.window_name,
                                     cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()

    def get_frame(self):
        return self.frame

    def exit(self):
        self.exit_flag = True
