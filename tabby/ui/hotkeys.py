
from lib.element import ElementType
from .action import Action, UserCmd
from .mode import Mode

class ActionHotkeyLink:
    def __init__(self, action, keys, modes, selections = None):
        self.keys = keys
        self.modes = modes
        self.action = action
        self.selections = selections or [ElementType.ANY]


ACTION_HOTKEY_MAP = [
    ActionHotkeyLink(Action.UNDO, ["z"], [Mode.VIEW]),
    ActionHotkeyLink(Action.REDO, ["Z"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CURSOR_MOVE_LEFT, ["KEY_LEFT"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CURSOR_MOVE_RIGHT, ["KEY_RIGHT"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CURSOR_MOVE_LEFT, ["KEY_LEFT"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_RIGHT, ["KEY_RIGHT"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_POSITION_RIGHT, ["KEY_RIGHT"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.CURSOR_MOVE_POSITION_LEFT, ["KEY_LEFT"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.CURSOR_MOVE_BIG_RIGHT, ["kRIT5"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CURSOR_MOVE_BIG_LEFT, ["kLFT5"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CURSOR_MOVE_BIG_RIGHT, ["kRIT5"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_BIG_LEFT, ["kLFT5"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_POSITION_BIG_RIGHT, ["kRIT5"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.CURSOR_MOVE_POSITION_BIG_LEFT, ["kLFT5"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.CURSOR_MOVE_TWO_RIGHT, [" "], [Mode.VIEW, Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_UP_STRING, ["KEY_UP"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CURSOR_MOVE_DOWN_STRING, ["KEY_DOWN"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.MODE_EDIT, ["e"], [Mode.VIEW]),
    ActionHotkeyLink(Action.MODE_HELP, ["h"], [Mode.VIEW]),
    ActionHotkeyLink(Action.BEGIN_CMD, [":"], [Mode.VIEW, Mode.HELP]),
    ActionHotkeyLink(Action.COPY, ["c"], [Mode.VIEW]),
    ActionHotkeyLink(Action.CUT, ["x"], [Mode.VIEW]),
    ActionHotkeyLink(Action.PASTE, ["v"], [Mode.VIEW]),
    ActionHotkeyLink(Action.BAR_GROW, ["+"], [Mode.VIEW], [ElementType.CHORD]),
    ActionHotkeyLink(Action.BAR_SHRINK, ["-"], [Mode.VIEW], [ElementType.CHORD]),
    ActionHotkeyLink(Action.NOTE_DELETE_LAST, ["KEY_BACKSPACE"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.DUPLICATE_NOTE_UP, ["KEY_SR"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.DUPLICATE_NOTE_DOWN, ["KEY_SF"], [Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.REMOVE_CHORD, ["kDC5"], [Mode.VIEW, Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.INSERT_CHORD, ["\x00"], [Mode.VIEW, Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.CLEAR_CHORD, ["KEY_DC"], [Mode.VIEW, Mode.EDIT], [ElementType.CHORD]),
    ActionHotkeyLink(Action.TEXT_BACKSPACE, ["KEY_BACKSPACE"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.TEXT_DELETE, ["KEY_DC"], [Mode.EDIT], [ElementType.TEXT]),
    ActionHotkeyLink(Action.ADD_TEXT, ["T"], [Mode.VIEW]),
    ActionHotkeyLink(Action.REMOVE_TEXT, ["kDC5"], [Mode.VIEW], [ElementType.TEXT]),
    ActionHotkeyLink(Action.ADD_BAR, ["B"], [Mode.VIEW]),
    ActionHotkeyLink(Action.REMOVE_BAR, ["kDC6"], [Mode.VIEW], [ElementType.CHORD]),
]


def key_to_action(key, mode, selected_type):
    for link in ACTION_HOTKEY_MAP:
        if key in link.keys and mode in link.modes \
          and (ElementType.ANY in link.selections or selected_type in link.selections or selected_type == ElementType.ANY):
            return UserCmd(link.action)

    return None
