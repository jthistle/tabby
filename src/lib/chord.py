
from .element import ElementBase, ElementType
from .note import Note

class Chord(ElementBase):
    def __init__(self, parent):
        super().__init__(ElementType.CHORD)
        self.parent = parent
        self.notes = []             # keep ordered by ascending string

    def get_width(self):
        max_w = 1
        for note in self.notes:
            max_w = max(max_w, note.get_width())
        return max_w

    def layout(self) -> [str]:
        width = self.get_width()
        lines = ["-" * width] * self.parent.nstrings
        for note in self.notes:
            lines[note.string] = note.layout().ljust(width, "-")

        return [x for x in reversed(lines)]

    @property
    def empty(self):
        for note in self.notes:
            if note.value != "":
                return False
        return True

    def clear(self):
        self.notes = []

    def get_note(self, string):
        if string >= self.parent.nstrings or string < 0:
            return None

        for note in self.notes:
            if note.string == string:
                return note

        new_note = Note(self, string, "")
        i = 0
        for note in self.notes:
            if note.string > string:
                break
            i += 1
        self.notes.insert(i, new_note)
        return new_note

    @property
    def next_el(self):
        my_ind = self.parent.chords.index(self)
        if my_ind == self.parent.nchords - 1:
            next_bar = self.parent.next_el
            if next_bar is None:
                return None
            elif not next_bar.is_bar:
                return next_bar
            return next_bar.first

        return self.parent.chord(my_ind + 1)

    @property
    def prev_el(self):
        my_ind = self.parent.chords.index(self)
        if my_ind == 0:
            prev_bar = self.parent.prev_el
            if prev_bar is None:
                return None
            elif not prev_bar.is_bar:
                return prev_bar
            return prev_bar.last

        return self.parent.chord(my_ind - 1)

    def tuning_causes_loss(self, new_max):
        for note in self.notes:
            if note.string > new_max:
                return True
        return False

    def write(self):
        obj = {
            "type": "Chord",
            "notes": [x.write() for x in self.notes]
        }

        return obj

    def read(self, obj):
        assert obj.get("type") == "Chord"

        self.notes = []
        for note in obj.get("notes"):
            new_note = Note(self, 0, "")
            new_note.read(note)
            self.notes.append(new_note)
