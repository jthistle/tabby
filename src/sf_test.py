
from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn
from util.logger import logger

synth = Synthesizer()

synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
inst = synth.new_instrument(0, 74)

print(inst.preset)

inst.send_event(EventNoteOn(60, 100))

synth.halt()
