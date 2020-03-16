from typing import List, Optional

from image.frame import SpongeFrame


class FrameBuffer():
    def __init__(self) -> None:
        self.paused: bool = False
        self.frame_buffer: List[SpongeFrame] = []

    def add_frame(self, frame: SpongeFrame) -> None:
        if not self.paused:
            self.frame_buffer.append(frame)

    def clear(self) -> None:
        self.frame_buffer.clear()

    def length(self) -> int:
        return len(self.frame_buffer)

    def pause_buffer(self):
        self.paused = True

    def is_paused(self) -> bool:
        return self.paused

    def pop(self) -> SpongeFrame:
        return self.frame_buffer.pop()

    def resume_buffer(self) -> None:
        self.paused = False
