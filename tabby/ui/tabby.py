
import curses

from lib.element import ElementType
from .header import Header
from .editor import Editor
from .console import Console
from .mode import Mode, mode_name
from .action import Action
from .hotkeys import key_to_action
from .cmd_parser import parse_cmd

from util.logger import logger

class Tabby:
    def __init__(self):
        self.mode = Mode.VIEW

        self.header = Header()
        self.editor = Editor(self)
        self.help_viewer = None     # TODO
        self.console = Console()

        self.win = self.editor.win

    def change_mode(self, new_mode):
        if new_mode == self.mode:
            return

        old_mode = self.mode
        self.mode = new_mode

        if new_mode in (Mode.VIEW, Mode.EDIT):
            self.editor.on_mode_change(old_mode, new_mode)
            self.win = self.editor.win
            self.editor.update()
        elif new_mode == Mode.HELP:
            # TODO uhhh probably set some help text here or smth idk
            self.win = self.help_viewer.win
            self.help_viewer.update()

        if new_mode != Mode.VIEW:
            self.console.echo("-- {} MODE --".format(mode_name(new_mode)))
        else:
            self.console.clear()


    def handle_input(self):
        """Returns False when the programme should exit, otherwise true."""
        # self.console.echo("Char: {}".format(repr(key)).replace("\n", "newline"))

        action_to_use = None
        if self.console.in_cmd:
            res = self.console.handle_input()
            if res:
                return True
            elif self.console.current_cmd != "":
                action_to_use = parse_cmd(self.console.current_cmd)
                if not action_to_use:
                    self.console.error("Invalid command!")
                    return True

        key = None
        if action_to_use is None:
            key = self.win.getkey()
            if len(key) == 1 and ord(key) == 27:    # ESC, temp for debug
                self.change_mode(Mode.VIEW)
                return True
            selected_type = ElementType.ANY
            if self.editor:
                selected_type = self.editor.cursor.element.type
            action_to_use = key_to_action(key, self.mode, selected_type)
            # logger.debug("key: {}, action: {}".format(key, action_to_use.action if action_to_use is not None else None))

        if action_to_use is not None:
            return self.handle_cmd(action_to_use)

        if self.mode == Mode.EDIT:
            return self.editor.handle_input(key)
        elif self.mode == Mode.HELP:
            return self.help_viewer.handle_input(key)

        return True

    def show_help(self, parts):
        if parts is None or len(parts) < 2:
            self.console.error("No command specified!")
            return True

        # TODO show help maybe

    def handle_cmd(self, user_cmd):
        action = user_cmd.action
        if action == Action.HELP:
            return self.show_help(user_cmd.parts)
        if action == Action.MODE_HELP:
            self.change_mode(Mode.HELP)
        elif action == Action.MODE_EDIT:
            self.change_mode(Mode.EDIT)
        elif action == Action.MODE_VIEW:
            self.change_mode(Mode.VIEW)
        elif action == Action.BEGIN_CMD:
            self.console.begin_cmd()
        else:
            return self.editor.handle_cmd(user_cmd)

        return True
