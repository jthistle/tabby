
#!/usr/bin/env python3

import simpleaudio as sa

from .conversion import samples_to_data
from .instrument import Instrument
from .const import SAMPLE_RATE, SAMPLE_WIDTH, CHANNELS


BASE_PATH = "./src/synth/samples/"


class Note:
    data = None
    play_obj = None
    fadeout = 0.05

    def __init__(self, samples, length):
        self.samples = samples
        self.length = length

        self.apply_envelope()
        self.bake()

    @property
    def finished(self):
        if not self.play_obj:
            return False
        return not self.play_obj.is_playing()

    def apply_envelope(self):
        fadeout_samples = int(self.fadeout * SAMPLE_RATE)
        max_v = len(self.samples)
        for i in range(max_v - fadeout_samples, max_v):
            frac = (max_v - i) / fadeout_samples
            self.samples[i] = int(self.samples[i] * frac)

    def bake(self):
        self.data = samples_to_data(self.samples)

    def start(self):
        if self.data is None:
            return
        obj = sa.play_buffer(self.data, CHANNELS, SAMPLE_WIDTH, SAMPLE_RATE)
        self.play_obj = obj



class Synthesizer:
    def __init__(self):
        self.instrument = Instrument(BASE_PATH + "electric_clean")
        self.notes = []

    def play_note(self, note, length = 1):
        samples = self.instrument.get_note(note, length)
        note = Note(samples, length)
        note.start()
        self.notes.append(note)

    def wait(self):
        while len(self.notes) > 0:
            for i in range(len(self.notes) - 1, -1, -1):
                if not self.notes[i].finished:
                    continue
                del self.notes[i]


