
from .layout import LayoutFragment, LayoutAnchor, LayoutAnchorName
from .element import ElementBase, ElementType
from .chord import Chord
from .const import TICKS_IN_BAR
from util.logger import logger

DEFAULT_WIDTH = 16

class Bar(ElementBase):
    def __init__(self, parent):
        super().__init__(ElementType.BAR)
        self.parent = parent
        self.chords = []            # < should be kept sorted
        self.tuning = self.parent.default_tuning

        for i in range(DEFAULT_WIDTH):
            self.chords.append(Chord(self))

    @property
    def size(self):
        return len(self.chords)

    def can_change_size(self, mult):
        return self.size * mult <= TICKS_IN_BAR

    def size_change_causes_loss(self, mult):
        if mult > 1:
            return False

        spacing = int(1 / mult)
        for i in range(self.size - 1, spacing - 2, -spacing):
            if not self.chords[i].empty:
                return True
        return False

    def change_size(self, mult):
        """If >1, mult must be an int. If <1, mult must be a rational number in the form 1/n, where n is an int."""
        if mult > 1:
            mult = int(mult)
            for i in range(1, self.size * mult, mult):
                self.chords.insert(i, Chord(self))
        elif mult < 1:
            spacing = int(1 / mult)
            for i in range(self.size - 1, spacing - 2, -spacing):
                del self.chords[i]

    @property
    def nstrings(self):
        return len(self.tuning.strings)

    @property
    def nchords(self):
        return len(self.chords)

    def get_width(self, is_system_start):
        width = 0
        for chord in self.chords:
            width += chord.get_width()

        # 2 for padding either side, 1 for end barline, 2 if system start for tuning and start barline
        return width + 2 + 1 + (self.tuning.get_width() + 1 if is_system_start else 0)

    def get_height(self):
        height = 0
        for chord in self.chords:
            height = max(height, chord.get_height())
        return height

    def layout(self, is_system_start) -> LayoutFragment:
        tuning_width = self.tuning.get_width()
        initial_lines = []
        for i in range(self.nstrings):
            line = ""

            if is_system_start:
                line += self.tuning.at(i).ljust(tuning_width, " ") + "|"

            # Initial padding
            line += "-"
            initial_lines.insert(0, line)

        final_frag = LayoutFragment(initial_lines, [LayoutAnchor(LayoutAnchorName.HIGHEST_STRING, 0)])

        # Render chords
        for chord in self.chords:
            final_frag = final_frag.match_with(chord.layout())

        end_lines = ["-|"] * self.nstrings
        end_frag = LayoutFragment(end_lines, [LayoutAnchor(LayoutAnchorName.HIGHEST_STRING, 0)])
        final_frag = final_frag.match_with(end_frag)

        return final_frag

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

    def insert_chord(self, n):
        new_chord = Chord(self)
        self.chords.insert(n, new_chord)

    @property
    def next_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == self.parent.nels - 1:
            return None

        return self.parent.element(my_ind + 1)

    @property
    def prev_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == 0:
            return None

        return self.parent.element(my_ind - 1)

    @property
    def first(self):
        return self.chords[0]

    @property
    def last(self):
        return self.chords[len(self.chords) - 1]

    def tuning_causes_loss(self, new_tuning):
        if len(new_tuning) >= self.nstrings:
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

    def write(self):
        obj = {
            "type": "Bar",
            "tuning": self.tuning.write(),
        }

        chords = []
        empty_count = 0
        for chord in self.chords:
            if chord.empty:
                empty_count += 1
                continue
            if empty_count > 0:
                chords.append({
                    "type": "EmptyChords",
                    "count": empty_count
                })
                empty_count = 0

            chords.append(chord.write())

        if empty_count > 0:
            chords.append({
                "type": "EmptyChords",
                "count": empty_count
            })

        obj["chords"] = chords
        return obj

    def read(self, obj):
        assert obj.get("type") == "Bar"
        self.tuning.read(obj.get("tuning"))

        self.chords = []
        for chord in obj.get("chords"):
            if chord.get("type") == "EmptyChords":
                for i in range(chord.get("count")):
                    self.chords.append(Chord(self))
                continue

            new_chord = Chord(self)
            new_chord.read(chord)
            self.chords.append(new_chord)
