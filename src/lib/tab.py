
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

from meta.api import API_VERSION

class LayoutResult:
    def __init__(self, txt, highlighted = None, strong = None):
        self.txt = txt
        self.highlighted = highlighted or []
        self.strong = strong or []


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

    def hydrate_state(self, state, ignore = 0):
        """Take a cursor state and return the objects the it points to.
            ignore is a bitmask: 1 = bar, 2 = chord, 4 = note, for normal cursor state."""

        if type(state) == CursorState:
            return self.hydrate_state_normal(state, ignore)
        elif type(state) == CursorStateText:
            return self.hydrate_state_text(state)
        elif type(state) == CursorStateGeneric:
            return self.hydrate_state_generic(state)

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
            if children[i].is_bar:
                return children[i]

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

    def end_system(self, bar_frag, lines, vertical_offset):
        if bar_frag is None:
            return
        bar_lines = bar_frag.lines
        for i in range(len(bar_lines)):
            ind = i + vertical_offset
            if ind > len(lines) - 1:
                for j in range(ind - len(lines) + 1):
                    lines.append("")
            lines[ind] += bar_lines[i]

    def layout(self) -> LayoutResult:
        current_width = 0                   # the width of the current working system
        system_start = True                 # whether we're at a system start or not
        current_bar_num = 0                 # the current bar number, beginning at 0

        cursor_highlight = []
        cursor_highlight_strong = []

        padding_left = 1                    # global score padding
        padding_top = 1

        bar_padding_bottom = 1

        lines = ["" * padding_top]
        vertical_offset = 0 + padding_top   # how far 'down' we are currently
        current_bar_frag = None

        prev_element = None
        for child in self.children:
            if child.is_text:
                if prev_element and prev_element.is_bar:
                    self.end_system(current_bar_frag, lines, vertical_offset)
                    vertical_offset += current_bar_frag.height
                    current_bar_frag = None

                lines.append("")
                has_cursor = self.cursor.on_text and child == self.cursor.element
                laid_out = child.layout()
                line_lengths = child.line_lengths
                pos = 0
                for i in range(len(laid_out)):
                    line = laid_out[i]
                    length = line_lengths[i]
                    if has_cursor:
                        vert = vertical_offset + padding_top
                        horz = padding_left
                        if self.cursor.position < pos + length and self.cursor.position >= pos:
                            cursor_highlight_strong.append((vert, horz + self.cursor.position - pos))

                        for i in range(len(line)):
                            cursor_highlight.append((vert, horz + i))
                        pos += length
                    lines.append(line)
                    vertical_offset += 1
                lines.append("")
                vertical_offset += 2    # for top and below padding
                system_start = True
                current_width = 0
            elif child.is_bar:
                width = child.get_width(system_start)
                if current_width + width > self.max_width and not system_start:
                    current_width = width
                    self.end_system(current_bar_frag, lines, vertical_offset)
                    vertical_offset += current_bar_frag.height + bar_padding_bottom
                    current_bar_frag = None
                    system_start = True
                else:
                    current_width += width

                # Layout bar
                bar_fragment = child.layout(system_start)

                # Decide where to put the cursor
                if self.cursor.on_chord and child == self.cursor.bar:
                    cols, curs_width = child.get_cursor_pos_and_width(system_start, self.cursor.element)
                    horizontal = padding_left + cols
                    vertical = bar_fragment.pos(LayoutAnchorName.HIGHEST_STRING)
                    if not system_start and current_bar_frag is not None:
                        horizontal += current_bar_frag.width
                    cursor_highlight_start = [vertical + vertical_offset, horizontal]
                    cursor_highlight_end = [vertical + vertical_offset + child.nstrings - 1, horizontal + curs_width - 1]

                    for y in range(cursor_highlight_start[0], cursor_highlight_end[0] + 1):
                        for x in range(cursor_highlight_start[1], cursor_highlight_end[1] + 1):
                            cursor_highlight.append((y, x))

                    # Specific string highlighting
                    bottom_line = vertical + vertical_offset + child.nstrings - 1
                    cursor_strong_highlight_start = [bottom_line - self.cursor.position, horizontal]
                    cursor_strong_highlight_end   = [bottom_line - self.cursor.position, horizontal + curs_width - 1]

                    for y in range(cursor_strong_highlight_start[0], cursor_strong_highlight_end[0] + 1):
                        for x in range(cursor_strong_highlight_start[1], cursor_strong_highlight_end[1] + 1):
                            cursor_highlight_strong.append((y, x))

                if current_bar_frag is None:
                    current_bar_frag = bar_fragment
                else:
                    current_bar_frag = current_bar_frag.match_with(bar_fragment)

                system_start = False
                current_bar_num += 1

            prev_element = child

        self.end_system(current_bar_frag, lines, vertical_offset)

        txt = "\n".join([" " * padding_left + x for x in lines])
        return LayoutResult(txt, cursor_highlight, cursor_highlight_strong)

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
