from enum import Enum
import curses

class Pair(Enum):
    WHITE_RED = 1
    HIGHLIGHT_DIM = 2
    HIGHLIGHT_MAIN = 3

pairs = {
    Pair.WHITE_RED: (curses.COLOR_WHITE, curses.COLOR_RED),
    Pair.HIGHLIGHT_DIM: (curses.COLOR_BLACK, curses.COLOR_CYAN),
    Pair.HIGHLIGHT_MAIN: (curses.COLOR_BLACK, curses.COLOR_WHITE),
}

def init_pairs():
    for pair in pairs:
        curses.init_pair(pair.value, pairs[pair][0], pairs[pair][1])
