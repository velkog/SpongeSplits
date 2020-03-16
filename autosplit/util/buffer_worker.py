from threading import Thread, Lock
from time import sleep
from typing import Callable

from common.video.webcam import Webcam
from image.diglet.model import CnnModel, Prediction
from image.diglet.frame_processor import FrameSet
from image.frame import SpongeFrame
from image.frame_buffer import FrameBuffer


class BufferWorker(Thread):
    EXIT_FLAG = False
    PAUSE_DURATION = 2

    def __init__(self, target, args):
        super(BufferWorker, self).__init__(target=target, args=args)

    def sleep(self):
        sleep(self.PAUSE_DURATION)


class BufferConsumer(BufferWorker):
    exit_flag = False

    def __init__(self,
                 frame_buffer: FrameBuffer,
                 lock: Lock,
                 args: tuple,
                 callback: Callable[[Prediction], None],
                 debug: bool = False) -> None:
        self.callback = callback
        self.debug = debug
        self.frame_buffer = frame_buffer
        self.lock = lock

        image_set = FrameSet()
        self.model = CnnModel(image_set.get_num_classes())
        self.model.compile_model()
        self.model.fit_model(image_set)

        super(BufferConsumer, self).__init__(target=self.__run, args=args)

    def __run(self, exit_flag) -> None:
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
                    continue
                self.callback(prediction)
                self.frame_buffer.clear()
                self.frame_buffer.pause_buffer()
                if self.debug:
                    print('Consumer Sleeping...')
                self.sleep()
                if self.debug:
                    print('Consumer Woke Up!')


class BufferProducer(BufferWorker):
    exit_flag = False

    def __init__(self,
                 frame_buffer: FrameBuffer,
                 lock: Lock,
                 args,
                 debug: bool = False) -> None:
        self.debug = debug
        self.frame_buffer = frame_buffer
        self.lock = lock
        self.webcam = Webcam(input=0, args=args, debug=debug)
        super(BufferProducer, self).__init__(target=self.__run, args=args)

    def __run(self, exit_flag) -> None:
        self.webcam.start()

        while True:
            if exit_flag():
                break

            frame = self.webcam.get_frame()
            if frame is not None:
                sponge_frame = SpongeFrame(frame)

                self.lock.acquire()
                try:
                    if self.frame_buffer.is_paused():
                        self.frame_buffer.clear()
                        self.frame_buffer.resume_buffer()
                        if self.debug:
                            print('Producer Sleeping...')
                        self.sleep()
                        if self.debug:
                            print('Producer Woke Up!')
                    else:
                        self.frame_buffer.add_frame(sponge_frame)
                finally:
                    self.lock.release()

            # TODO: This line is definitely not ideal, things could get out of sync,
            # and can't guarantee duplicate/skipped frames, but should be
            # close enough for this use case for now.
            # 0.015 is roughly the right number
            sleep(0.01)  # sleep for about a frame's length

    def exit(self):
        self.exit_flag = True
