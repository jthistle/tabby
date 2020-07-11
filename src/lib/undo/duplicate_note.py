
class UndoDuplicateNote:
    def __init__(self, bar: int, chord: int, string: int, direction: int):
        self.bar = bar
        self.chord = chord
        self.string = string
        self.direction = direction

        self.prev = None

    def redo(self, tab):
        bar = tab.bar(self.bar)
        chord = bar.chord(self.chord)
        note = chord.get_note(self.string)

        value = note.value
        if value == "":
            return

        self.prev = {}
        end = 0
        if self.direction == 1:
            end = bar.nstrings() - 1

        initial = note.string
        for i in range(initial + self.direction, end + self.direction, self.direction):
            new_note = chord.get_note(i)
            self.prev[i] = new_note.value
            new_note.value = value

    def undo(self, tab):
        if self.prev == None:
            return

        bar = tab.bar(self.bar)
        chord = bar.chord(self.chord)
        for string in self.prev:
            note = chord.get_note(string)
            note.value = self.prev[string]


