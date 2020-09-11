

from .undo_action import UndoAction


class UndoInsertAnnotationCharacter(UndoAction):
    def __init__(self, state, char):
        self.state = state
        self.char = char
        super().__init__("insert annotation character")

    def redo(self, tab):
        annotation, position = tab.hydrate_state(self.state)

        chars = list(annotation.value)
        chars.insert(position, self.char)
        annotation.value = "".join(chars)

    def undo(self, tab):
        annotation, position = tab.hydrate_state(self.state)

        chars = list(annotation.value)
        del chars[position]
        annotation.value = "".join(chars)

