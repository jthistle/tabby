
from util.logger import logger

import synth.sf2.decode as decode
from .definitions import SFGenerator


class Generator:
    def __init__(self, operation, amount):
        self.operation = operation
        self.amount = amount

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

        # Assuming all generators use signed short values may be wrong.
        # However, the spec doesn't provide any guidance as to which generators use
        # what type, so lets hope it's right.
        amount = decode.SHORT(inst[2:4])

        return cls(gen_oper, amount)

    def __str__(self):
        return "Generator, operation {} @ {}".format(
            self.operation, self.amount
        )
