
class UndoClearChord:
    def __init__(self, state):
        self.state = state
        self.initial_val = None

    def populate(self, chord):
        string_val_map = {}
        for note in chord.notes:
            string_val_map[note.string] = note.value
        return string_val_map

    def redo(self, tab):
        _, chord, _ = tab.hydrate_state(self.state)
        self.initial_val = self.populate(chord)
        chord.notes = []

    def undo(self, tab):
        if self.initial_val is None:
            return

        _, chord, _ = tab.hydrate_state(self.state)
        for string in self.initial_val:
            chord.get_note(string).value = self.initial_val[string]
