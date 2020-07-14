
from .undo_action import UndoAction

class UndoReplaceChord(UndoAction):
    def __init__(self, state, written_chord):
        self.state = state
        self.written_chord = written_chord
        super().__init__("replace chord")

    def redo(self, tab):
        _, chord, _ = tab.hydrate_state(self.state)
        prev_val = chord.write()

        chord.read(self.written_chord)

        self.written_chord = prev_val

    def undo(self, tab):
        self.redo(tab)
