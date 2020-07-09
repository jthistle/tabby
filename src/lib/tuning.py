
from util.logger import logger

DEFAULT_TUNING = ["E", "A", "D", "G", "B", "e"]

class Tuning:
    def __init__(self, tuning_str = ""):
        if tuning_str != "":
            self.strings = self.parse_str(tuning_str)
        else:
            self.strings = DEFAULT_TUNING

    def parse_str(self, val):
        strings = [x.strip() for x in val.capitalize().split()]
        final = []

        for string in strings:
            use_str = string
            if use_str in final:
                use_str = use_str.lower()
            final.append(use_str)

        return final

    def at(self, i):
        if i < 0 or i > len(self.strings):
            raise Exception("String index '{}' too high!".format(i))

        return self.strings[i]
