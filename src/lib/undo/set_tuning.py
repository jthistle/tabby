
from .undo_action import UndoAction


class UndoSetTuning(UndoAction):
    def __init__(self, new_strings):
        super().__init__("edit tuning")
        self.new_strings = new_strings

    def redo(self, tab):
        # TODO allow setting of tuning for specific bar
        old_strings = tab.bar(0).tuning.strings
        tab.set_tuning(self.new_strings)
        self.new_strings = old_strings

    def undo(self, tab):
        self.redo(tab)
