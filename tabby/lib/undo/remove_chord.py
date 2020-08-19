
from lib.chord import Chord
from .undo_action import UndoAction


class UndoRemoveChord(UndoAction):
    def __init__(self, state):
        super().__init__("remove chord")
        self.state = state
        self.initial_val = None

    def populate(self, chord):
        string_val_map = {}
        for note in chord.notes:
            string_val_map[note.string] = note.value
        return string_val_map

    def redo(self, tab):
        bar, chord, _ = tab.hydrate_state(self.state)
        self.initial_val = self.populate(chord)
        bar.delete_chord(self.state.chord)

    def undo(self, tab):
        if self.initial_val is None:
            return

        # Ignore note and chord
        bar, _, _ = tab.hydrate_state(self.state, 0b110)
        new_chord = bar.add_chord(self.state.chord, Chord(bar))
        for string in self.initial_val:
            new_chord.get_note(string).value = self.initial_val[string]
