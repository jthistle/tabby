
from lib.chord import Chord
from lib.text import Text

class UndoAction:
    def __init__(self, undo_name = None):
        if undo_name is None:
            self.undo_name = "unnamed action"
        else:
            self.undo_name = undo_name

    def reset_cursor(self, tab):
        # This is kind of hacky because it relies on a member of the undo
        # action being named 'state', which isn't really standardised, it
        # just happens that it works at the moment. Consider a registration
        # system or taking a second state that will be confirmed to exist.
        if not self.state:
            return

        hydrated = tab.hydrate_state(self.state)
        for part in hydrated:
            if type(part) in (Chord, Text):
                tab.cursor.element = part
                break
