
from .undo_action import UndoAction


class UndoSetNoteValue(UndoAction):
    def __init__(self, state, value: str):
        self.state = state
        self.value = value
        super().__init__("edit note")

    def redo(self, tab):
        bar, chord, note = tab.hydrate_state(self.state)

        old_value = note.value
        note.value = self.value
        self.value = old_value

    def undo(self, tab):
        self.redo(tab)


