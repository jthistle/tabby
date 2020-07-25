
"""
A script for (manually) testing the synthesizer module.

Try it out! `python3 ./src/synth_test.py`
"""

import time
from synth.synthesizer import Synthesizer
from lib.notenames import name_to_val

synth = Synthesizer()
synth.play_note(name_to_val("G2"), 2)
synth.play_note(name_to_val("B2"), 2)
synth.play_note(name_to_val("D3"), 2)
synth.play_note(name_to_val("F3"), 2)

synth.wait()

BEAT = 60 / 120

MUSIC = [
    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("C4", BEAT),
    ("A3", BEAT * 0.5),

    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("G3", BEAT),
    ("F3", BEAT * 0.5),

    ("E3", BEAT * 0.5),
    ("E3", BEAT * 0.5),
    ("F3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("C3", BEAT),
    ("D3", BEAT),

    ("E3", BEAT * 4),

    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("C4", BEAT),
    ("A3", BEAT * 0.5),

    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("G3", BEAT),
    ("F3", BEAT * 0.5),

    ("E3", BEAT * 0.5),
    ("E3", BEAT * 0.5),
    ("F3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("C3", BEAT),
    ("D3", BEAT),
    ("C3", BEAT * 4),

    ("B3", BEAT),
    ("E3", BEAT),
    (None, BEAT * 0.5),
    ("C4", BEAT),
    ("B3", BEAT * 0.5),

    ("B3", BEAT * 0.5),
    ("A3", BEAT * 0.5),
    ("A3", BEAT * 0.5),
    ("B3", BEAT * 0.5),
    ("A3", BEAT * 2),

    ("A3", BEAT),
    ("D3", BEAT),
    (None, BEAT * 0.5),
    ("B3", BEAT),
    ("A3", BEAT * 0.5),

    ("A3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("A3", BEAT * 0.5),
    ("G3", BEAT * 2),

    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("C4", BEAT),
    ("A3", BEAT * 0.5),

    ("G3", BEAT),
    ("C3", BEAT),
    (None, BEAT * 0.5),
    ("G3", BEAT),
    ("F3", BEAT * 0.5),

    ("E3", BEAT * 0.5),
    ("E3", BEAT * 0.5),
    ("F3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("C3", BEAT),
    ("D3", BEAT),

    (None, BEAT * 0.5),
    ("E3", BEAT * 0.5),
    ("F3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("C3", BEAT),
    ("D3", BEAT),

    (None, BEAT * 0.5),
    ("E3", BEAT * 0.5),
    ("F3", BEAT * 0.5),
    ("G3", BEAT * 0.5),
    ("C4", BEAT),
    ("D4", BEAT),
    ("C4", BEAT * 4),
]

for note in MUSIC:
    if note[0] is None:
        time.sleep(note[1])
        continue
    synth.play_note(name_to_val(note[0]), note[1])
    synth.wait()
