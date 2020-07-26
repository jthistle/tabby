
import synth.sf2.decode as decode


class Bag:
    def __init__(self, gen, mod):
        self.gen = gen
        self.mod = mod


    @classmethod
    def from_raw(cls, bag, gens, mods):
        # Soundfont 2.01 spec, 7.7
        gen_ndx = decode.WORD(bag[:2])
        mod_ndx = decode.WORD(bag[2:4])

        gen = gens[gen_ndx]
        mod = mods[mod_ndx]

        return cls(gen, mod)

    def __str__(self):
        return "Bag, gen < {}  >  mod < {} >".format(
            self.gen, self.mod
        )
