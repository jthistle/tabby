
import simpleaudio as sa
import time
import wave
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

waves = [
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[:44100 * 1],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/G3.wav")[:44100 * 1],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/E4.wav")[:44100 * 1],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/G3.wav")[:44100 * 1],
    read_wav("/home/james/Python/tabby/src/synth/samples/electric_clean/C3.wav")[44100:44100*2],
]

waves[2] = change_pitch_semitones(waves[2], -1)
waves[1] = change_pitch_semitones(waves[1], -1)
waves[3] = change_pitch_semitones(waves[3], 2)

byte_waves = []
for w in waves:
    byte_waves.append(samples_to_data(w))

print("Tabby audio interface:")
for i in range(10):
    for w in waves:
        b = inter.play(w, channels=1)
        time.sleep(0.1)
time.sleep(1)

print("SimpleAudio:")
for i in range(10):
    for w in byte_waves:
        sa.play_buffer(w, 1, 2, 44100)
        time.sleep(0.1)
time.sleep(1)

print("Tabby audio interface can extend existing playback. Here is an example of two samples joined together:")
b = inter.play(waves[0], channels=1)
inter.extend(b, waves[4], channels=1)
time.sleep(4)

print("Didn't notice it, right? Here's how SimpleAudio compares:")
b = sa.play_buffer(byte_waves[0], 1, 2, 44100)
b.wait_done()
sa.play_buffer(byte_waves[4], 1, 2, 44100)
time.sleep(3)

print("Even waiting until just before the end isn't quite right:")
b = sa.play_buffer(byte_waves[0], 1, 2, 44100)
time.sleep(0.995)
sa.play_buffer(byte_waves[4], 1, 2, 44100)
time.sleep(3)

print("And that's why Tabby needs its own interface (:")

inter.halt()
