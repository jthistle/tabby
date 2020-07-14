
from .undo_action import UndoAction

# ignore chord and note. Not doing so causes a crash since there are problems
# caused by chord numbers changing.
IGNORE_MASK = 0b110

class UndoResizeBar(UndoAction):
    def __init__(self, state, mult):
        super().__init__("resize bar")
        self.state = state
        self.mult = mult

    def redo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state, IGNORE_MASK)
        bar.change_size(self.mult)

    def undo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state, IGNORE_MASK)
        bar.change_size(1 / self.mult)
