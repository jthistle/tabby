
from .bar import Bar
from .tuning import Tuning
from .text import Text
from .cursor import Cursor
from util.logger import logger
from .undo.stack import UndoStack

class LayoutResult:
    def __init__(self, txt, highlighted = None, strong = None):
        self.txt = txt
        self.highlighted = highlighted or []
        self.strong = strong or []


class Tab:
    def __init__(self):
        self.default_tuning = Tuning()
        self.children = [Bar(self)] + [Text(self, "Hello, world!")] + [Bar(self) for i in range(12)]
        self.max_width = 100
        self.cursor = Cursor(self, self.bar(0).chord(0))
        self.undo_stack = UndoStack(self)

    def do(self, action):
        self.undo_stack.do(action)
        self.undo_stack.redo()

    def hydrate_state(self, state):
        """Take a cursor state and return the objects the it points to."""
        bar = self.bar(state.bar)
        chord = bar.chord(state.chord)
        note = chord.get_note(state.string)

        return bar, chord, note

    def bars(self):
        for child in self.children:
            if type(child) == Bar:
                yield child

    def bar(self, n):
        i = 0
        for child in self.children:
            if type(child) == Bar:
                if i == n:
                    return child
                i += 1

        return None

    def bar_number(self, bar):
        i = 0
        for child in self.children:
            if type(child) == Bar:
                if child == bar:
                    return i
                i += 1
        return None

    def nbars(self):
        i = 0
        for child in self.children:
            if type(child) == Bar:
                i += 1

        return i

    def prev_bar(self, bar):
        found = -1
        for i in range(len(self.children)):
            if type(self.children[i]) == Bar:
                found = i
                break

        if found <= 0:
            return None

        for i in range(found - 1, -1, -1):
            if type(children[i]) == Bar:
                return children[i]

        return None

    def tuning_causes_loss(self, new_tuning: [str]):
        for bar in self.bars():
            if bar.tuning_causes_loss(new_tuning):
                return True
        return False

    def set_tuning(self, strings):
        new_tuning = Tuning(" ".join(strings))
        self.default_tuning = new_tuning
        for bar in self.bars():
            bar.set_tuning(new_tuning)
        self.cursor.string = len(strings) - 1

    def layout(self) -> LayoutResult:
        current_width = 0                   # the width of the current working system
        system_start = True                 # whether we're at a system start or not
        current_bar_num = 0                 # the current bar number, beginning at 0

        cursor_highlight_start = [0, 0]     # line, column
        cursor_highlight_end = [0, 0]

        cursor_strong_highlight_start = [0, 0]
        cursor_strong_highlight_end = [0, 0]

        padding_left = 1                    # global score padding
        padding_top = 1

        bar_padding_bottom = 1

        lines = ["" * padding_top]
        vertical_offset = 0 + padding_top   # how far 'down' we are currently

        prev_element = None
        for child in self.children:
            element_type = type(child)
            if element_type == Text:
                if prev_element and type(prev_element) == Bar:
                    vertical_offset += prev_element.get_height()

                lines.append("")
                for line in child.layout():
                    lines.append(line)
                    vertical_offset += 1
                lines.append("")
                vertical_offset += 2    # for top and below padding
                system_start = True
                current_width = 0
            elif element_type == Bar:
                width = child.get_width(system_start)
                if current_width + width > self.max_width:
                    current_width = width
                    vertical_offset += child.get_height() + bar_padding_bottom
                    system_start = True
                else:
                    current_width += width

                # Layout bar
                bar_lines = child.layout(system_start)

                # Decide where to put the cursor
                if child == self.cursor.bar():
                    cols, curs_width = child.get_cursor_pos_and_width(system_start, self.cursor.chord)
                    horizontal = padding_left + cols
                    if not system_start:
                        horizontal += len(lines[vertical_offset])
                    cursor_highlight_start = [vertical_offset, horizontal]
                    cursor_highlight_end = [vertical_offset + child.nstrings() - 1, horizontal + curs_width - 1]

                    # Specific string highlighting
                    bottom_line = vertical_offset + child.nstrings() - 1
                    cursor_strong_highlight_start = [bottom_line - self.cursor.string, horizontal]
                    cursor_strong_highlight_end   = [bottom_line - self.cursor.string, horizontal + curs_width - 1]

                for i in range(len(bar_lines)):
                    ind = i + vertical_offset
                    if ind > len(lines) - 1:
                        for j in range(ind - len(lines) + 1):
                            lines.append("")
                    lines[ind] += bar_lines[i]

                system_start = False
                current_bar_num += 1

            prev_element = child

        highlighted = []
        for y in range(cursor_highlight_start[0], cursor_highlight_end[0] + 1):
            for x in range(cursor_highlight_start[1], cursor_highlight_end[1] + 1):
                highlighted.append((y, x))

        strong_highlighted = []
        for y in range(cursor_strong_highlight_start[0], cursor_strong_highlight_end[0] + 1):
            for x in range(cursor_strong_highlight_start[1], cursor_strong_highlight_end[1] + 1):
                strong_highlighted.append((y, x))

        txt = "\n".join([" " * padding_left + x for x in lines])
        return LayoutResult(txt, highlighted, strong_highlighted)



