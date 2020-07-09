from enum import Enum
from .logger import logger

class Action(Enum):
    QUIT = 1
    SAVE_QUIT = 2
    SAVE = 3
    HELP = 4


class ActionMod(Enum):
    NONE = 1
    FORCE = 2


ALIASES = {
    Action.QUIT: ["q", "quit"],
    Action.SAVE_QUIT: ["wq"],
    Action.SAVE: ["w", "write", "s", "save"],
    Action.HELP: ["h", "help"],
}


HELP_STRINGS = {
    Action.QUIT: "{}: quit tab editor",
    Action.SAVE_QUIT: "{}: quit tab editor, saving any unsaved changes",
    Action.SAVE: "{}: save any unsaved changes",
    Action.HELP: "{} [command]: get help with the usage of a command",
}


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


def get_help(cmd_str):
    for action in ALIASES:
        if cmd_str in ALIASES[action]:
            return HELP_STRINGS[action]

    return None
