
class UndoSetNoteValue:
    def __init__(self, state, value: str):
        self.state = state
        self.value = value

    def redo(self, tab):
        bar = tab.bar(self.state.bar)
        chord = bar.chord(self.state.chord)
        note = chord.get_note(self.state.string)
        old_value = note.value
        note.value = self.value
        self.value = old_value

    def undo(self, tab):
        self.redo(tab)


