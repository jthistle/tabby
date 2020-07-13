
import subprocess
from meta.info import NAME, VERSION, DEV_URL
from .cmd_parser import Action, ALIASES, action_from_alias

def get_revision():
    try:
        # File that should be created at distribution time
        from meta.revision import REVISION
    except ImportError:
        rev = subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8")
        return rev
    else:
        return REVISION


def get_version():
    return VERSION


HELP_STR = """
=== {name} {version} ===
Revision {rev}

= Keys to change modes while in view mode:

e - enter edit mode
h - display this help message

== Mode-specific bindings

= ALL modes:

esc - back to view mode

= view mode (default):

:                - open console
esc              - exit console
c                - copy selected chord
v                - paste selected chord
z                - undo
shift + z        - redo
ctrl + backspace - clear selected chord
ctrl + delete    - remove selected chord
+                - double bar length
-                - halve bar length

= edit mode:

arrow keys        - move cursor
ctrl + arrow keys - move cursor in large steps
delete            - clear selected note
ctrl + delete     - clear selected chord

---

{name} is by James Thistlewood and is licensed under the GPL-v3.
Development at {url}.
""".format(name=NAME, version=VERSION, rev=get_revision(), url=DEV_URL)


ACTION_HELP_FORMAT = """
=== {name} {version}: manual ===

aliases:
    {aliases}

usage:
    {usages}

description:
    {desc}
"""

ACTION_HELP_PAGES = {
    Action.QUIT: {
        "usages": ":{cmd}[!]",
        "desc": "Quit {name}. Append `!` to force quit even if there are unsaved changes."
    },
    Action.SAVE_QUIT: {
        "usages": ":{cmd}[!]",
        "desc": "Quit {name}, saving any unsaved changes. Append `!` to force quit even if saving fails."
    },
    Action.SAVE: {
        "usages": ":{cmd}",
        "desc": "Save any unsaved changes."
    },
    Action.HELP: {
        "usages": ":{cmd} [command]",
        "desc": "Get help with the usage of a command. If no command provided, show the main help screen."
    },
    Action.SET_TUNING: {
        "usages": [
            ":{cmd} <string 1> [string 2] [string 3] ...",
            ":{cmd} <tuning name>"
        ],
        "desc": """Set the tuning of the tab. If strings are provided, set the tuning as the string names, with string 1
    being the bottom string. Strings can be max 2 characters long.

    If instead a tuning name is provided, the tuning will be set based on that. Valid tunings:
        - standard, std:    standard tuning
        - bass:             standard bass tuning
        - dropd:            guitar drop-D tuning
        - eflat:            guitar Eb tuning (each string down a semitone)

    If changing the tuning will decrease the number of strings and cause notes to be deleted, a warning will be shown."""
    },
    Action.UNDO: {
        "usages": ":{cmd}",
        "desc": "Undo the last undoable action."
    },
    Action.REDO: {
        "usages": ":{cmd}",
        "desc": "Redo the last undoable action."
    },
}

for action in ACTION_HELP_PAGES:
    if type(ACTION_HELP_PAGES[action]["usages"]) == list:
        ACTION_HELP_PAGES[action]["usages"] = "\n    ".join(ACTION_HELP_PAGES[action]["usages"])


def get_help(cmd_str = None):
    if cmd_str is None:
        return HELP_STR
    else:
        action = action_from_alias(cmd_str)
        if action is None:
            return None
        return ACTION_HELP_FORMAT.format(name=NAME, version=VERSION, aliases=", ".join(ALIASES[action]), **ACTION_HELP_PAGES[action]).format(name=NAME, cmd=ALIASES[action][0])
