
from .layout import LayoutAnchorName
from .element import ElementBase, ElementType
from .bar import Bar
from .tuning import Tuning
from .text import Text
from .cursor import Cursor
from util.logger import logger
from .undo.stack import UndoStack
from .tab_meta import TabMeta
from .undo.cursor_state import CursorState
from .undo.cursor_state_text import CursorStateText
from .undo.cursor_state_generic import CursorStateGeneric
from .undo.cursor_state_annotation import CursorStateAnnotation

from meta.api import API_VERSION


class Tab(ElementBase):
    def __init__(self):
        super().__init__(ElementType.TAB)
        self.default_tuning = Tuning()
        self.children = [Bar(self)] + [Text(self, "The quick bro=wn fox jumps. Over the lazy! Dog!\nLorem    ipsum   dolar.")] + [Bar(self) for i in range(12)]
        self.max_width = 100
        self.cursor = Cursor(self)
        self.undo_stack = UndoStack(self)
        self.meta = TabMeta(API_VERSION, "Untitled")

    def do(self, action):
        self.undo_stack.do(action)
        self.undo_stack.redo()

    def hydrate_state_normal(self, state, ignore):
        bar = chord = note = None
        use = ~ignore

        if use & 0b1:
            bar = self.element(state.bar)
        if use & 0b10 and bar is not None:
            chord = bar.chord(state.chord)
        if use & 0b100 and chord is not None:
            note = chord.get_note(state.string)

        return bar, chord, note

    def hydrate_state_text(self, state):
        text = self.element(state.text)
        position = state.position

        return text, position

    def hydrate_state_generic(self, state):
        element = self.element(state.element)
        position = state.position

        return element, position

    def hydrate_state_annotation(self, state):
        bar = self.element(state.bar)
        chord = bar.chord(state.chord)
        annotation = chord.annotation
        position = state.position

        return annotation, position

    def hydrate_state(self, state, ignore = 0):
        """Take a cursor state and return the objects the it points to.
            ignore is a bitmask: 1 = bar, 2 = chord, 4 = note, for normal cursor state."""

        if type(state) == CursorState:
            return self.hydrate_state_normal(state, ignore)
        elif type(state) == CursorStateText:
            return self.hydrate_state_text(state)
        elif type(state) == CursorStateGeneric:
            return self.hydrate_state_generic(state)
        elif type(state) == CursorStateAnnotation:
            return self.hydrate_state_annotation(state)

        return None

    @property
    def bars(self):
        for child in self.children:
            if child.is_bar:
                yield child

    def element(self, n):
        return self.children[n]

    def bar(self, n):
        """Only use this if you want only a bar by index, for example the first one. In all other
        possible cases, please use `element`."""
        i = 0
        for child in self.children:
            if child.is_bar:
                if i == n:
                    return child
                i += 1
        return None

    def el_number(self, element):
        i = 0
        for i in range(len(self.children)):
            if self.children[i] == element:
                return i
        return None

    @property
    def nels(self):
        return len(self.children)

    @property
    def nbars(self):
        i = 0
        for child in self.children:
            if child.is_bar:
                i += 1

        return i

    def prev_bar(self, bar):
        found = -1
        for i in range(len(self.children)):
            if self.children[i].is_bar:
                found = i
                break

        if found <= 0:
            return None

        for i in range(found - 1, -1, -1):
            if self.children[i].is_bar:
                return self.children[i]

        return None

    def tuning_causes_loss(self, new_tuning: [str]):
        for bar in self.bars:
            if bar.tuning_causes_loss(new_tuning):
                return True
        return False

    def set_tuning(self, strings):
        new_tuning = Tuning(" ".join(strings))
        self.default_tuning = new_tuning
        for bar in self.bars:
            bar.set_tuning(new_tuning)
        self.cursor.string = len(strings) - 1

    def write(self):
        written_obj = {
            "meta": self.meta.write(),
            "max_width": self.max_width
        }

        tab_obj = []
        for child in self.children:
            tab_obj.append(child.write())

        written_obj["tab"] = tab_obj

        return written_obj

    def read(self, obj):
        self.meta.read(obj.get("meta"))
        self.max_width = obj.get("max_width")

        self.children = []
        for child in obj.get("tab"):
            type_name = child.get("type")
            new_obj = None
            if type_name == "Bar":
                new_obj = Bar(self)
            elif type_name == "Text":
                new_obj = Text(self, "")
            new_obj.read(child)
            self.children.append(new_obj)

        # Reset cursor
        self.cursor = Cursor(self)
