
from .undo_action import UndoAction

class UndoInsertChord(UndoAction):
    def __init__(self, state):
        super().__init__("insert chord")
        self.state = state
        self.initial_val = None

    def redo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state)
        bar.insert_chord(self.state.chord + 1)      # insert AFTER cursor

    def undo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state)
        bar.delete_chord(self.state.chord + 1)
