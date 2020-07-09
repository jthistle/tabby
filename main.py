#!/usr/bin/env python3

import os
from curses import wrapper
from editor import Editor


def setup():
    os.environ.setdefault('ESCDELAY', '0')


def main(stdscr):
    editor = Editor()

    res = True
    while res:
        res = editor.handle_input()


if __name__ == "__main__":
    setup()
    wrapper(main)
