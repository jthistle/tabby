from util.logger import logger
from .action import Action, ActionMod, UserCmd

ALIASES = {
    Action.QUIT: ["q", "quit"],
    Action.SAVE_QUIT: ["wq"],
    Action.SAVE: ["w", "write", "save"],
    Action.HELP: ["h", "help"],
    Action.SET_TUNING: ["t", "tuning"],
    Action.UNDO: ["u", "undo"],
    Action.REDO: ["r", "redo"],
    Action.OPEN: ["o", "open", "read"],
    Action.READ_PLAINTEXT: ["op", "rp", "openplain", "readplain"],
    Action.LIST: ["l", "list"],
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
            return UserCmd(action, parts, modifier)
    return None

