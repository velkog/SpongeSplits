from threading import Thread
from time import sleep, time
from typing import Callable

from common.video.webcam import Webcam
from config import Identity
from image.diglet.model import CnnModel, Prediction
from image.diglet.frame_processor import FrameSet
from image.frame import SpongeFrame
from util.display import InformationDisplay


class FrameProcessor(Thread):
    __FRAME_LENGTH = 0.01666666666

    def __init__(
            self,
            args: tuple,
            callback: Callable[[Prediction], None],
            display: InformationDisplay,
            webcam: Webcam,
    ) -> None:
        self.callback = callback
        self.display = display
        self.webcam = webcam

        image_set = FrameSet()
        self.model = CnnModel(image_set.get_num_classes())
        self.model.compile_model()
        self.model.fit_model(image_set)

        super(FrameProcessor, self).__init__(target=self.__run, args=args)

    def __start_processing(self) -> None:
        self.__process_start_time = time()

    def __finish_processing(self) -> None:
        processing_time = time() - self.__process_start_time
        sleep_time = self.__FRAME_LENGTH - processing_time
        if sleep_time < 0:
            self.display.log(
                f"Frame lag of '{sleep_time/-self.__FRAME_LENGTH*100.0}%'")
        else:
            sleep(sleep_time)

    def __run(self, exit_flag: Callable[[], bool]) -> None:
        while True:
            if exit_flag():
                break

            self.__start_processing()
            frame = self.webcam.get_frame()
            if frame is not None:
                sponge_frame = SpongeFrame(frame)
                spatula_prediction = self.model.predict(sponge_frame)
                # TODO: maybe move this threshold into a config value
                empty = True
                identity_states = []
                if spatula_prediction.label is not None and spatula_prediction.probability >= 95:
                    empty = False
                    identity_states.append(Identity.SPATULA)
                if empty:
                    identity_states.append(Identity.NONE)
                self.webcam.set_states(identity_states)
                self.callback(spatula_prediction)
            self.__finish_processing()
