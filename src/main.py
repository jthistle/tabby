#!/usr/bin/env python3

import os
import curses
from ui.editor import Editor
from ui.colour_pairs import init_pairs


def setup():
    os.environ.setdefault('ESCDELAY', '0')


def post_start():
    init_pairs()


def main(stdscr):
    post_start()

    editor = Editor()

    res = True
    while res:
        res = editor.handle_input()


if __name__ == "__main__":
    setup()
    curses.wrapper(main)
