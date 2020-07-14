
from .undo_action import UndoAction

class UndoReplaceChord(UndoAction):
    def __init__(self, state, chord):
        self.state = state
        self.string_val_map = self.populate(chord)
        super().__init__("replace chord")

    def populate(self, chord):
        string_val_map = {}
        for i in range(chord.parent.nstrings):
            string_val_map[i] = chord.get_note(i).value
        return string_val_map

    def redo(self, tab):
        bar, chord, _ = tab.hydrate_state(self.state)
        prev_val = self.populate(chord)

        for string in self.string_val_map:
            chord.get_note(string).value = self.string_val_map[string]

        self.string_val_map = prev_val

    def undo(self, tab):
        self.redo(tab)
