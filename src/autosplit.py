from pynput.keyboard import KeyCode
from threading import Thread, Lock
from typing import List

from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer
from util.buffer_worker import BufferConsumer, BufferProducer
from util.keyboard.trigger_listener import TriggerListener
from util.video.webcam import Webcam

DEBUG = 1


class AutoSplit():
    frame_list: List[SpongeFrame] = []

    def __init__(self) -> None:
        self.__start_listener()
        self.__start_webcam()
        self.__start_buffers()

        self.thread_webcam.join()
        self.buffer_cons.join()
        self.buffer_prod.join()
        self.trigger_listener.join()

    def __start_webcam(self):
        self.thread_webcam: Webcam = Webcam(input=0, debug=DEBUG)
        self.thread_webcam.start()

    def __start_listener(self):
        self.trigger_listener = TriggerListener(KeyCode.from_char('\\'),
                                                self.__trigger_callback,
                                                self.__exit_callback)
        self.trigger_listener.start()

    def __start_buffers(self):
        frame_buffer: FrameBuffer = FrameBuffer(self.frame_list)
        frame_buff_lock = Lock()

        self.buffer_cons: BufferConsumer = BufferConsumer(
            frame_buffer, frame_buff_lock)
        self.buffer_prod: BufferProducer = BufferProducer(
            self.thread_webcam, frame_buffer, frame_buff_lock)

        self.buffer_cons.start()
        self.buffer_prod.start()

    def __exit_callback(self):
        self.thread_webcam.exit()
        self.buffer_cons.exit()
        self.buffer_prod.exit()

    def __trigger_callback(self):
        print('Trigger Callback')


if __name__ == '__main__':
    autosplit = AutoSplit()
