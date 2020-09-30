
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
===== {name} {version} =====
Revision {rev}

== Essential ==

Move this page up and down with  up arrow  and  down arrow   .

== Note on console ==

You can access the console by typing  :  . To list commands that can be used at
the console, type  :list<ENTER>  .

== Modes ==

Tabby works using a 'mode' system.

View mode is the default mode.
In Edit mode you can edit the individual notes of a tab, as well as text and annotations.
In Help mode you can see this message and help for various commands.

Keybindings for when you are in view mode:

e - enter Edit mode
h - display this help message

== Mode-specific bindings ==

= ALL modes =

esc - return to View mode

= View mode AND Edit mode =

arrow keys        - move cursor
space             - move cursor forward two steps
ctrl + arrow keys - move cursor in large steps
delete            - clear selected chord
delete            - remove selected text
ctrl + delete     - remove selected chord
ctrl + space      - insert chord after selected chord
ctrl + up/dn arrow - move the viewport up or down

= View mode =

:                 - open console
esc               - exit console
c                 - copy selected chord
x                 - cut selected chord
v                 - paste selected chord
z                 - undo
shift + z         - redo
+                 - double bar length
-                 - halve bar length
shift + t         - add text
shift + b         - insert bar
ctrl + shift + delete  - delete bar

= Edit mode =

(type)             - enter note value
up and down arrows - change note selection
backspace          - delete last character entered

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
        "shortdesc": "Quit Tabby.",
        "desc": "Quit {name}. Append `!` to force quit even if there are unsaved changes."
    },
    Action.SAVE_QUIT: {
        "usages": ":{cmd}[!] [file path]",
        "shortdesc": "Quit Tabby, saving any unsaved changes.",
        "desc": "Quit {name}, saving any unsaved changes. Append `!` to force quit even if saving fails."
    },
    Action.SAVE: {
        "usages": ":{cmd} [file path]",
        "desc": "Save any unsaved changes."
    },
    Action.OPEN: {
        "usages": ":{cmd} <file path>",
        "desc": "Open the {name} file located at file path."
    },
    Action.READ_PLAINTEXT: {
        "usages": ":{cmd} <file path>",
        "shortdesc": "Attempt to read a plain text tab file into Tabby.",
        "desc": """Open the plain text file located at the path and try to read it into Tabby.
    Warning: badly formatted tabs will not be read correctly and at worst will not be read at all.
"""
    },
    Action.HELP: {
        "usages": ":{cmd} [command]",
        "shortdesc": "Get help with the usage of a command.",
        "desc": "Get help with the usage of a command. If no command provided, show the main help screen."
    },
    Action.SET_TUNING: {
        "usages": [
            ":{cmd} <string 1> [string 2] [string 3] ...",
            ":{cmd} <tuning name>"
        ],
        "shortdesc":  "Set the tuning of the tab.",
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
    Action.LIST: {
        "usages": ":{cmd}",
        "desc": "List all different commands."
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


def get_cmd_list():
    acc = "\n=== Tabby {version}: commands ===\n\n".format(version=VERSION)

    for action in ACTION_HELP_PAGES:
        short = ACTION_HELP_PAGES[action].get("shortdesc") or ACTION_HELP_PAGES[action].get("desc")
        acc += ", ".join([":" + x for x in ALIASES[action]]) + "  -  " + short + "\n\n"

    return acc
