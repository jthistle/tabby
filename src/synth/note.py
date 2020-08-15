
import math
import struct

from .repitch import cents_to_ratio
from .sf2.definitions import SFGenerator, LoopType
from .interface import CustomBuffer
from util.logger import logger


COARSE_SIZE = 2 ** 15
BASE_SAMPLE_RATE = 44100


def interpolate(a, b, t):
    # Linear interpolation is good enough
    return a + (b - a) * t


class Note:
    def __init__(self, key, on_vel, sample, gens, mods):
        self.sample = sample
        self.key = key
        self.on_vel = on_vel
        self.gens = gens
        self.mods = mods

        self.playback = None
        self.position = 0
        self.stopped = False    # TEMP - replace with proper env

        # SoundFont spec 2.01, 8.1.2
        # SFGenerator.overridingRootKey:
        # "This parameter represents the MIDI key number at which the sample is to be played back
        #  at its original sample rate.  If not present, or if present with a value of -1, then
        #  the sample header parameter Original Key is used in its place.  If it is present in the
        #  range 0-127, then the indicated key number will cause the sample to be played back at
        #  its sample header Sample Rate"
        original_key = self.sample.pitch if self.gens[SFGenerator.overridingRootKey] == -1 else self.gens[SFGenerator.overridingRootKey]
        self.hard_pitch_diff = (self.key - original_key) * 100 + self.sample.pitch_correction
        self.hard_pitch_diff += self.gens[SFGenerator.coarseTune] * 100 + self.gens[SFGenerator.fineTune]


        sample_ratio = self.sample.sample_rate / BASE_SAMPLE_RATE
        self.total_ratio = sample_ratio * cents_to_ratio(self.hard_pitch_diff)

        offset_s = self.gens[SFGenerator.startAddrsOffset] + self.gens[SFGenerator.startAddrsCoarseOffset] * COARSE_SIZE
        offset_e = self.gens[SFGenerator.endAddrsOffset] + self.gens[SFGenerator.endAddrsCoarseOffset] * COARSE_SIZE

        # buffer should be given as a list of frames where possible
        self.sample_data = struct.unpack("<{}h".format(len(sample.data) // 2), sample.data)
        self.sample_size = len(self.sample_data)

        self.loop = None
        if self.gens[SFGenerator.sampleModes].loop_type in (LoopType.CONT_LOOP, LoopType.KEY_LOOP):
            self.loop = [x for x in self.sample.loop]

        # Optional debug:
        # print("gens")
        # for g in self.gens:
        #     print(">",g,self.gens[g])

        # print("\n\nmods")
        # for m in self.mods:
        #     print(">",m)

        # print("\nsample:", self.sample)

    def play(self, inter):
        if not self.sample.is_mono:
            print("Stereo samples are not supported yet")
            return

        self.playback = inter.add_custom_buffer(CustomBuffer(), self.collect)

    def stop(self, inter):
        if self.loop is not None:
            inter.end_loop(self.playback)
            self.stopped = True

    def collect(self, size, looping):
        if self.stopped:
            return []

        LIMIT = (1 << 15) - 1

        channel_ratio = 2        # TODO do this properly
        rate = self.total_ratio

        finished = []
        count = 0
        end = self.sample_size - math.ceil(rate)
        while self.position < end:
            i = int(self.position)
            frac = self.position - i
            s1 = self.sample_data[i]
            s2 = self.sample_data[i + math.ceil(rate)]
            val = int(interpolate(s1, s2, frac))

            # Apply clipping
            for i in range(channel_ratio):
                finished.append(val)
                count += 1

            self.position += rate
            if looping:
                if self.position > self.loop[1]:
                    self.position = self.loop[0] + (self.position - self.loop[1])

            if count >= size:
                break

        return finished
