
from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn, EventNoteOff
from util.logger import logger
import time


NOTE = 50

synth = Synthesizer()

synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
# synth.load_soundfont("/home/james/Documents/MuseScore3Development/SoundFonts/MuseScore_General_Lite-v0.1.5/MuseScore_General_Lite.sf2")

inst = synth.new_instrument(0, 0)

print(synth.sfont.presets_list_user())

input()
inst.send_event(EventNoteOn(60, 100))
inst.send_event(EventNoteOn(64, 100))
inst.send_event(EventNoteOn(67, 100))

input()

inst.send_event(EventNoteOff(60))
inst.send_event(EventNoteOff(64))
inst.send_event(EventNoteOff(67))

input()
synth.halt()
