import curses
from console import Console
from header import Header
from cmd_parser import parse_cmd, Action, ActionMod, get_help

class Editor:
    def __init__(self):
        self.header = Header()
        self.console = Console()
        self.win = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
        self.win.keypad(True)

        # Initial update
        self.update()
        self.draw()

    def update(self):
        self.win.clear()
        self.win.addstr(0, 1, "Hello, world!")

    def handle_cmd(self, raw_cmd):
        cmd = parse_cmd(raw_cmd)
        if not cmd:
            self.console.error("Invalid command!")
            return

        action = cmd.get("action")
        if action == Action.HELP:
            cmd_str = ""
            if len(cmd.get("parts")) == 1:
                # TODO display help screen
                cmd_str = cmd.get("parts")[0]
            else:
                cmd_str = cmd.get("parts")[1]
            help_str = get_help(cmd_str)
            if help_str is None:
                self.console.error("Command {} doesn't exist!".format(cmd_str))
                return
            self.console.echo("usage: " + help_str.format(cmd_str))
        else:
            self.console.echo("Action: {}, Modifier: {}".format(cmd.get("action"), cmd.get("modifier")))

    def handle_input(self):
        if self.console.in_cmd:
            res = self.console.handle_input()
            if res:
                return True
            elif self.console.current_cmd != "":
                self.handle_cmd(self.console.current_cmd)

        key = self.win.getkey()
        if len(key) == 1 and ord(key) == 27:    # ESC, temp for debug
            return False
        elif key == ":":
            self.console.begin_cmd()
        else:
            self.console.echo("Char: {}".format(key).replace("\n", "newline"))

        return True

    def draw(self):
        self.win.refresh()
