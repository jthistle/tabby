
from .undo_action import UndoAction
from lib.text import Text


class UndoRemoveText(UndoAction):
    def __init__(self, state, text):
        self.state = state
        self.saved_text = text.write()
        super().__init__("remove text")

    def redo(self, tab):
        tab.cursor.move_away(1)
        del tab.children[self.state.text]

    def undo(self, tab):
        new_text = Text(tab)
        tab.children.insert(self.state.text, new_text)
        new_text.read(self.saved_text)
