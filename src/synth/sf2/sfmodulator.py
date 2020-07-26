
from util.logger import logger
from .definitions import SFModPolarity, SFModDirection, SFGeneralController, SFModType


class SFModulator:
    def __init__(self, val):
        mod_type = val >> 10
        val ^= mod_type << 10

        polarity = val >> 9
        val ^= polarity << 9

        direction = val >> 8
        val ^= direction << 8

        use_general_cc = val >> 7
        val ^= use_general_cc << 7

        index = val

        self.polarity = SFModPolarity(polarity)
        self.direction = SFModDirection(direction)
        self.type = SFModType(mod_type)

        if use_general_cc == 0:
            try:
                self.controller = SFGeneralController(index)
            except ValueError:
                logger.warn("Invalid general controller value '{}' for modulator src".format(index))
                self.controller = SFGeneralController(-1)
        else:
            self.controller = index     # TODO SFMIDIController(index)

    @property
    def is_general_controller(self):
        return type(self.controller) == SFGeneralController

    def __str__(self):
        return "SFModulator, type {} controller {} polarity {} direction {}".format(
            self.type, self.controller, self.polarity, self.direction
        )
