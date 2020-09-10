
import curses

from .action import Action
from .help import get_help
from util.logger import logger
from .mode import Mode


class HelpViewer:
    def __init__(self, parent):
        self.parent = parent
        self.dimensions = (curses.LINES - 2, curses.COLS)
        self.win = curses.newwin(*self.dimensions, 1, 0)
        self.win.keypad(True)

        self.position = 0

        self.__current_content = ""
        self.content_lines = 0

    @property
    def current_content(self):
        return self.__current_content

    @current_content.setter
    def current_content(self, new_val):
        self.__current_content = new_val
        self.content_lines = len(self.current_content.split("\n"))

    def handle_cmd(self, user_cmd):
        action = user_cmd.action
        if action == Action.MOVE_VIEW_DOWN:
            self.position = min(self.position + 1, self.content_lines - self.dimensions[0] + 2)
            self.update()
        elif action == Action.MOVE_VIEW_UP:
            self.position = max(self.position - 1, 0)
            self.update()
        else:
            return None

        return True

    def update(self):
        self.win.erase()
        self.win.addstr("\n".join(
            self.current_content.split("\n")[self.position:self.dimensions[0] + self.position]
        ))

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
