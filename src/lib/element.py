
from enum import Enum

class ElementType(Enum):
    TAB = 1
    BAR = 2
    TEXT = 3
    CHORD = 4
    NOTE = 5

class ElementBase:
    def __init__(self, el_type):
        self.type = el_type

    @property
    def is_tab(self):
        return self.type == ElementType.TAB

    @property
    def is_bar(self):
        return self.type == ElementType.BAR

    @property
    def is_text(self):
        return self.type == ElementType.TEXT

    @property
    def is_chord(self):
        return self.type == ElementType.CHORD

    @property
    def is_note(self):
        return self.type == ElementType.NOTE
