
from synth.synthesizer import Synthesizer
from util.logger import logger

synth = Synthesizer()

synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
synth.use_preset(0, 74)

# for x in synth.sfont.presets:
#     print(x)
