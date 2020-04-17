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
from util.buffer_worker import BufferConsumer, BufferProducer
from util.display import InformationDisplay


# TODO: in hindsight, this class should probably inherit from trigger_listener,
# but I have a feeling that would require a ton of work, and I might want to get
# rid of the trigger listener class all together
class AutoSplit():
    spatula_count = 0
    sock_count = 0

    def __init__(self) -> None:
        self.debug = DEBUG
        self.livesplit = LiveSplitSignal()
        self.route = get_route()
        self.stop_threads = False

        self._start_listener()
        self._start_webcam()
        self._start_buffers()

        self.display = InformationDisplay()
        self.buffer_cons.join()
        self.buffer_prod.join()
        self.trigger_listener.join()
        self.display.clean()

    def _exit_callback(self) -> None:
        self.stop_threads = True

    def _start_buffers(self) -> None:
        frame_buffer = FrameBuffer()
        frame_buff_lock = Lock()

        self.buffer_cons: BufferConsumer = BufferConsumer(
            args=(lambda: self.stop_threads, ),
            callback=self._trigger_callback,
            debug=self.debug,
            frame_buffer=frame_buffer,
            lock=frame_buff_lock,
            webcam=self.webcam,
        )
        self.buffer_prod: BufferProducer = BufferProducer(
            args=(lambda: self.stop_threads, ),
            debug=self.debug,
            frame_buffer=frame_buffer,
            lock=frame_buff_lock,
            webcam=self.webcam,
        )

        self.buffer_cons.start()
        self.buffer_prod.start()

    def _start_listener(self) -> None:
        self.trigger_listener = TriggerListener(
            KeyCode.from_char('\\'),
            trigger_callback=None,
            exit_callback=self._exit_callback,
        )
        self.trigger_listener.start()

    def _start_webcam(self) -> None:
        self.webcam = Webcam(input=0,
                             args=(lambda: self.stop_threads, ),
                             debug=self.debug)
        self.webcam.start()

    def _trigger_callback(self, prediction: Prediction) -> None:
        if self.debug: # TODO: move debug to curses logic or something like that
            self.display.set_prediction(prediction)
            
        # Ignore prediction, unless it's the next logical increment
        # TODO: this could result in a deadlock, add a retry count, so
        #       if the counter gets out of sync, we can recover
        if prediction.label == self.spatula_count + 1:
            self.spatula_count += 1
        else:
            return

        if self.route[0]["spatula"] == self.spatula_count:
            # self.livesplit.split()
            self.route.pop(0)


if __name__ == '__main__':
    autosplit = AutoSplit()
