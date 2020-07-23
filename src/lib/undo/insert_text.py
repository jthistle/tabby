
from .undo_action import UndoAction
from lib.text import Text


class UndoInsertText(UndoAction):
    def __init__(self, state, value):
        self.state = state
        self.value = value
        super().__init__("add text")

    def redo(self, tab):
        new_el = Text(tab, self.value)
        tab.children.insert(self.state.element, new_el)

    def undo(self, tab):
        del tab.children[self.state.element]

