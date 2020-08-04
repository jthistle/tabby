
from util.logger import logger

import synth.sf2.decode as decode
from .exceptions import SoundfontException, SoundfontReadException, SoundfontIncompatibleVersion
from .riff_reader import RiffReader
from .sample import Sample
from .instrument import Instrument
from .bag import Bag
from .generator import Generator
from .modulator import Modulator
from .preset import Preset


def records(hydra, ident, size, ignore_terminating = False):
    data = hydra.child(ident).data
    if len(data) % size != 0:
        raise SoundfontReadException("'{}' sub-chunk is invalid length ({})".format(ident, len(data)))

    for i in range(len(data) // size - (1 if ignore_terminating else 0)):
        yield data[i * size:(i + 1) * size]


class Soundfont:
    def __init__(self, file):
        self.reader = RiffReader(file)
        self.samples = []
        self.instruments = []
        self.bags = []
        self.generators = []
        self.modulators = []
        self.presets = []
        self.preset_bags = []
        self.preset_gens = []
        self.preset_mods = []
        try:
            self.chunk = self.reader.read()
            # print(self.chunk)

            self.get_metadata()
            self.raw_samples = self.chunk.child("sdta").child("smpl").data
            self.interpret_hydra()
        except SoundfontException as e:
            msg = "Corrupt soundfont: {}".format(e.message)
            logger.error(msg)
            print(msg)
            raise e

    def get_metadata(self):
        self.name = decode.ascii_str(self.chunk.child("INFO").child("INAM").data)

        version_data = self.chunk.child("INFO").child("ifil").data
        major = decode.WORD(version_data[:2])
        minor = decode.WORD(version_data[2:4])
        self.version = "{}.{:02d}".format(major, minor)

        if not (major == 2 and minor <= 1):
            return SoundfontIncompatibleVersion("Soundfont version {} is not supported by this synth".format(self.version))


    def bake_bags(self):
        """
        Since bags and instruments use ids that end at the id of the next bag/instrument,
        we need to wait until we've read all of them before we can assign references to generators
        or modulators.
        """
        for i in range(len(self.bags) - 1):
            current = self.bags[i]
            nxt = self.bags[i + 1]
            current.gens = self.generators[current.gen_ndx:nxt.gen_ndx]
            current.mods = self.modulators[current.mod_ndx:nxt.mod_ndx]

    def bake_instruments(self):
        for i in range(len(self.instruments) - 1):
            current = self.instruments[i]
            nxt = self.instruments[i + 1]
            current.bags = self.bags[current.bag_ndx:nxt.bag_ndx]

    def bake_preset_bags(self):
        for i in range(len(self.preset_bags) - 1):
            current = self.preset_bags[i]
            nxt = self.preset_bags[i + 1]
            current.gens = self.preset_gens[current.gen_ndx:nxt.gen_ndx]
            current.mods = self.preset_mods[current.mod_ndx:nxt.mod_ndx]

    def bake_presets(self):
        for i in range(len(self.presets) - 1):
            current = self.presets[i]
            nxt = self.presets[i + 1]
            current.bags = self.preset_bags[current.bag_ndx:nxt.bag_ndx]

    def interpret_hydra(self):
        hydra = self.chunk.child("pdta")

        # Samples
        for smpl in records(hydra, "shdr", 46):
            new_samp = Sample.from_raw(smpl, self.raw_samples)
            if new_samp is not None:
                self.samples.append(new_samp)

        # Instrument zone generators
        for gen in records(hydra, "igen", 4, ignore_terminating=True):
            new_gen = Generator.from_raw(gen)
            if new_gen is not None:
                self.generators.append(new_gen)

        # Instrument zone modulators
        for mod in records(hydra, "imod", 10, ignore_terminating=True):
            new_mod = Modulator.from_raw(mod)
            if new_mod is not None:
                self.modulators.append(new_mod)

        # Bags (instrument zones)
        for bag in records(hydra, "ibag", 4):
            new_bag = Bag.from_raw(bag, False)
            if new_bag is not None:
                self.bags.append(new_bag)

        self.bake_bags()

        # Instruments
        for inst in records(hydra, "inst", 22):
            new_inst = Instrument.from_raw(inst)
            if new_inst is not None:
                self.instruments.append(new_inst)

        self.bake_instruments()

        # Now onto Pxxx headers
        # Preset zone generators
        for gen in records(hydra, "pgen", 4, ignore_terminating=True):
            new_gen = Generator.from_raw(gen)
            if new_gen is not None:
                self.preset_gens.append(new_gen)

        # Preset zone modulators
        for mod in records(hydra, "pmod", 10, ignore_terminating=True):
            new_mod = Modulator.from_raw(mod)
            if new_mod is not None:
                self.preset_mods.append(new_mod)

        # Preset bags
        for pbag in records(hydra, "pbag", 4):
            new_pbag = Bag.from_raw(pbag, True)
            if new_pbag is not None:
                self.preset_bags.append(new_pbag)

        self.bake_preset_bags()

        # Presets
        for preset in records(hydra, "phdr", 38):
            new_preset = Preset.from_raw(preset)
            if new_preset is not None:
                self.presets.append(new_preset)

        self.bake_presets()

    def presets_list_user(self):
        res = ""
        for p in self.presets:
            res += "{:03d}:{:03d}: {}\n".format(p.bank, p.preset_num, p.name)
        return res

    def __str__(self):
        return """Soundfont '{}' on version {}.
- {} samples
- {} instruments
- {} instrument generators
- {} instrument modulators
- {} instrument zones
- {} presets
- {} preset generators
- {} preset modulators
- {} preset zones""".format(
            self.name, self.version, len(self.samples), len(self.instruments), len(self.generators), len(self.modulators), len(self.bags),
            len(self.presets), len(self.preset_gens), len(self.preset_mods), len(self.preset_bags)
        )
