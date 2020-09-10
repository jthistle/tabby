
import curses

from .help import get_help
from util.logger import logger
from .mode import Mode


class HelpViewer:
    def __init__(self, parent):
        self.parent = parent
        self.dimensions = (curses.LINES - 2, curses.COLS)
        self.win = curses.newwin(*self.dimensions, 1, 0)
        self.win.keypad(True)

        self.current_content = ""

    def update(self):
        self.win.erase()
        self.win.addstr(self.current_content)

    def update_parent_mode(self):
        if self.parent.mode != Mode.HELP:
            self.parent.change_mode(Mode.HELP)

    def show_welcome(self):
        self.update_parent_mode()
        self.current_content = get_help()
        self.update()

    def show_help(self, parts):
        if len(parts) < 2:
            self.show_welcome()
            return True

        res = get_help(" ".join(parts[1:]))
        if res is None:
            self.parent.console.error("Couldn't find help for that command!")
            return True

        self.update_parent_mode()
        self.current_content = res
        self.update()
        return True
