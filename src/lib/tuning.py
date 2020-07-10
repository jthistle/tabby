
from util.logger import logger

DEFAULT_TUNING = ["E", "A", "D", "G", "B", "e"]

class Tuning:
    def __init__(self, tuning_str = ""):
        if tuning_str != "":
            self.strings = self.parse_str(tuning_str)
        else:
            self.strings = DEFAULT_TUNING

    def get_width(self):
        m = 1
        for s in self.strings:
            m = max(len(s), m)
        return m

    def parse_str(self, val):
        strings = [x.strip()[:2] for x in val.upper().split()]
        final = []

        for string in strings:
            use_str = string
            if len(use_str) == 2:
                use_str = use_str.capitalize()      # bb -> Bb
            elif use_str in final:
                use_str = use_str.lower()
            final.append(use_str)

        return final

    def at(self, i):
        if i < 0 or i > len(self.strings):
            raise Exception("String index '{}' too high!".format(i))

        return self.strings[i]
