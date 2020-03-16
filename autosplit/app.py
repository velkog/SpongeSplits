from pynput.keyboard import KeyCode
from threading import Lock, enumerate
from typing import List

from common.livesplit import LiveSplitSignal
from common.keyboard.trigger_listener import TriggerListener
from config import DEBUG, get_route
from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer
from image.diglet.model import Prediction
from util.buffer_worker import BufferConsumer, BufferProducer


class AutoSplit():
    spatula_count = 0
    sock_count = 0

    def __init__(self) -> None:
        self.debug = DEBUG
        self.livesplit = LiveSplitSignal()
        self.route = get_route()

        self.__start_listener()
        self.__start_buffers()

        self.buffer_cons.join()
        self.buffer_prod.join()
        self.trigger_listener.join()

    def __start_listener(self) -> None:
        self.trigger_listener = TriggerListener(
            KeyCode.from_char('\\'),
            trigger_callback=None,
            exit_callback=self.__exit_callback)
        self.trigger_listener.start()

    def __start_buffers(self) -> None:
        frame_buffer = FrameBuffer()
        frame_buff_lock = Lock()

        self.stop_threads = False
        args = (lambda: self.stop_threads, )
        self.buffer_cons: BufferConsumer = BufferConsumer(
            frame_buffer,
            frame_buff_lock,
            args=args,
            callback=self.__trigger_callback,
            debug=self.debug)
        self.buffer_prod: BufferProducer = BufferProducer(
            frame_buffer,
            frame_buff_lock,
            args=args,
            debug=self.debug,
        )

        self.buffer_cons.start()
        self.buffer_prod.start()

    def __exit_callback(self) -> None:
        self.stop_threads = True

    def __trigger_callback(self, prediction: Prediction) -> None:
        if self.debug:
            print('Predicted value found, we got %s with probability %f!' %
                  (prediction.label, prediction.probability))

        # Ignore prediction, unless it's the next logical increment
        # TODO: this could result in a deadlock, add a retry count, so
        #       if the counter gets out of sync, we can recover
        if prediction.label == self.spatula_count + 1:
            self.spatula_count += 1
        else:
            return

        if self.route[0]["spatula"] == self.spatula_count:
            self.livesplit.split()
            self.route.pop(0)


if __name__ == '__main__':
    autosplit = AutoSplit()
