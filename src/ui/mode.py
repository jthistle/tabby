
from enum import Enum

class Mode(Enum):
    VIEW = 1
    EDIT = 2
    HELP = 3

MODE_NAMES = {
    Mode.VIEW: "VIEW",
    Mode.EDIT: "EDIT",
    Mode.HELP: "HELP"
}

def mode_name(mode):
    return MODE_NAMES[mode]
