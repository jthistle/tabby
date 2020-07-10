import curses
import re
from .line_input import LineInput
from .colour_pairs import Pair

class Console:
    def __init__(self):
        self.win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.win.keypad(True)
        self.output = ""
        self.current_cmd = ""
        self.in_cmd = False

        self.line_input = LineInput(self.win, self.on_input_val_change, 1)

        self.in_error_state = False

        # Initial update
        self.update()
        self.draw()


    def set_output(self, msg):
        self.output = msg
        self.update()
        self.draw()

    def echo(self, msg):
        self.in_error_state = False
        self.set_output(msg)

    def error(self, msg):
        self.in_error_state = True
        self.set_output(msg)

    def clear(self):
        self.echo("")

    def begin_cmd(self):
        if self.in_cmd:
            self.echo("Internal error: already in cmd!")
            return

        self.in_cmd = True
        self.current_cmd = ""
        self.echo(":")
        self.line_input.reset()
        curses.curs_set(1)

    def end_cmd(self):
        if not self.in_cmd:
            self.echo("Internal error: not in cmd!")
            return

        self.in_cmd = False
        self.clear()
        curses.curs_set(0)

    def on_input_val_change(self, new_val):
        self.current_cmd = new_val
        self.echo(":" + self.current_cmd)

    def handle_input(self):
        if not self.in_cmd:
            self.echo("Internal error: can't handle input, not in cmd!")
            return

        res = self.line_input.handle_input()

        if not res:
            self.end_cmd()

        return res

    def confirm(self, msg):
        curses.curs_set(1)
        self.echo("{} [Y/N]".format(msg))

        key = self.win.getkey()
        res = False
        if key.lower() == "y":
            res = True

        curses.curs_set(0)
        self.echo("")
        return res

    def update(self):
        text_attr = 0
        if self.in_error_state:
            text_attr = curses.color_pair(Pair.WHITE_RED.value)

        self.win.clear()
        self.win.addstr(0, 0, self.output, text_attr)

    def draw(self):
        self.win.refresh()

