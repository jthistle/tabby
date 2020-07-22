

from .undo_action import UndoAction


class UndoDeleteChar(UndoAction):
    def __init__(self, state, offset):
        self.state = state
        self.offset = offset
        self.saved_char = None
        super().__init__("delete text")

    def redo(self, tab):
        text, position = tab.hydrate_state(self.state)
        use_pos = position + self.offset

        chars = list(text.value)
        self.saved_char = chars[use_pos]
        del chars[use_pos]
        text.value = "".join(chars)

    def undo(self, tab):
        text, position = tab.hydrate_state(self.state)

        chars = list(text.value)
        chars.insert(position + self.offset, self.saved_char)
        text.value = "".join(chars)
