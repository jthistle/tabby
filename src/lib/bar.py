
from .chord import Chord
from .const import TICKS_IN_BAR
from util.logger import logger

DEFAULT_WIDTH = 16

class Bar:
    def __init__(self, parent):
        self.parent = parent
        self.chords = []            # < should be kept sorted
        self.tuning = self.parent.default_tuning

        for i in range(DEFAULT_WIDTH):
            self.chords.append(Chord(self))

    def size(self):
        return len(self.chords)

    def change_size(self, mult):
        """If >1, mult must be an int. If <1, mult must be a rational number in the form 1/n, where n is an int."""
        if mult > 1:
            # logger.info("Initial size: {}".format(self.size()))
            # logger.info("{} to {}, step {}".format(1, self.size() * 2, mult))
            for i in range(1, self.size() * mult, mult):
                # logger.info("{}".format(i))
                self.chords.insert(i, Chord(self))
            # logger.info("Final size: {}".format(self.size()))
        elif mult < 1:
            spacing = int(1 / mult)
            for i in range(self.size() - 1, spacing - 2, -spacing):
                del self.chords[i]

    def nstrings(self):
        return len(self.tuning.strings)

    def nchords(self):
        return len(self.chords)

    def get_width(self, is_system_start):
        width = 0
        for chord in self.chords:
            width += chord.get_width()

        # 2 for padding either side, 1 for end barline, 2 if system start for tuning and start barline
        return width + 2 + 1 + (self.tuning.get_width() + 1 if is_system_start else 0)

    def get_height(self):
        return self.nstrings()

    def layout(self, is_system_start) -> [str]:
        lines = []
        tuning_width = self.tuning.get_width()
        for i in range(self.nstrings()):
            line = []

            if is_system_start:
                line.append(self.tuning.at(i).ljust(tuning_width, " "))
                line.append("|")

            # Initial padding
            line.append("-")
            lines.insert(0, line)

        # Render chords
        for chord in self.chords:
            chord_lines = chord.layout()
            for i in range(len(chord_lines)):
                lines[i] += chord_lines[i]

        for i in range(self.nstrings()):
            # Final padding
            lines[i].append("-")
            lines[i].append("|")

        return ["".join(line) for line in lines]

    def get_cursor_pos_and_width(self, is_system_start, cursor_chord):
        """Returns (`pos`, `width`), where:
            - pos: the position of the cursor relative to the start of the bar, in columns
            - width: the horizontal width of the cursor"""
        internal_columns = 0
        width = 1
        for chord in self.chords:
            if chord == cursor_chord:
                width = chord.get_width()
                break
            internal_columns += chord.get_width()

        pos = 1 + (self.tuning.get_width() + 1 if is_system_start else 0) + internal_columns
        return pos, width

    def chord(self, n):
        return self.chords[n]

    def chord_number(self, chord):
        return self.chords.index(chord)

    def add_chord(self, n, chord):
        self.chords.insert(n, chord)
        return chord

    def delete_chord(self, n):
        del self.chords[n]

    def next_bar(self):
        my_ind = self.parent.bar_number(self)
        if my_ind == self.parent.nbars() - 1:
            return None

        return self.parent.bar(my_ind + 1)

    def prev_bar(self):
        my_ind = self.parent.bar_number(self)
        if my_ind == 0:
            return None

        return self.parent.bar(my_ind - 1)

    def tuning_causes_loss(self, new_tuning):
        if len(new_tuning) >= self.nstrings():
            return False
        new_max = len(new_tuning) - 1
        for chord in self.chords:
            if chord.tuning_causes_loss(new_max):
                return True
        return False

    def set_tuning(self, new_tuning):
        new_max = len(new_tuning.strings) - 1
        for chord in self.chords:
            for i in range(len(chord.notes) - 1, -1, -1):
                if chord.notes[i].string > new_max:
                    del chord.notes[i]
                else:
                    break
        self.tuning = new_tuning
