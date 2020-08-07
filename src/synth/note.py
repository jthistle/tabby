
from .samples_cache import data_to_samples
from .repitch import change_pitch, change_sample_point, change_sample_point_ratio, cents_to_ratio
from .sf2.definitions import SFGenerator, LoopType


COARSE_SIZE = 2 ** 15
BASE_SAMPLE_RATE = 44100


class Note:
    def __init__(self, key, on_vel, sample, gens, mods):
        self.sample = sample
        self.key = key
        self.on_vel = on_vel
        self.gens = gens
        self.mods = mods

        self.playback = None

        self.hard_pitch_diff = (self.key - self.sample.pitch) * 100 + self.sample.pitch_correction
        self.hard_pitch_diff += self.gens[SFGenerator.coarseTune] * 100 + self.gens[SFGenerator.fineTune]

        # We need to adjust everything to fit the sample rate in use
        sample_ratio = self.sample.sample_rate / BASE_SAMPLE_RATE
        self.total_ratio = sample_ratio * cents_to_ratio(self.hard_pitch_diff)

        offset_s = self.gens[SFGenerator.startAddrsOffset] + self.gens[SFGenerator.startAddrsCoarseOffset] * COARSE_SIZE
        offset_e = self.gens[SFGenerator.endAddrsOffset] + self.gens[SFGenerator.endAddrsCoarseOffset] * COARSE_SIZE

        offset_s = change_sample_point_ratio(offset_s, self.total_ratio)
        offset_e = change_sample_point_ratio(offset_e, self.total_ratio)

        self.sample_data = change_pitch(data_to_samples(sample.data), self.total_ratio)

        self.loop = None
        if self.gens[SFGenerator.sampleModes].loop_type in (LoopType.CONT_LOOP, LoopType.KEY_LOOP):
            self.loop = [change_sample_point_ratio(x, self.total_ratio) for x in self.sample.loop]

        self.loop[0] += self.gens[SFGenerator.startloopAddrsOffset] + self.gens[SFGenerator.startloopAddrsCoarseOffset] * COARSE_SIZE
        self.loop[1] += self.gens[SFGenerator.endloopAddrsOffset] + self.gens[SFGenerator.endloopAddrsCoarseOffset] * COARSE_SIZE

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

        self.playback = inter.play(self.sample_data, channels=1, loop=self.loop)

    def stop(self, inter):
        if self.loop is not None:
            inter.end_loop(self.playback)
