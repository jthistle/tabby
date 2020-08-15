

from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn, EventNoteOff
from util.logger import logger
import time
from lib.notenames import name_to_val


synth = Synthesizer()

synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
# synth.load_soundfont("/home/james/Documents/MuseScore3Development/SoundFonts/MuseScore_General_Lite-v0.1.5/MuseScore_General_Lite.sf2")

inst = synth.new_instrument(0, 56)

BEAT = 60 / 140

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
    note_val = name_to_val(note[0])
    inst.send_event(EventNoteOn(note_val, 100))
    time.sleep(note[1] - 0.05)
    inst.send_event(EventNoteOff(note_val))
    time.sleep(0.05)

input()
synth.halt()
