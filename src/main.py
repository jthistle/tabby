#!/usr/bin/env python3

import os
import curses
from ui.tabby import Tabby
from ui.colour_pairs import init_pairs


def setup():
    os.environ.setdefault('ESCDELAY', '0')


def post_start():
    init_pairs()


def main(stdscr):
    post_start()

    instance = Tabby()

    res = True
    while res:
        res = instance.handle_input()


if __name__ == "__main__":
    setup()
    curses.wrapper(main)
