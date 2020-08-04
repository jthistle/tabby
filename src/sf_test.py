
from synth.synthesizer import Synthesizer
from synth.event import EventNoteOn
from util.logger import logger

synth = Synthesizer()

synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
inst = synth.new_instrument(0, 4)

print(inst.preset)

input()
inst.send_event(EventNoteOn(50, 100))
# synth.interface.play(inst.notes[0].sample_data)

# synth.halt()

input()
synth.halt()
