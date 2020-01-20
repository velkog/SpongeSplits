import cv2
from threading import Thread


class Webcam(Thread):
    window_name = 'Video Stream'
    key_escape = 27

    def __init__(self, input):
        self.video_capture = cv2.VideoCapture(input, cv2.CAP_DSHOW)
        super(Webcam, self).__init__(target=self.__run)

    def __run(self):
        while True:
            ret, self.frame = self.video_capture.read()
            cv2.imshow(self.window_name, self.frame)

            # If escape key is pressed, or the window is closed then break out
            if cv2.waitKey(1) == self.key_escape or cv2.getWindowProperty(
                    self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        cv2.destroyAllWindows()

    def get_frame(self):
        return self.frame
