
from util.logger import logger

# ignore chord and note. Not doing so causes a crash since there are problems
# caused by chord numbers changing.
IGNORE_MASK = 0b110

class UndoResizeBar:
    def __init__(self, state, mult):
        self.state = state
        self.mult = mult

    def redo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state, IGNORE_MASK)
        logger.info(self.state)
        bar.change_size(self.mult)

    def undo(self, tab):
        bar, _, _ = tab.hydrate_state(self.state, IGNORE_MASK)
        bar.change_size(1 / self.mult)
