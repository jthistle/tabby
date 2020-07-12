
class UndoDuplicateNote:
    def __init__(self, state, direction: int):
        self.state = state
        self.direction = direction

        self.prev = None

    def redo(self, tab):
        bar = tab.bar(self.state.bar)
        chord = bar.chord(self.state.chord)
        note = chord.get_note(self.state.string)

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

        bar = tab.bar(self.state.bar)
        chord = bar.chord(self.state.chord)
        for string in self.prev:
            note = chord.get_note(string)
            note.value = self.prev[string]


