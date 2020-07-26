
from util.logger import logger

from .exceptions import SoundfontException, SoundfontReadException
from .riff_reader import RiffReader
from .sample import Sample
from .instrument import Instrument
from .bag import Bag
from .generator import Generator
from .modulator import Modulator


class Soundfont:
    def __init__(self, file):
        self.reader = RiffReader(file)
        self.samples = []
        self.instruments = []
        self.bags = []
        self.generators = []
        self.modulators = []
        try:
            self.chunk = self.reader.read()
            print(self.chunk)

            self.raw_samples = self.chunk.child("sdta").child("smpl").data
            self.interpret_hydra()
        except SoundfontException as e:
            msg = "Corrupt soundfont: {}".format(e.message)
            logger.error(msg)
            print(msg)
            raise e

    def bake_instruments(self):
        for i in range(len(self.instruments) - 1):
            current = self.instruments[i]
            nxt = self.instruments[i + 1]
            current.bags = self.bags[current.bag_ndx:nxt.bag_ndx]

    def interpret_hydra(self):
        hydra = self.chunk.child("pdta")

        # Samples
        sample_data = hydra.child("shdr").data
        if len(sample_data) % 46 != 0:
            raise SoundfontReadException("SHDR sub-chunk is invalid length")

        for i in range(len(sample_data) // 46):
            smpl = sample_data[i * 46:(i + 1) * 46]
            new_samp = Sample.from_raw(smpl, self.raw_samples)
            if new_samp is not None:
                self.samples.append(new_samp)

        # Instrument zone generators
        gen_data = hydra.child("igen").data
        if len(gen_data) % 4 != 0:
            raise SoundfontReadException("IGEN sub-chunk is invalid length")

        for i in range(len(gen_data) // 4):
            gen = gen_data[i * 4:(i + 1) * 4]
            new_gen = Generator.from_raw(gen)
            if new_gen is not None:
                self.generators.append(new_gen)

        # Instrument zone modulators
        mod_data = hydra.child("imod").data
        if len(mod_data) % 10 != 0:
            raise SoundfontReadException("IMOD sub-chunk is invalid length")

        # -1 to ignore terminating record
        for i in range(len(mod_data) // 10 - 1):
            mod = mod_data[i * 10:(i + 1) * 10]
            new_mod = Modulator.from_raw(mod)
            if new_mod is not None:
                self.modulators.append(new_mod)

        # Bags (instrument zones)
        bag_data = hydra.child("ibag").data
        if len(bag_data) % 4 != 0:
            raise SoundfontReadException("IBAG sub-chunk is invalid length")

        # Again, -1 to ignore terminating record
        for i in range(len(bag_data) // 4 - 1):
            bag = bag_data[i * 4:(i + 1) * 4]
            new_bag = Bag.from_raw(bag, self.generators, self.modulators)
            if new_bag is not None:
                self.bags.append(new_bag)

        # Instruments
        inst_data = hydra.child("inst").data
        if len(inst_data) % 22 != 0:
            raise SoundfontReadException("INST sub-chunk is invalid length")

        for i in range(len(inst_data) // 22):
            inst = inst_data[i * 22:(i + 1) * 22]
            new_inst = Instrument.from_raw(inst)
            if new_inst is not None:
                self.instruments.append(new_inst)

        self.bake_instruments()

        for inst in self.instruments:
            print(inst)
