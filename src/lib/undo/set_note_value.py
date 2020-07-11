
class UndoSetNoteValue:
    def __init__(self, bar: int, chord: int, string: int, value: str):
        self.bar = bar
        self.chord = chord
        self.string = string
        self.value = value

    def redo(self, tab):
        bar = tab.bar(self.bar)
        chord = bar.chord(self.chord)
        note = chord.get_note(self.string)
        old_value = note.value
        note.value = self.value
        self.value = old_value

    def undo(self, tab):
        self.redo(tab)


