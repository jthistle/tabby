from enum import Enum
from util.logger import logger

class Action(Enum):
    QUIT = 1
    SAVE_QUIT = 2
    SAVE = 3
    HELP = 4
    SET_TUNING = 5
    UNDO = 6
    REDO = 7
    OPEN = 8


class ActionMod(Enum):
    NONE = 1
    FORCE = 2


ALIASES = {
    Action.QUIT: ["q", "quit"],
    Action.SAVE_QUIT: ["wq"],
    Action.SAVE: ["w", "write", "save"],
    Action.HELP: ["h", "help"],
    Action.SET_TUNING: ["t", "tuning"],
    Action.UNDO: ["u", "undo"],
    Action.REDO: ["r", "redo"],
    Action.OPEN: ["o", "open", "read"]
}


def action_from_alias(alias):
    for action in ALIASES:
        if alias in ALIASES[action]:
            return action
    return None


def parse_cmd(cmd):
    parts = [x for x in cmd.split(" ") if x != ""]
    modifier = ActionMod.NONE
    if parts[0][-1] == "!":
        modifier = ActionMod.FORCE
        parts[0] = parts[0][:-1]

    cmd = parts[0]
    for action in ALIASES:
        if cmd in ALIASES[action]:
            return {
                "action": action,
                "modifier": modifier,
                "parts": parts
            }
    return None

