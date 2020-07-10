
from .note import Note

class Chord:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.notes = []

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

    def get_note(self, string):
        for note in self.notes:
            if note.string == string:
                return note

        new_note = Note(string, "")
        self.notes.append(new_note)
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
