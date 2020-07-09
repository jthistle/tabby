import curses
from console import Console
from header import Header


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

    def handle_cmd(self, cmd):
        self.console.echo("Cmd: {}".format(cmd))

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
