
from .undo_action import UndoAction


class UndoDuplicateNote(UndoAction):
    def __init__(self, state, direction: int):
        self.state = state
        self.direction = direction

        self.prev = None
        super().__init__("duplicate note")

    def redo(self, tab):
        bar, chord, note = tab.hydrate_state(self.state)

        value = note.value
        if value == "":
            return

        self.prev = {}
        end = 0
        if self.direction == 1:
            end = bar.nstrings - 1

        initial = note.string
        for i in range(initial + self.direction, end + self.direction, self.direction):
            new_note = chord.get_note(i)
            self.prev[i] = new_note.value
            new_note.value = value

    def undo(self, tab):
        if self.prev == None:
            return

        bar, chord, _ = tab.hydrate_state(self.state)
        for string in self.prev:
            note = chord.get_note(string)
            note.value = self.prev[string]


