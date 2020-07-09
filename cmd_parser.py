from enum import Enum
from logger import logger

class Action(Enum):
    QUIT = 1
    SAVE_QUIT = 2
    SAVE = 3


class ActionMod(Enum):
    NONE = 1
    FORCE = 2


ALIASES = {
    Action.QUIT: ["q", "quit"],
    Action.SAVE_QUIT: ["wq"],
    Action.SAVE: ["w", "write", "save"],
}


def parse_cmd(cmd):
    parts = [x for x in cmd.split(" ") if x != ""]
    modifier = ActionMod.NONE
    if parts[0][-1] == "!":
        modifier = ActionMod.FORCE
        parts[0] = parts[:-1]

    cmd = parts[0]
    for action in ALIASES:
        if cmd in ALIASES[action]:
            return {
                "action": action,
                "modifier": modifier
            }
    return None
