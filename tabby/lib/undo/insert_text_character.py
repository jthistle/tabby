

from .undo_action import UndoAction


class UndoInsertTextCharacter(UndoAction):
    def __init__(self, state, char):
        self.state = state
        self.char = char
        super().__init__("insert text character")

    def redo(self, tab):
        text, position = tab.hydrate_state(self.state)

        chars = list(text.value)
        chars.insert(position, self.char)
        text.value = "".join(chars)

    def undo(self, tab):
        text, position = tab.hydrate_state(self.state)

        chars = list(text.value)
        del chars[position]
        text.value = "".join(chars)

