
from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn, EventNoteOff
from util.logger import logger
import time


NOTE = 50

synth = Synthesizer()

# synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
synth.load_soundfont("/home/james/Documents/MuseScore3Development/SoundFonts/MuseScore_General_Lite-v0.1.5/MuseScore_General_Lite.sf2")

inst = synth.new_instrument(0, 64)

print(synth.sfont.presets_list_user())

input()
for i in range(10):
    inst.send_event(EventNoteOn(NOTE, 100))
    time.sleep(2)
    inst.send_event(EventNoteOff(NOTE))
    time.sleep(0.5)
    NOTE += 2

input()
synth.halt()
