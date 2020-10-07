from typing import NamedTuple


class color(NamedTuple):
    red: int
    green: int
    blue: int

    @property
    def rgb(self):
        return (self.blue, self.green, self.red)


RED = color(255, 26, 26)
GREEN = color(0, 255, 128)
BLUE = color(0, 128, 255)
