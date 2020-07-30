
import simpleaudio as sa
import wave
import time
from synth.basic.conversion import data_to_samples, samples_to_data
from synth.basic.repitch import change_pitch_semitones
from synth.interface import AudioInterface, AudioConfig

cfg = AudioConfig()
latency = 0.1
inter = AudioInterface(cfg, max_latency=latency, use_buffering=True)

def read_wav(file):
    wave_obj = wave.open(file, "rb")
    data = wave_obj.readframes(wave_obj.getnframes())
    return data_to_samples(data)

wave = read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[:44100 * 2]

waves = [change_pitch_semitones(wave, i) for i in range(10)]

for i in range(10):
    input("Press ENTER")
    inter.play(waves[i], 1)

time.sleep(3)
inter.halt()
