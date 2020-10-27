from pynput.keyboard import KeyCode
from threading import Lock, enumerate
from typing import List

from common.livesplit import LiveSplitSignal
from common.keyboard.trigger_listener import TriggerListener
from common.video.webcam import Webcam
from config import DEBUG, get_route
from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer
from image.diglet.model import Prediction
from util.frame_processor import FrameProcessor
from util.display import InformationDisplay


# TODO: in hindsight, this class should probably inherit from trigger_listener,
# but I have a feeling that would require a ton of work, and I might want to get
# rid of the trigger listener class all together
class AutoSplit:
    spatula_count = 0
    sock_count = 0

    def __init__(self) -> None:
        self.livesplit = LiveSplitSignal()
        self.route = get_route()
        self.stop_threads = False
        self.display = InformationDisplay()

        self._start_listener()
        self._start_webcam()
        self._start_buffers()
        self.display.start()

        self.frame_processor.join()
        self.trigger_listener.join()
        self.display.clean()

    def _exit_callback(self) -> None:
        self.stop_threads = True

    def _start_buffers(self) -> None:
        self.frame_processor: FrameProcessor = FrameProcessor(
            args=(lambda: self.stop_threads,),
            callback=self.__trigger_callback,
            display=self.display,
            webcam=self.webcam,
        )

        self.frame_processor.start()

    def _start_listener(self) -> None:
        self.trigger_listener = TriggerListener(
            KeyCode.from_char("\\"),
            trigger_callback=None,
            exit_callback=self._exit_callback,
        )
        self.trigger_listener.start()

    def _start_webcam(self) -> None:
        self.webcam = Webcam(input=0, args=(lambda: self.stop_threads,), debug=DEBUG)
        self.webcam.start()

    def __trigger_callback(self, spatula_prediction: Prediction) -> None:
        self.display.set_prediction(spatula_prediction)

        split_name, split_value = next(iter(self.route[0].items()))
        if split_value == spatula_prediction.label:
            self.display.log(f"Split action occured for '{split_name}'")
            self.livesplit.split()
            self.route.pop(0)


if __name__ == "__main__":
    autosplit = AutoSplit()
