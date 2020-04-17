from enum import auto, Enum
from threading import Thread, Lock
from time import sleep
from typing import Callable

from common.video.webcam import Webcam
from config import Identity
from image.diglet.model import CnnModel, Prediction
from image.diglet.frame_processor import FrameSet
from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer


class BufferWorker(Thread):
    class FrameLength(Enum):
        FRAME = 0.015
        HALF_FRAME = FRAME / 2
        QUARTER_FRAME = FRAME / 4

        def __init__(self, frame_length: float):
            self.frame_length = frame_length

        @property
        def time(self):
            return self.frame_length

    def __init__(self, target, args):
        super(BufferWorker, self).__init__(target=target, args=args)

    def sleep(self, frame_length: FrameLength = FrameLength.FRAME):
        sleep(frame_length.time)


class BufferConsumer(BufferWorker):
    exit_flag = False

    def __init__(
            self,
            args: tuple,
            callback: Callable[[Prediction], None],
            frame_buffer: FrameBuffer,
            lock: Lock,
            webcam: Webcam,
            debug: bool = False,
    ) -> None:
        self.callback = callback
        self.debug = debug
        self.frame_buffer = frame_buffer
        self.ipc_value = Identity.ALL
        self.lock = lock
        self.webcam = webcam

        image_set = FrameSet()
        self.model = CnnModel(image_set.get_num_classes())
        self.model.compile_model()
        self.model.fit_model(image_set)

        super(BufferConsumer, self).__init__(target=self.__run, args=args)

    def __run(self, exit_flag) -> None:
        # TODO: look into sleep while buffer is empty
        while True:
            if exit_flag():
                break

            self.lock.acquire()
            sponge_frame = None
            try:
                if self.frame_buffer.length() > 0:
                    sponge_frame = self.frame_buffer.pop()
            finally:
                self.lock.release()

            if sponge_frame is not None:
                prediction = self.model.predict(sponge_frame)
                if prediction.label is None or prediction.probability < 95:
                    self.webcam.set_states([Identity.NONE])
                    continue
                self.webcam.set_states([Identity.SPATULA])
                self.callback(prediction)
                self.frame_buffer.clear()

            self.sleep(BufferWorker.FrameLength.QUARTER_FRAME)

    @property
    def ipc(self) -> Identity:
        return self.ipc_value


class BufferProducer(BufferWorker):
    exit_flag = False

    def __init__(
            self,
            args: tuple,
            frame_buffer: FrameBuffer,
            lock: Lock,
            webcam: Webcam,
            debug: bool = False,
    ) -> None:
        self.debug = debug
        self.frame_buffer = frame_buffer
        self.lock = lock
        self.webcam = webcam
        super(BufferProducer, self).__init__(target=self.__run, args=args)

    def __run(self, exit_flag) -> None:
        while True:
            if exit_flag():
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
            # and can't guarantee duplicate/skipped frames, but should be
            # close enough for this use case for now.
            # 0.015 is roughly the right number
            self.sleep()

    def exit(self):
        self.exit_flag = True
