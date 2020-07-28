
from synth.synthesizer import Synthesizer

import time
import wave
from synth.basic.conversion import data_to_samples
from synth.interface import AudioInterface, AudioConfig

# synth = Synthesizer()

# synth.load_soundfont("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
# synth.use_preset(0, 74)

# for x in my_sf.presets:
#     print(x)

cfg = AudioConfig()
latency = 0.1
inter = AudioInterface(cfg, max_latency=latency)

def read_wav(file):
    wave_obj = wave.open(file, "rb")
    data = wave_obj.readframes(wave_obj.getnframes())
    return data_to_samples(data)

waves = [
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[:44100],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[44100:44100*2],
    # read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/G3.wav")[:44100*5],
    # read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/E4.wav")[:44100*5],
]

print("playing")
for w in waves:
    print("play")
    inter.play(w, channels=1)
    time.sleep(1 - latency - 0.005)
