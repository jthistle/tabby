#!/usr/bin/env python3

import os
import curses
from editor import Editor
from colour_pairs import init_pairs


def setup():
    os.environ.setdefault('ESCDELAY', '0')


def post_start():
    init_pairs()


def main(stdscr):
    editor = Editor()

    post_start()

    res = True
    while res:
        res = editor.handle_input()


if __name__ == "__main__":
    setup()
    curses.wrapper(main)
