from cv2 import imwrite
from os import makedirs
from pynput.keyboard import KeyCode
from time import sleep
from typing import List

from common.error import report
from common.error.exceptions import InvalidOptionException, OutOfRangeOptionException
from common.error.validate import validate_int
from common.keyboard.trigger_listener import TriggerListener
from common.video.webcam import Webcam
from image.diglet.specifications import get_datapath
from image.frame import SpongeFrame

# TODO: This isn't the cleanest and I don't really this it'll be worth cleaning this up
DATASET_PATH = get_datapath()
EXIT = False
EXIT_LAMBDA = (lambda: EXIT,)
OPTIONS: List[str] = ["Save a single frame when trigger is pressed", "Exit"]
WEBCAM: Webcam


class BaseDataCollector:
    def __init__(self, count: int, label_prefix: str, webcam: Webcam) -> None:
        self._count = count
        self._label_prefix = label_prefix
        self._directory = "%sunsorted/%s/" % (DATASET_PATH, self._label_prefix)
        self._webcam = webcam

        try:
            makedirs(self._directory)
        except FileExistsError:
            pass

        self._start_listener()
        self._trigger_listener.join()

    def _exit_callback(self):
        pass

    def _get_filename(self):
        return "%s%s_%d.jpg" % (self._directory, self._label_prefix, self._count)

    def _save_frame(self):
        frame = self._webcam.get_frame()
        if frame is not None:
            file_name = self._get_filename()
            SpongeFrame(frame).save_frame(file_name)
            print("Frame saved to file %s." % (file_name))
            self._count += 1

    def _start_listener(self):
        self._trigger_listener = TriggerListener(
            KeyCode.from_char("\\"), self._trigger_callback, self._exit_callback
        )
         self._trigger_listener.start()

    def _trigger_callback(self):
        pass


class SingleFrameDataCollector(BaseDataCollector):
    def _trigger_callback(self):
        self._save_frame()


if __name__ == "__main__":
    WEBCAM = Webcam(args=EXIT_LAMBDA, input=0, debug=True)
    WEBCAM.start()

    while True:
        print("Select a collection mode:")
        for count, option in enumerate(OPTIONS, start=1):
            print("%s. %s" % (count, option))

        try:
            selection = validate_int(input(), range_min=1, range_max=len(OPTIONS))
            if selection == len(OPTIONS):
                break
            label_prefix = input("Enter desired title prefix: ")
            count = validate_int(input("Enter starting count: "))

            if selection == 1:
                SingleFrameDataCollector(count=count,
                                         label_prefix=label_prefix,
                                         webcam=WEBCAM)
                SingleFrameDataCollector(
                    count=count, label_prefix=label_prefix, webcam=WEBCAM
                )

        except InvalidOptionException as e:
            report(e)
            break
        except OutOfRangeOptionException as e:
            report(e)
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            report("Error: unhandled exception: '%s'" % (str(e)))
            break

    EXIT = True
