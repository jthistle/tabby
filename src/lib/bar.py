
from .chord import Chord
from .const import TICKS_IN_BAR

DEFAULT_WIDTH = 16

class Bar:
    def __init__(self, parent):
        self.parent = parent
        self.chords = []            # < should be kept sorted
        self.tuning = self.parent.default_tuning

        for i in range(DEFAULT_WIDTH):
            self.chords.append(Chord(self, i))

        ## DEBUG - testing
        chrd = self.chords[0]
        note = chrd.get_note(1)
        note.value = "12"

    def nstrings(self):
        return len(self.tuning.strings)

    def nchords(self):
        return len(self.chords)

    def get_width(self, is_system_start):
        width = 0
        for chord in self.chords:
            width += chord.width()

        # 2 for padding either side, 1 for end barline, 2 if system start for tuning and start barline
        return width + 2 + 1 + (2 if is_system_start else 0)

    def get_height(self):
        return self.nstrings()

    def layout(self, is_system_start) -> [str]:
        lines = []
        for i in range(self.nstrings()):
            line = []

            if is_system_start:
                line.append(self.tuning.at(i))
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
                width = chord.width()
                break
            internal_columns += chord.width()

        pos = 1 + (2 if is_system_start else 0) + internal_columns
        return pos, width

    def chord(self, n):
        return self.chords[n]

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

