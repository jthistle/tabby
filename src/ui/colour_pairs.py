from enum import Enum
import curses

class Pair(Enum):
    WHITE_RED = 1

pairs = {
    Pair.WHITE_RED: (curses.COLOR_WHITE, curses.COLOR_RED),
}

def init_pairs():
    for pair in pairs:
        curses.init_pair(pair.value, pairs[pair][0], pairs[pair][1])
