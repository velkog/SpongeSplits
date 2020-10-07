from curses import color_pair, endwin, initscr
import curses  # TODO: get rid of package import
from time import time
from datetime import datetime
from typing import List

from image.diglet.model import Prediction


class InformationDisplay:
    _TITLE = "  Velkog's BfBB Autosplitter  "
    _P_TITLE = "Prediction"
    _P_H = 10
    _P_W = 50

    class _Log:
        def __init__(self, log: str):
            self.timestamp = datetime.fromtimestamp(
                time()).strftime("%H:%M:%S.%f")[:-3]
            self.log = log

    def __init__(self):
        self.spat_label = None
        self.spat_prob = None
        self.sock_label = None
        self.sock_prob = None
        self._logs: List[_Log] = []

    def _init_logs(self) -> None:
        self.logsscr.erase()
        self.logsscr.addstr(1, 2, "Logs:")
        self.logsscr.border()

        for i, log in enumerate(self._logs):
            self.logsscr.addstr(3 + i, 2, f"[{log.timestamp}]\t{log.log}")

        self._refresh()

    def start(self):
        # Initialize Screen
        self.stdscr = initscr()
        curses.curs_set(0)

        # Create Window Border
        self.stdscr.border()

        # Create title
        self.title = curses.newwin(3,
                                   len(self._TITLE) + 2, 0,
                                   curses.COLS // 2 - len(self._TITLE) // 2)
        self.title.border()
        self.title.addstr(1, 1, self._TITLE)
        self.stdscr.addstr(2, 1, "-" * (curses.COLS - 2))

        self.prediction = curses.newwin(self._P_H, self._P_W, 4, 2)
        self.logsscr = curses.newwin(10, curses.COLS, curses.LINES - 10, 0)

        self.set_prediction()
        self._init_logs()

        # Refreshing
        self._refresh()

    def _refresh(self):
        self.stdscr.refresh()
        self.title.refresh()
        self.prediction.refresh()
        self.logsscr.refresh()

    def clean(self):
        endwin()

    def log(self, log: str):
        self._logs.append(self._Log(log))
        if len(self._logs) >= 6:
            self._logs = self._logs[-6:]
        self._init_logs()

    def set_prediction(self,
                       spatula_prediction: Prediction = None,
                       sock_prediction: Prediction = None) -> None:
        if spatula_prediction:
            self.spat_label = spatula_prediction.label
            self.spat_prob = spatula_prediction.probability
        if sock_prediction:
            self.sock_label = sock_prediction.label
            self.sock_prob = sock_prediction.probability

        self.prediction.erase()

        # Title
        self.prediction.addstr(0, self._P_W // 2 - len(self._P_TITLE) // 2,
                               self._P_TITLE)

        # Spatula
        self.prediction.addstr(1, 5, "Predicted spatula value:")
        self.prediction.addstr(
            1, 35,
            str(self.spat_label) if self.spat_label else "None")
        self.prediction.addstr(2, 5, "Prediction confidence:")
        self.prediction.addstr(
            2, 35,
            str(self.spat_prob)[0:7] + "%" if self.spat_prob else "None")

        # SockS
        self.prediction.addstr(4, 5, "Predicted sock value:")
        self.prediction.addstr(
            4, 35,
            str(self.sock_label) if self.sock_label else "None")
        self.prediction.addstr(5, 5, "Prediction confidence:")
        self.prediction.addstr(
            5, 35,
            str(self.sock_prob)[0:7] + "%" if self.sock_prob else "None")

        self._refresh()
