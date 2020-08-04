
from util.logger import logger

import synth.sf2.decode as decode
from .definitions import SFGenerator, genAmountType, rangesType, sampleModes, get_gen_amount_type


class Generator:
    def __init__(self, operation, amount):
        self.operation = operation
        self.amount = amount

    def instrument(self, instruments):
        assert self.operation == SFGenerator.instrument
        return instruments[self.amount]

    def sample(self, samples_list):
        assert self.operation == SFGenerator.sampleID
        return samples_list[self.amount]

    @classmethod
    def from_raw(cls, inst):
        # Soundfont 2.01 spec, 7.9
        gen_id = decode.WORD(inst[:2])
        try:
            gen_oper = SFGenerator(gen_id)
        except ValueError:
            logger.warn("Ignoring undefined generator id {}".format(gen_id))
            return None

        amount = None
        amount_type = get_gen_amount_type(gen_oper)
        if amount_type == genAmountType.SHORT:
            amount = decode.SHORT(inst[2:4])
        elif amount_type == genAmountType.rangesType:
            raw_val = decode.WORD(inst[2:4])
            amount = rangesType(raw_val)
        elif amount_type == genAmountType.sampleModes:
            raw_val = decode.WORD(inst[2:4])
            amount = sampleModes(raw_val)
        elif amount_type == genAmountType.WORD:
            amount = decode.WORD(inst[2:4])

        return cls(gen_oper, amount)

    def __str__(self):
        return "Generator, operation {} @ {}".format(
            self.operation, self.amount
        )
