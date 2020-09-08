#!/usr/bin/env python3

import os
import curses
from ui.tabby import Tabby
from ui.colour_pairs import init_pairs
from synth.fluidsynth import Synth


def setup():
    os.environ.setdefault('ESCDELAY', '0')


def post_start():
    init_pairs()


def main(stdscr):
    post_start()

    synth = Synth(gain=1)
    synth.sfload("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
    synth.start(driver="alsa")

    instance = Tabby(synth)

    res = True
    while res:
        res = instance.handle_input()

    synth.delete()


if __name__ == "__main__":
    setup()
    curses.wrapper(main)
