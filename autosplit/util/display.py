from curses import color_pair, endwin, initscr
import curses # TODO: get rid of package import


from image.diglet.model import Prediction


class InformationDisplay:
    _TITLE = "  Velkog's BfBB Autosplitter  "
    _P_TITLE = "Prediction"
    _P_H = 4
    _P_W = 50

    def __init__(self):
        self.p_label = None
        self.p_prob = None

        self._initialize_screen()

    def _initialize_screen(self):
        # Initialize Screen
        self.stdscr = initscr()
        curses.curs_set(0)
        
        # Create Window Border
        self.stdscr.border()
        
        # Create title
        self.title = curses.newwin(3, len(self._TITLE) + 2, 0, curses.COLS // 2 - len(self._TITLE) // 2)
        self.title.border()
        self.title.addstr(1, 1, self._TITLE)
        self.stdscr.addstr(2, 1, "-" * (curses.COLS - 2))

        self.prediction = curses.newwin(self._P_H, self._P_W, 4, 2)
        # self.prediction.border()
        self.prediction.addstr(0, self._P_W // 2 - len(self._P_TITLE) // 2, self._P_TITLE)
        self.prediction.addstr(1, 5, "Predicted value:")
        self.prediction.addstr(1, 35, "None")
        self.prediction.addstr(2, 5, "Prediction confidence:")
        self.prediction.addstr(2, 35, "None")

        # Refreshing
        self._refresh()

    def _reinit(self):
        self.prediction.erase()
        self.prediction.addstr(0, self._P_W // 2 - len(self._P_TITLE) // 2, self._P_TITLE)
        self.prediction.addstr(1, 5, "Predicted value:")
        self.prediction.addstr(1, 35, "None" if self.p_label is None else str(self.p_label))
        self.prediction.addstr(2, 5, "Prediction confidence:")
        self.prediction.addstr(2, 35, "None" if self.p_prob is None else str(self.p_prob)[0:7] + "%")
        self._refresh()
        
    def _refresh(self):
        self.stdscr.refresh()
        self.title.refresh()
        self.prediction.refresh()

    def clean(self):
        endwin()

    def set_prediction(self, prediction: Prediction):
        self.p_label = prediction.label
        self.p_prob = prediction.probability
        self._reinit()
