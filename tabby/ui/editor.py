import curses
import re
import json
import time
from os.path import expanduser, splitext
from threading import Thread, Lock

from .action import Action, ActionMod
from lib.tab import Tab
from lib.text import Text
from util.logger import logger
from .colour_pairs import Pair
from .mode import Mode, mode_name
from .const import FILE_EXTENSION
from .playback_manager import PlaybackManager
from lib.from_plaintext import from_plaintext

from lib.undo.cursor_state import CursorState
from lib.undo.cursor_state_text import CursorStateText
from lib.undo.cursor_state_generic import CursorStateGeneric
from lib.undo.set_note_value import UndoSetNoteValue
from lib.undo.duplicate_note import UndoDuplicateNote
from lib.undo.set_tuning import UndoSetTuning
from lib.undo.replace_chord import UndoReplaceChord
from lib.undo.clear_chord import UndoClearChord
from lib.undo.remove_chord import UndoRemoveChord
from lib.undo.insert_chord import UndoInsertChord
from lib.undo.resize_bar import UndoResizeBar
from lib.undo.insert_text_character import UndoInsertTextCharacter
from lib.undo.delete_char import UndoDeleteChar
from lib.undo.insert_text import UndoInsertText
from lib.undo.remove_text import UndoRemoveText
from lib.undo.insert_bar import UndoInsertBar
from lib.undo.remove_bar import UndoRemoveBar

# TODO ditch this?
ACCEPTED_NOTE_VALS = re.compile(r"[a-z0-9~/\\<>\^]", re.I)

class Editor:
    def __init__(self, parent, synth):
        self.parent = parent
        self.dimensions = (curses.LINES - 2, curses.COLS)
        self.win = curses.newwin(*self.dimensions, 1, 0)
        self.win.keypad(True)

        self.viewport_pos = 0       # vertically
        self.last_cursor_draw = []

        self.current_tab = Tab()

        self.first_entry = True     # first entry after moving the cursor to this position
        self.clipboard = None
        self.file_path = None
        self.__dirty = False

        self.playback_manager = PlaybackManager(synth)

        # Initial update
        curses.curs_set(0)
        self.update()

    @property
    def mode(self):
        return self.parent.mode

    @property
    def header(self):
        return self.parent.header

    @property
    def console(self):
        return self.parent.console

    @property
    def cursor(self):
        return self.current_tab.cursor

    @property
    def dirty(self):
        return self.__dirty

    @dirty.setter
    def dirty(self, val):
        self.__dirty = val
        self.header.dirty = val
        self.header.update()

    def do(self, action):
        self.current_tab.do(action)
        self.dirty = True

    def update(self, tab = None):
        self.win.erase()

        if tab is None:
            tab = self.current_tab.layout()

        lines = tab.txt.split("\n")[self.viewport_pos:self.viewport_pos + self.dimensions[0]]
        self.win.addstr(0, 0, "\n".join(lines))

        self.update_cursor(tab)
        self.draw()

    def update_cursor(self, tab = None):
        if tab is None:
            tab = self.current_tab.layout()

        # Remove last highlighting if only updating cursor
        self.clear_cursor()

        # Process new cursor highlighting
        for pos in tab.highlighted:
            draw_pos = (pos[0] - self.viewport_pos, pos[1])
            if draw_pos[0] >= self.dimensions[0]:
                continue
            ch = self.win.inch(*draw_pos)
            self.win.addch(*draw_pos, ch, curses.color_pair(Pair.HIGHLIGHT_DIM.value) | curses.A_DIM)
            self.last_cursor_draw.append(draw_pos)

        # Strong highlighting in EDIT mode only
        if self.mode == Mode.EDIT:
            for pos in tab.strong:
                draw_pos = (pos[0] - self.viewport_pos, pos[1])
                if draw_pos[0] >= self.dimensions[0]:
                    continue
                ch = self.win.inch(*draw_pos) & curses.A_CHARTEXT
                self.win.addch(*draw_pos, ch, curses.color_pair(Pair.HIGHLIGHT_MAIN.value))
                self.last_cursor_draw.append(draw_pos)

    def clear_cursor(self):
        for pos in self.last_cursor_draw:
            # Bottom eight bits ignores formatting/colours
            ch = self.win.inch(pos[0], pos[1]) & curses.A_CHARTEXT
            self.win.addch(pos[0], pos[1], ch, 0)

    def move_viewport_for_cursor(self, tab):
        """Also calls an update on the tab and the cursor."""
        min_h = self.dimensions[0] + self.viewport_pos
        max_h = 0
        for pos in tab.highlighted + tab.strong:
            min_h = min(min_h, pos[0])
            max_h = max(max_h, pos[0])

        if min_h < self.viewport_pos:
            self.viewport_pos = max(0, min_h - 1)
        elif max_h >= self.viewport_pos + self.dimensions[0]:
            self.viewport_pos = max_h - self.dimensions[0] + 1

        self.update(tab)

    def on_mode_change(self, old_mode, new_mode):
        if new_mode == Mode.EDIT:
            self.first_entry = True

        if old_mode in (Mode.EDIT, Mode.VIEW):
            self.update_cursor()

    def play_current(self):
        if not self.cursor.on_chord:
            return

        self.playback_manager.play_chord(self.cursor.element)

    def handle_cmd(self, user_cmd):
        """Handles both console commands and hotkey commands. For hotkey commands, `parts` is None.
            Returns False if the programme should exit, otherwise True."""
        action = user_cmd.action
        force = user_cmd.modifier == ActionMod.FORCE
        parts = user_cmd.parts

        if action == Action.SAVE or action == Action.SAVE_QUIT:
            path = None
            if len(parts) > 1:
                path = " ".join(parts[1:]).strip()
            res = self.save_current(path)
            if action == Action.SAVE_QUIT and (res or force):
                return False
            return True
        elif action == Action.OPEN:
            if len(parts) == 1:
                self.console.error("Must specify file location")
                return True

            path = " ".join(parts[1:]).strip()
            self.read(path)
        elif action == Action.READ_PLAINTEXT:
            if len(parts) == 1:
                self.console.error("Must specify file location")
                return True

            path = " ".join(parts[1:]).strip()
            self.read_plaintext(path)
        elif action == Action.QUIT:
            if self.dirty and not force:
                self.console.error("Tab has unsaved changes, append ! to force quit")
                return True
            return False
        elif action == Action.SET_TUNING:
            strings = [x.strip() for x in parts[1:] if x.strip() != ""]
            return self.set_tuning(strings)
        elif action == Action.UNDO:
            self.undo()
        elif action == Action.REDO:
            self.redo()
        elif action in (Action.CURSOR_MOVE_RIGHT, Action.CURSOR_MOVE_LEFT):
            direction = 1 if action == Action.CURSOR_MOVE_RIGHT else -1
            self.cursor.move(direction)
            self.post_cursor_move()
            self.play_current()
        elif action in (Action.CURSOR_MOVE_BIG_RIGHT, Action.CURSOR_MOVE_BIG_LEFT):
            direction = 1 if action == Action.CURSOR_MOVE_BIG_RIGHT else -1
            self.cursor.move_big(direction)
            self.post_cursor_move()
            self.play_current()
        elif action in (Action.CURSOR_MOVE_POSITION_BIG_RIGHT, Action.CURSOR_MOVE_POSITION_BIG_LEFT):
            direction = 1 if action == Action.CURSOR_MOVE_POSITION_BIG_RIGHT else -1
            self.cursor.move_position_big(direction)
            self.post_cursor_move()
        elif action == Action.CURSOR_MOVE_TWO_RIGHT:
            self.cursor.move(2)
            self.post_cursor_move()
            self.play_current()
        elif action in (Action.CURSOR_MOVE_UP_STRING, Action.CURSOR_MOVE_DOWN_STRING):
            direction = 1 if action == Action.CURSOR_MOVE_UP_STRING else -1
            self.cursor.move_position(direction)
            if not self.first_entry:
                self.play_current()
            self.post_cursor_move()
        elif action in (Action.CURSOR_MOVE_POSITION_RIGHT, Action.CURSOR_MOVE_POSITION_LEFT):
            direction = 1 if action == Action.CURSOR_MOVE_POSITION_RIGHT else -1
            self.cursor.move_position(direction)
            self.post_cursor_move()
        elif action == Action.NOTE_DELETE_LAST:
            state = CursorState(self.cursor)
            new_val = self.cursor.note.value[:-1]
            self.do(UndoSetNoteValue(state, new_val))
            self.update()
            self.first_entry = False
        elif action == Action.REMOVE_CHORD:
            self.remove_chord()
        elif action == Action.INSERT_CHORD:
            self.insert_chord()
        elif action == Action.CLEAR_CHORD:
            self.clear_chord()
        elif action == Action.COPY:
            self.clipboard = self.cursor.element.write()
        elif action == Action.CUT:
            self.clipboard = self.cursor.element.write()
            if self.cursor.on_chord:
                self.clear_chord()
            elif self.cursor.on_text:
                self.remove_text()
        elif action == Action.PASTE:
            self.paste()
        elif action == Action.BAR_GROW:
            if self.cursor.bar.can_change_size(2):
                self.do(UndoResizeBar(CursorState(self.cursor), 2))
                self.update()
        elif action == Action.BAR_SHRINK:
            self.shrink_bar()
        elif action in (Action.DUPLICATE_NOTE_UP, Action.DUPLICATE_NOTE_DOWN):
            direction = 1 if action == Action.DUPLICATE_NOTE_UP else -1
            state = CursorState(self.cursor)
            self.do(UndoDuplicateNote(state, direction))
            self.update()
            self.play_current()
        elif action == Action.TEXT_BACKSPACE:
            self.text_backspace()
        elif action == Action.TEXT_DELETE:
            self.text_delete()
        elif action == Action.ADD_TEXT:
            state = CursorStateGeneric(self.cursor)
            self.do(UndoInsertText(state, ""))
            self.cursor.element = self.current_tab.element(state.element)
            self.parent.change_mode(Mode.EDIT)
            self.update()
        elif action == Action.REMOVE_TEXT:
            self.remove_text()
        elif action == Action.ADD_BAR:
            state = CursorStateGeneric(self.cursor)
            self.do(UndoInsertBar(state))
            self.cursor.element = self.current_tab.element(state.element).chord(0)
            self.update()
        elif action == Action.REMOVE_BAR:
            self.remove_bar()
        else:
            self.console.echo("Unhandled action: {}, Modifier: {}".format(action, user_cmd.modifier))

        return True

    def remove_text(self):
        state = CursorStateText(self.cursor)
        text = self.cursor.element
        self.do(UndoRemoveText(state, text))
        self.update()

    def remove_bar(self):
        state = CursorState(self.cursor)
        bar = self.cursor.bar
        self.do(UndoRemoveBar(state, bar))
        self.update()

    def paste(self):
        if self.clipboard is None:
            self.console.error("Nothing to paste!")
        else:
            el_type = self.clipboard.get("type")
            if el_type == "Chord":
                state = CursorState(self.cursor)
                self.do(UndoReplaceChord(state, self.clipboard))
                self.update()
            elif el_type == "Text":
                state = CursorStateGeneric(self.cursor)
                self.do(UndoInsertText(state, ""))
                self.cursor.element = self.current_tab.element(state.element)
                self.cursor.element.read(self.clipboard)
                self.update()

    def set_tuning(self, strings):
        if len(strings) == 0:
            self.console.error("Must specify at least one string for tuning!")
            return True

        if self.current_tab.tuning_causes_loss(strings):
            confirm = self.console.confirm("Setting this tuning will cause loss of data. Continue?")
            if not confirm:
                return True

        self.do(UndoSetTuning(strings))
        self.update()
        return True

    def undo(self):
        res, action = self.current_tab.undo_stack.undo()
        if not res:
            self.console.error("Nothing to undo!")
        else:
            self.console.echo("Undo {}".format(action.undo_name))
            self.update()

    def redo(self):
        res, action = self.current_tab.undo_stack.redo()
        if not res:
            self.console.error("Nothing to redo!")
        else:
            self.console.echo("Redo {}".format(action.undo_name))
            self.update()

    def post_cursor_move(self):
        self.first_entry = True
        tab = self.current_tab.layout()
        self.move_viewport_for_cursor(tab)
        self.draw()

    def clear_chord(self):
        state = CursorState(self.cursor)
        self.do(UndoClearChord(state))
        self.update()

    def insert_chord(self):
        state = CursorState(self.cursor)
        self.do(UndoInsertChord(state))
        self.update()

    def remove_chord(self):
        if self.cursor.bar.nchords == 1:
            return

        state = CursorState(self.cursor)
        if not (self.cursor.bar_number == self.current_tab.nels - 1
                and self.cursor.chord_number == self.cursor.bar.nchords - 1):
            self.cursor.move(1)
        else:
            self.cursor.move(-1)
        self.do(UndoRemoveChord(state))
        self.update()

    def save_current(self, path = None):
        if self.file_path is None and path is None:
            self.console.error("Must specify location to write to!")
            return False

        path_to_use = path or self.file_path
        written = self.current_tab.write()
        value = json.dumps(written)

        # Automatically add extension if none provided
        _, file_extension = splitext(path_to_use)
        if file_extension == "":
            path_to_use += "." + FILE_EXTENSION

        try:
            with open(expanduser(path_to_use), "w") as f:
                f.write(value)
        except IOError:
            self.console.error("Couldn't open {}!".format(path))
            return False

        self.file_path = path_to_use
        self.dirty = False
        self.header.filename = path_to_use
        self.header.update()
        self.console.echo("Saved successfully")
        return True

    def read(self, path):
        # Automatically add extension if none provided
        _, file_extension = splitext(path)
        if file_extension == "":
            path += "." + FILE_EXTENSION

        try:
            with open(expanduser(path), "r") as f:
                raw_text = f.read()
        except IOError:
            self.console.error("Couldn't open {}!".format(path))
            return False

        try:
            obj = json.loads(raw_text)
        except json.JSONDecodeError:
            self.console.error("File corrupted, could not read")
            return False

        new_tab = Tab()
        new_tab.read(obj)

        self.current_tab = new_tab
        self.file_path = path
        self.dirty = False
        self.header.filename = path
        self.header.update()
        self.update()

    def read_plaintext(self, path):
        try:
            with open(expanduser(path), "r") as f:
                raw_text = f.read()
        except IOError:
            self.console.error("Couldn't open {}!".format(path))
            return False

        try:
            model = from_plaintext(raw_text)
        except:
            self.console.error("Couldn't read tab!")
            return False

        new_tab = Tab()
        new_tab.read(model)
        self.current_tab = new_tab
        self.file_path = None
        self.dirty = False
        self.header.filename = "Untitled"
        self.header.update()
        self.update()

    def text_backspace(self):
        if self.cursor.position == 0:
            return

        state = CursorStateText(self.cursor)
        self.do(UndoDeleteChar(state, -1))
        self.cursor.move_position(-1)
        self.update()

    def text_delete(self):
        if self.cursor.position >= self.cursor.element.text_length - 1:
            return

        state = CursorStateText(self.cursor)
        self.do(UndoDeleteChar(state, 0))
        self.update()

    def shrink_bar(self):
        if self.cursor.bar.size_change_causes_loss(1/2):
            self.console.echo("Can't shrink further, would delete notes")
            return

        state = CursorState(self.cursor)
        self.do(UndoResizeBar(state, 1/2))
        bar = self.current_tab.element(state.bar)
        n_to_use = state.chord // 2
        if n_to_use > bar.nchords - 1:
            n_to_use = bar.nchords - 1
        self.cursor.element = bar.chord(n_to_use)
        self.update()

    def note_input(self, key):
        if not (len(key) == 1 and ACCEPTED_NOTE_VALS.match(key)):
            return True

        # here we finally can handle note input
        state = CursorState(self.cursor)
        value = self.cursor.note.value
        if self.first_entry:
            value = key
        else:
            value += key
        self.do(UndoSetNoteValue(state, value))
        self.update()
        self.first_entry = False

        return True

    def text_input(self, key):
        if not len(key) == 1:
            return True

        if ord(key) < 32 and ord(key) not in (9, 10, 13):
            return True

        state = CursorStateText(self.cursor)
        self.do(UndoInsertTextCharacter(state, key))
        self.cursor.move_position(1)
        self.update()

        return True

    def handle_input(self, key):
        if self.mode != Mode.EDIT:
            return True

        if self.cursor.on_chord:
            return self.note_input(key)
        elif self.cursor.on_text:
            return self.text_input(key)
        return True

    def draw(self):
        self.win.refresh()
