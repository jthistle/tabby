
import synth.sf2.decode as decode
from .definitions import SFGenerator
from .defaults import SF_GEN_DEFAULTS


class Bag:
    gens = mods = None

    def __init__(self, gen_ndx, mod_ndx, is_preset):
        self.gen_ndx = gen_ndx
        self.mod_ndx = mod_ndx
        self.is_preset = is_preset

    @classmethod
    def from_raw(cls, bag, is_preset):
        # Soundfont 2.01 spec, 7.7
        gen_ndx = decode.WORD(bag[:2])
        mod_ndx = decode.WORD(bag[2:4])

        return cls(gen_ndx, mod_ndx, is_preset)

    @property
    def is_global(self):
        assert self.gens is not None
        if len(self.gens) == 0:
            return False
        if self.is_preset:
            return self.gens[-1].operation != SFGenerator.instrument
        else:
            return self.gens[-1].operation != SFGenerator.sampleID

    @property
    def key_range(self):
        assert self.gens is not None
        if self.gens[0].operation == SFGenerator.keyRange:
            return self.gens[0].amount
        return SF_GEN_DEFAULTS[SFGenerator.keyRange]

    @property
    def vel_range(self):
        assert self.gens is not None
        if self.gens[0].operation == SFGenerator.velRange:
            return self.gens[0].amount
        elif len(self.gens) > 1 and self.gens[1].operation == SFGenerator.velRange:
            return self.gens[1].amount
        return SF_GEN_DEFAULTS[SFGenerator.velRange]

    def applies_to(self, key, vel):
        return self.is_global or (self.key_range.contains(key) and self.vel_range.contains(vel))

    def instrument(self, instruments):
        assert self.is_preset and not self.is_global
        inst_gen = self.gens[-1]
        return inst_gen.instrument(instruments)

    def sample(self, samples):
        assert not self.is_preset and not self.is_global
        sample_gen = self.gens[-1]
        return sample_gen.sample(samples)

    def __str__(self):
        if self.gens == None and self.mods == None:
            return "Bag, gen id {}, mod id {}".format(
                self.gen_ndx, self.mod_ndx
            )

        gen_str = "\n- ".join([""] + [str(x) for x in self.gens])

        mods = [""]
        for m in self.mods:
            mods += str(m).split("\n")
        mod_str = "\n- ".join(mods)

        return "Bag{}, {} gens: {} \n{} mods: {}".format(
            (" (global)" if self.is_global else ""), len(self.gens), gen_str, len(self.mods), mod_str
        )
