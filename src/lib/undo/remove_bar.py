
from .undo_action import UndoAction
from lib.bar import Bar


class UndoRemoveBar(UndoAction):
    def __init__(self, state, bar):
        self.state = state
        self.saved_bar = bar.write()
        super().__init__("remove bar")

    def redo(self, tab):
        tab.cursor.move_away_big(1)
        del tab.children[self.state.bar]

    def undo(self, tab):
        new_bar = Bar(tab)
        tab.children.insert(self.state.bar, new_bar)
        new_bar.read(self.saved_bar)
