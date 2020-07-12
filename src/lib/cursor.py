
from util.logger import logger
from .note import Note

class Cursor:
    def __init__(self, tab, initial_chord):
        self.tab = tab
        self.chord = initial_chord
        self.string = initial_chord.parent.nstrings() - 1

    def bar(self):
        return self.chord.parent

    def note(self):
        return self.chord.get_note(self.string)

    def bar_number(self):
        return self.chord.parent.parent.bar_number(self.chord.parent)

    def chord_number(self):
        return self.chord.parent.chord_number(self.chord)

    def move(self, direction):
        """- for left, + for right"""
        if direction < 0:
            for i in range(abs(direction)):
                self.chord = self.chord.prev_chord() or self.chord
        elif direction > 0:
            for i in range(direction):
                self.chord = self.chord.next_chord() or self.chord

    def move_big(self, direction):
        """Moves around by the bar. -1 for left, +1 for right"""
        if direction == -1:
            prev_bar = None
            if self.chord.parent.chord_number(self.chord) == 0:
                prev_bar = self.chord.parent.prev_bar()

            if not prev_bar:
                prev_bar = self.bar()
            self.chord = prev_bar.chord(0)
        elif direction == 1:
            next_bar = self.chord.parent.next_bar()
            if not next_bar:
                next_bar = self.bar()
            self.chord = next_bar.chord(0)

    def move_string(self, direction):
        """+1 for up, -1 for down"""
        cur_bar = self.bar()
        max_s = cur_bar.nstrings() - 1

        self.string = min(max_s, max(0, self.string + direction))

    def backspace(self):
        note = self.note()
        if note.value != "":
            note.value = note.value[:-1]

    def delete(self):
        note = self.note()
        if note.value != "":
            note.value = note.value[1:]

    def clear_note(self):
        self.note().value = ""
