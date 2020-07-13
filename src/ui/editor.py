import curses
import re

from .console import Console
from .header import Header
from .cmd_parser import parse_cmd, Action, ActionMod
from lib.tab import Tab
from util.logger import logger
from .colour_pairs import Pair
from .mode import Mode, mode_name
from .help import get_help

from lib.undo.cursor_state import CursorState
from lib.undo.set_note_value import UndoSetNoteValue
from lib.undo.duplicate_note import UndoDuplicateNote
from lib.undo.set_tuning import UndoSetTuning
from lib.undo.replace_chord import UndoReplaceChord
from lib.undo.clear_chord import UndoClearChord
from lib.undo.resize_bar import UndoResizeBar

ACCEPTED_NOTE_VALS = re.compile(r"[a-z0-9~/\\<>\^]", re.I)

class Editor:
    def __init__(self):
        self.header = Header()
        self.console = Console()
        self.win = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
        self.win.keypad(True)

        self.viewport_pos = 0       # vertically
        self.last_cursor_draw = []

        self.current_tab = Tab()

        self.mode = Mode.VIEW
        self.first_entry = True     # first entry after moving the cursor to this position
        self.current_help = ""
        self.clipboard = None

        # Initial update
        curses.curs_set(0)
        self.update()

    @property
    def cursor(self):
        return self.current_tab.cursor

    def do(self, action):
        self.current_tab.do(action)

    def help_update(self):
        self.win.clear()
        self.win.addstr(0, 0, self.current_help)
        self.draw()

    def update(self):
        if self.mode == Mode.HELP:
            self.help_update()
            return

        self.win.erase()
        tab = self.current_tab.layout()
        self.win.addstr(self.viewport_pos, 0, tab.txt)

        self.update_cursor(tab)
        self.draw()

    def update_cursor(self, tab = None):
        # TODO: re-layout-ing the entire tab for every cursor move probably isn't a good idea.
        # In the future, just work out a way of doing it without doing this.
        if not tab:
            tab = self.current_tab.layout()

        # Remove last highlighting if only updating cursor
        self.clear_cursor()

        # Process new cursor highlighting
        for pos in tab.highlighted:
            ch = self.win.inch(pos[0], pos[1])
            self.win.addch(pos[0], pos[1], ch, curses.color_pair(Pair.HIGHLIGHT_DIM.value) | curses.A_DIM)

        # Strong highlighting in EDIT mode only
        if self.mode == Mode.EDIT:
            for pos in tab.strong:
                ch = self.win.inch(pos[0], pos[1]) & curses.A_CHARTEXT
                self.win.addch(pos[0], pos[1], ch, curses.color_pair(Pair.HIGHLIGHT_MAIN.value))

        # Should be enough - we expect tab.strong to always be contained within tab.highlighted
        self.last_cursor_draw = tab.highlighted

    def clear_cursor(self):
        for pos in self.last_cursor_draw:
            # Bottom eight bits ignores formatting/colours
            ch = self.win.inch(pos[0], pos[1]) & curses.A_CHARTEXT
            self.win.addch(pos[0], pos[1], ch, 0)

    def change_mode(self, new_mode):
        old_mode = self.mode
        if new_mode == old_mode:
            return

        self.mode = new_mode
        if new_mode == Mode.EDIT:
            self.first_entry = True

        if old_mode in (Mode.EDIT, Mode.VIEW):
            self.update_cursor()

        if new_mode == Mode.VIEW:
            self.console.clear()
        else:
            self.console.echo("-- {} MODE --".format(mode_name(new_mode)))

        # Must be done last
        if old_mode == Mode.HELP or new_mode == Mode.HELP:
            self.update()

    def handle_cmd(self, raw_cmd):
        cmd = parse_cmd(raw_cmd)
        if not cmd:
            self.console.error("Invalid command!")
            return True

        action = cmd.get("action")
        if action == Action.HELP:
            if len(cmd.get("parts")) == 1:
                self.current_help = get_help()
            else:
                cmd_str = cmd.get("parts")[1]
                help_str = get_help(cmd_str)
                if help_str is None:
                    self.console.error("Command {} doesn't exist!".format(cmd_str))
                    return True
                self.current_help = help_str

            self.change_mode(Mode.HELP)
        elif action == Action.SAVE_QUIT:
            # TODO save
            return False
        elif action == Action.QUIT:
            return False
        elif action == Action.SET_TUNING:
            strings = [x.strip() for x in cmd.get("parts")[1:] if x.strip() != ""]
            if len(strings) == 0:
                self.console.error("Must specify at least one string for tuning!")
                return True

            if self.current_tab.tuning_causes_loss(strings):
                confirm = self.console.confirm("Setting this tuning will cause loss of data. Continue?")
                if not confirm:
                    return True

            self.do(UndoSetTuning(strings))
            self.update()
        elif action == Action.UNDO:
            self.undo()
        elif action == Action.REDO:
            self.redo()
        else:
            self.console.echo("Action: {}, Modifier: {}".format(cmd.get("action"), cmd.get("modifier")))

        return True

    def undo(self):
        res = self.current_tab.undo_stack.undo()
        if not res:
            self.console.error("Nothing to undo!")
        self.update()

    def redo(self):
        res = self.current_tab.undo_stack.redo()
        if not res:
            self.console.error("Nothing to redo!")
        self.update()

    def post_cursor_move(self):
        self.first_entry = True
        self.update_cursor(tab=None)
        self.draw()

    def clear_chord(self):
        state = CursorState(self.cursor)
        self.do(UndoClearChord(state))
        self.update()

    def handle_input(self):
        if self.console.in_cmd:
            res = self.console.handle_input()
            if res:
                return True
            elif self.console.current_cmd != "":
                cmd_res = self.handle_cmd(self.console.current_cmd)
                if not cmd_res:
                    return False

        key = self.win.getkey()
        if len(key) == 1 and ord(key) == 27:    # ESC, temp for debug
            self.change_mode(Mode.VIEW)
        elif key == "KEY_RIGHT" or key == "KEY_LEFT":
            direction = 1 if key == "KEY_RIGHT" else -1
            self.cursor.move(direction)
            self.post_cursor_move()
        elif key == "kRIT5" or key == "kLFT5":      # w/ ctrl mod
            direction = 1 if key == "kRIT5" else -1
            self.cursor.move_big(direction)
            self.post_cursor_move()
        elif key == " ":
            self.cursor.move(2)
            self.post_cursor_move()
        elif self.mode == Mode.VIEW:
            if key == "e":
                self.change_mode(Mode.EDIT)
            elif key == "h":
                self.current_help = get_help()
                self.change_mode(Mode.HELP)
            elif key == ":":
                self.console.begin_cmd()
            elif key == "c":
                self.clipboard = self.cursor.chord
            elif key == "v":
                if self.clipboard is None:
                    self.console.error("Nothing to paste!")
                else:
                    state = CursorState(self.cursor)
                    self.do(UndoReplaceChord(state, self.clipboard))
                    self.update()
            elif key == "z":
                self.undo()
            elif key == "Z":
                self.redo()
            elif key == "kDC5":
                self.clear_chord()
            elif key == "+":
                self.do(UndoResizeBar(CursorState(self.cursor), 2))
                self.update()
            elif key == "-":
                self.do(UndoResizeBar(CursorState(self.cursor), 1/2))
                self.update()

        elif self.mode == Mode.EDIT:
            if key == "KEY_UP" or key == "KEY_DOWN":
                direction = 1 if key == "KEY_UP" else -1
                self.cursor.move_string(direction)
                self.post_cursor_move()
            elif key == "KEY_DC":
                self.do(UndoSetNoteValue(CursorState(self.cursor), ""))
                self.update()
            elif key == "KEY_BACKSPACE":
                state = CursorState(self.cursor)
                new_val = self.cursor.note().value[:-1]
                self.do(UndoSetNoteValue(state, new_val))
                self.update()
                self.first_entry = False
            elif key == "kDC5":
                self.clear_chord()
            elif key == "KEY_SR" or key == "KEY_SF":
                direction = 1 if key == "KEY_SR" else -1
                state = CursorState(self.cursor)
                self.do(UndoDuplicateNote(state, direction))
                self.update()
            elif len(key) == 1 and ACCEPTED_NOTE_VALS.match(key):
                state = CursorState(self.cursor)
                value = self.cursor.note().value
                if self.first_entry:
                    value = key
                else:
                    value += key
                self.do(UndoSetNoteValue(state, value))
                self.update()
                self.first_entry = False

        # self.console.echo("Char: {}".format(repr(key)).replace("\n", "newline"))

        return True

    def draw(self):
        self.win.refresh()
