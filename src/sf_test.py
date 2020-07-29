
from synth.synthesizer import Synthesizer


import time
import wave
from synth.basic.conversion import data_to_samples
from synth.interface import AudioInterface, AudioConfig
from util.logger import logger

# synth = Synthesizer()

# synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
# synth.use_preset(0, 74)

# for x in my_sf.presets:
#     print(x)

cfg = AudioConfig()
latency = 0.1
inter = AudioInterface(cfg, target_latency=0.01, max_latency=latency)

def read_wav(file):
    wave_obj = wave.open(file, "rb")
    data = wave_obj.readframes(wave_obj.getnframes())
    return data_to_samples(data)

waves = [
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[:44100],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[44100:44100*4],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/G3.wav")[:44100*2],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/E4.wav")[:44100*2],
]

print("playing")
# for w in waves:
#     b = inter.play(w, channels=1)

b = inter.play(waves[0], channels=1)
inter.extend(b, waves[1], channels=1)
