
import math
import struct
import time

from .repitch import cents_to_ratio
from .sf2.definitions import SFGenerator, LoopType
from .interface import CustomBuffer
from .sf2.convertors import timecents_to_secs, decibels_to_atten
from .envelope import Envelope
from util.logger import logger


# Optimization tooling
import cProfile
profile = cProfile.Profile()


COARSE_SIZE = 2 ** 15
BASE_SAMPLE_RATE = 44100
SINGLE_SAMPLE_LEN = 1 / 44100


class Note:
    def __init__(self, inter, key, on_vel, sample, gens, mods):
        self.inter = inter
        self.sample = sample
        self.key = key
        self.on_vel = on_vel
        self.gens = gens
        self.mods = mods

        self.playback = None
        self.position = 0

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

        self.sample_data = struct.unpack("<{}h".format(len(sample.data) // 2), sample.data)
        self.sample_size = len(self.sample_data)

        self.loop = None
        if self.gens[SFGenerator.sampleModes].loop_type in (LoopType.CONT_LOOP, LoopType.KEY_LOOP):
            self.loop = [x for x in self.sample.loop]

        self.vol_env = Envelope(
            timecents_to_secs(self.gens[SFGenerator.delayVolEnv]),
            timecents_to_secs(self.gens[SFGenerator.attackVolEnv]),
            timecents_to_secs(self.gens[SFGenerator.holdVolEnv]),
            timecents_to_secs(self.gens[SFGenerator.decayVolEnv]),
            decibels_to_atten(self.gens[SFGenerator.sustainVolEnv] / 10),   # sus uses cB = 1/10 dB
            timecents_to_secs(self.gens[SFGenerator.releaseVolEnv]),
        )

        # Optional debug:
        # print("gens")
        # for g in self.gens:
        #     print(">",g,self.gens[g])

        # print("\n\nmods")
        # for m in self.mods:
        #     print(">",m)

        # print("\nsample:", self.sample)

    def play(self):
        if not self.sample.is_mono:
            print("Stereo samples are not supported yet")
            return

        self.playback = self.inter.add_custom_buffer(CustomBuffer(self.loop is not None), self.collect)

    def stop(self):
        self.vol_env.release()

    def collect(self, *args):
        return self.__collect(*args)
        # return profile.runcall(self.__collect, *args)

    def __collect(self, size, looping):
        if self.vol_env.finished:
            self.inter.end_loop(self.playback)
            return []

        channel_ratio = 2        # TODO do this properly
        rate = self.total_ratio

        finished = []
        count = 0
        offset = math.ceil(rate)
        end = self.sample_size - offset
        while looping or self.position < end:
            i = int(self.position)
            frac = self.position - i
            s1 = self.sample_data[i]
            # If adding the offset overshoots the end of the sample loop, make sure that we wrap back arround
            # to the start of the loop again. Enjoy the horrible conditional.
            s2 = self.sample_data[i + offset if not looping or i + offset < self.loop[1] else self.loop[0] + (i + offset - self.loop[1])]
            val = int(s1 + (s2 - s1) * frac) * self.vol_env.current_val

            finished += [val] * channel_ratio
            count += channel_ratio

            self.position += rate
            if looping and self.position > self.loop[1]:
                self.position = self.loop[0] + (self.position - self.loop[1])

            # envprofile.runcall(self.vol_env.update, SINGLE_SAMPLE_LEN)
            self.vol_env.update(SINGLE_SAMPLE_LEN)

            if count >= size:
                break

        return finished


# Optimization tools

import sys, signal, pstats

def end(signum, frame):
    global profile
    global envprofile
    try:
        ps = pstats.Stats(profile)
        ps.sort_stats("cumtime")
        print("\n==== COLLECT ")
        ps.print_stats(1.0)
        print("\n ///")
        ps.print_callers()
    except:
        pass
    sys.exit(0)

# signal.signal(signal.SIGINT, end)
# signal.signal(signal.SIGKILL, end)
# signal.signal(signal.SIGPIPE, end)
