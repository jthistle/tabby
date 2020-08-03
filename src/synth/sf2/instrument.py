
import synth.sf2.decode as decode


class Instrument:
    def __init__(self, name, bag):
        self.name = name
        self.bag_ndx = bag
        self.bags = []

    @property
    def is_real(self):
        return self.name != "EOI"

    @classmethod
    def from_raw(cls, inst):
        # Soundfont 2.01 spec, 7.6
        name = decode.ascii_str(inst[:20])
        bag_ndx = decode.WORD(inst[20:22])

        return cls(name, bag_ndx)

    def get_sample(self, key, vel, samples):
        for bag in self.bags:
            if bag.is_global or not bag.applies_to(key, vel):
                continue
            return bag.sample(samples)

    def __str__(self):
        bags = []
        for x in self.bags:
            bags += str(x).split("\n")
        bags_str = "\n- ".join([""] + bags)
        return "Instrument '{}' starting at bag {}, total {} bags: {}".format(
            self.name, self.bag_ndx, len(self.bags), bags_str
        )
