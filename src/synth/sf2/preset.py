
import synth.sf2.decode as decode
from .defaults import DEFAULT_MODULATORS, SF_GEN_DEFAULTS
from .definitions import rangesType


class Preset:
    bags = None

    def __init__(self, name, preset_num, bank, bag_ndx):
        self.name = name
        self.preset_num = preset_num
        self.bank = bank
        self.bag_ndx = bag_ndx

    @classmethod
    def from_raw(cls, prst):
        # Soundfont 2.01 spec, 7.2
        name = decode.ascii_str(prst[:20])

        preset_num = decode.WORD(prst[20:22])
        bank_num = decode.WORD(prst[22:24])
        bag_ndx = decode.WORD(prst[24:26])

        # Unused but reserved values, don't read
        # nop_library = decode.DWORD(prst[26:30])
        # nop_genre = decode.DWORD(prst[30:34])
        # nop_morphology = decode.DWORD(prst[30:34])

        return cls(name, preset_num, bank_num, bag_ndx)

    def get_instrument(self, key, vel, instruments):
        for bag in self.bags:
            if bag.is_global or not bag.applies_to(key, vel):
                continue
            return bag.instrument(instruments)

    def get_gens_and_mods(self, key, vel, inst):
        # Init first with defaults
        gens = {}
        for operation in SF_GEN_DEFAULTS:
            gens[operation] = SF_GEN_DEFAULTS[operation]

        # Instrument zones are absolute
        mods = [x for x in DEFAULT_MODULATORS]
        for bag in inst.bags:
            if not bag.applies_to(key, vel):
                continue
            for gen in bag.gens:
                gens[gen.operation] = gen.amount

            # "A modulator, contained within a global instrument zone, that is identical
            # to a default modulator supersedes or replaces the default modulator."
            # "A modulator, that is contained in a local instrument zone, which is identical
            # to a default modulator or to a modulator in a global instrument zone supersedes
            # or replaces that modulator."
            for mod in bag.mods:
                for i in range(len(mods)):
                    if mods[i] == mod:
                        mods[i] = mod


        # Preset zones are additive
        max_v = 0x7fff
        min_v = -max_v
        preset_mods_global = []
        for bag in self.bags:
            if not bag.applies_to(key, vel):
                continue
            for gen in bag.gens:
                if type(gen.amount) == rangesType:
                    continue
                try:
                    gens[gen.operation] = min(max_v, max(min_v, gens[gen.operation] + gen.amount))
                except KeyError:
                    # Some gens like SFGenerator.instrument aren't considered.
                    continue

            if bag.is_global:
                preset_mods_global += bag.mods
            else:
                # "A modulator, contained within a local preset zone, that is identical to
                # a modulator in a global preset zone supersedes or replaces that modulator
                # in the global preset zone. That modulator then has its effects added to
                # the destination summing node of all zones in the given instrument."
                for mod in bag.mods:
                    for i in range(len(preset_mods_global)):
                        if preset_mods_global[i] == mod:
                            preset_mods_global[i] = mod

        mods += preset_mods_global

        return gens, mods

    def __str__(self):
        bags_str = "n/a"
        if self.bags is not None:
            bags = []
            for x in self.bags:
                bags += str(x).split("\n")
            bags_str = "\n- ".join(bags)

        return "Preset '{}' @ {:03d}:{:03d}, bags ({} from {}) = < {} >".format(
            self.name, self.bank, self.preset_num, len(self.bags) if self.bags is not None else "_", self.bag_ndx, bags_str
        )
