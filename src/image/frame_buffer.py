from typing import List, Optional

from image.frame import SpongeFrame


class FrameBuffer():

    def __init__(self, frame_buffer: List[SpongeFrame]) -> None:
        self.frame_buffer = frame_buffer

    def add_frame(self, frame: SpongeFrame) -> None:
        self.frame_buffer.append(frame)
        print(len(self.frame_buffer))

    def length(self) -> int:
        return len(self.frame_buffer)

    def pop(self) -> SpongeFrame:
        return self.frame_buffer.pop()
