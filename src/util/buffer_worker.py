from threading import Thread, Lock
from time import sleep

from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer
from image.frame_hash import FrameHash
from util.video.webcam import Webcam


class BufferConsumer(Thread):
    exit_flag = False

    def __init__(self, frame_buffer: FrameBuffer, lock: Lock) -> None:
        self.lock = lock
        self.frame_buffer = frame_buffer
        self.frame_hash = FrameHash()
        super(BufferConsumer, self).__init__(target=self.__run)

    def __run(self, consumer: bool = False) -> None:
        while True:
            if self.exit_flag:
                break

            self.lock.acquire()
            try:
                if self.frame_buffer.length() > 0:
                    sponge_frame = self.frame_buffer.pop()
            finally:
                self.lock.release()

    def exit(self):
        self.exit_flag = True


class BufferProducer(Thread):
    exit_flag = False

    def __init__(self, webcam: Webcam, frame_buffer: FrameBuffer,
                 lock: Lock) -> None:
        self.lock = lock
        self.frame_buffer = frame_buffer
        self.webcam = webcam
        super(BufferProducer, self).__init__(target=self.__run)

    def __run(self, consumer: bool = False) -> None:
        while True:
            if self.exit_flag:
                break

            frame = self.webcam.get_frame()
            if frame is not None:
                sponge_frame = SpongeFrame(frame)

                self.lock.acquire()
                try:
                    self.frame_buffer.add_frame(sponge_frame)
                finally:
                    self.lock.release()

            # TODO: This line is definitely not ideal, things could get out of sync,
            # and can't guarantee duplicate frames or skipped frames, but should
            # be close enough for this use case for now.
            sleep(0.015)  # sleep for about a frame

    def exit(self):
        self.exit_flag = True
