
from enum import Enum

class Action(Enum):
    QUIT = 1
    SAVE_QUIT = 2
    SAVE = 3
    HELP = 4
    SET_TUNING = 5
    UNDO = 6
    REDO = 7
    OPEN = 8
    CURSOR_MOVE_LEFT = 9
    CURSOR_MOVE_RIGHT = 10
    CURSOR_MOVE_BIG_LEFT = 11
    CURSOR_MOVE_BIG_RIGHT = 12
    CURSOR_MOVE_TWO_RIGHT = 13
    REMOVE_CHORD = 14
    CLEAR_CHORD = 15
    INSERT_CHORD = 16
    MODE_EDIT = 17
    MODE_VIEW = 18
    MODE_HELP = 19
    BEGIN_CMD = 20
    COPY = 21
    CUT = 22
    PASTE = 23
    BAR_GROW = 24
    BAR_SHRINK = 25
    CURSOR_MOVE_UP_STRING = 26
    CURSOR_MOVE_DOWN_STRING = 27
    NOTE_DELETE_LAST = 28
    DUPLICATE_NOTE_UP = 29
    DUPLICATE_NOTE_DOWN = 30
    CURSOR_MOVE_POSITION_RIGHT = 31
    CURSOR_MOVE_POSITION_LEFT = 32
    TEXT_BACKSPACE = 33
    TEXT_DELETE = 34
    CURSOR_MOVE_POSITION_BIG_RIGHT = 35
    CURSOR_MOVE_POSITION_BIG_LEFT = 36
    ADD_TEXT = 37
    REMOVE_TEXT = 38
    ADD_BAR = 39
    REMOVE_BAR = 40



class ActionMod(Enum):
    NONE = 1
    FORCE = 2


class UserCmd:
    def __init__(self, action, parts = None, modifier = ActionMod.NONE):
        self.action = action
        self.parts = parts
        self.modifier = modifier
