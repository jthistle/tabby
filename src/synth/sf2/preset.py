
import synth.sf2.decode as decode


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
