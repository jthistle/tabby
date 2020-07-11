
from .note import Note

class Chord:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.notes = []             # keep ordered by ascending string

    def width(self):
        max_w = 1
        for note in self.notes:
            max_w = max(max_w, note.width())
        return max_w

    def layout(self) -> [str]:
        width = self.width()
        lines = ["-" * width] * self.parent.nstrings()
        for note in self.notes:
            lines[note.string] = note.layout().ljust(width, "-")

        return [x for x in reversed(lines)]

    def clear(self):
        self.notes = []

    def get_note(self, string):
        if string >= self.parent.nstrings() or string < 0:
            return None

        for note in self.notes:
            if note.string == string:
                return note

        new_note = Note(string, "")
        i = 0
        for note in self.notes:
            if note.string > string:
                break
            i += 1
        self.notes.insert(i, new_note)
        return new_note

    def next_chord(self):
        my_ind = self.parent.chords.index(self)
        if my_ind == self.parent.nchords() - 1:
            bar = self.parent.next_bar()
            if bar is None:
                return None
            return bar.chord(0)

        return self.parent.chord(my_ind + 1)

    def prev_chord(self):
        my_ind = self.parent.chords.index(self)
        if my_ind == 0:
            bar = self.parent.prev_bar()
            if bar is None:
                return None
            return bar.chord(bar.nchords() - 1)

        return self.parent.chord(my_ind - 1)

    def tuning_causes_loss(self, new_max):
        for note in self.notes:
            if note.string > new_max:
                return True
        return False
