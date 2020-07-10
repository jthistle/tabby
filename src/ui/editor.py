import curses
from .console import Console
from .header import Header
from .cmd_parser import parse_cmd, Action, ActionMod, get_help
from lib.tab import Tab
from util.logger import logger
from .colour_pairs import Pair
from .mode import Mode, mode_name
from .help import HELP_STR

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

        # Initial update
        curses.curs_set(0)
        self.update()
        self.draw()

    def help_update(self):
        self.win.clear()
        self.win.addstr(0, 0, HELP_STR)

    def update(self):
        if self.mode == Mode.HELP:
            self.help_update()
            return

        self.win.clear()
        tab = self.current_tab.layout()
        self.win.addstr(self.viewport_pos, 0, tab.txt)

        if self.mode == Mode.EDIT:
            self.update_cursor(tab)

    def update_cursor(self, tab = None, clear = False):
        # TODO: re-layout-ing the entire tab for every cursor move probably isn't a good idea.
        # In the future, just work out a way of doing it without doing this.
        if not tab:
            tab = self.current_tab.layout()

        if clear:
            # Remove last highlighting if only updating cursor
            self.clear_cursor()

        # Process new cursor highlighting
        for pos in tab.highlighted:
            ch = self.win.inch(pos[0], pos[1])
            self.win.addch(pos[0], pos[1], ch, curses.color_pair(Pair.HIGHLIGHT_DIM.value) | curses.A_DIM)

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

        if old_mode == Mode.EDIT:
            self.clear_cursor()

        self.mode = new_mode
        if new_mode == Mode.EDIT:
            self.update_cursor()
            self.first_entry = True

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
                self.change_mode(Mode.HELP)
            else:
                cmd_str = cmd.get("parts")[1]
                help_str = get_help(cmd_str)
                if help_str is None:
                    self.console.error("Command {} doesn't exist!".format(cmd_str))
                else:
                    self.console.echo("usage: " + help_str.format(cmd_str))
        elif action == Action.SAVE_QUIT:
            # TODO save
            return False
        elif action == Action.QUIT:
            return False
        else:
            self.console.echo("Action: {}, Modifier: {}".format(cmd.get("action"), cmd.get("modifier")))

        return True

    def post_cursor_move(self):
        self.first_entry = True
        self.update_cursor(tab=None, clear=True)
        self.draw()

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
        elif self.mode == Mode.VIEW:
            if key == "e":
                self.change_mode(Mode.EDIT)
            elif key == "h":
                self.change_mode(Mode.HELP)
            elif key == ":":
                self.console.begin_cmd()
        elif self.mode == Mode.EDIT:
            if key == "KEY_RIGHT" or key == "KEY_LEFT":
                direction = 1 if key == "KEY_RIGHT" else -1
                self.current_tab.cursor.move(direction)
                self.post_cursor_move()
            elif key == "kRIT5" or key == "kLFT5":      # w/ ctrl mod
                direction = 1 if key == "kRIT5" else -1
                self.current_tab.cursor.move_big(direction)
                self.post_cursor_move()
            elif key == "KEY_UP" or key == "KEY_DOWN":
                direction = 1 if key == "KEY_UP" else -1
                self.current_tab.cursor.move_string(direction)
                self.post_cursor_move()
            elif len(key) == 1:
                note = self.current_tab.cursor.note()
                if self.first_entry:
                    note.value = key
                else:
                    note.value += key
                self.update()
                self.first_entry = False

        # self.console.echo("Char: {}".format(key).replace("\n", "newline"))

        return True

    def draw(self):
        self.win.refresh()
