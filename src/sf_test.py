
from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn
from util.logger import logger
import time


synth = Synthesizer()

# synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
synth.load_soundfont("/home/james/Documents/MuseScore3Development/SoundFonts/MuseScore_General_Lite-v0.1.5/MuseScore_General_Lite.sf2")
inst = synth.new_instrument(0, 57)

print(synth.sfont.presets_list_user())

input()
inst.send_event(EventNoteOn(60, 100))
note = synth.interface.play(inst.notes[0].sample_data, channels=1, loop=inst.notes[0].sample.loop)


input()
synth.interface.end_loop(note)

# synth.halt()

input()
synth.halt()
