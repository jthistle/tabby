
from .undo_action import UndoAction
from lib.bar import Bar


class UndoInsertBar(UndoAction):
    def __init__(self, state):
        self.state = state
        super().__init__("add bar")

    def redo(self, tab):
        new_el = Bar(tab)
        tab.children.insert(self.state.element + 1, new_el)

    def undo(self, tab):
        tab.cursor.move_away_big(1)
        del tab.children[self.state.element + 1]

