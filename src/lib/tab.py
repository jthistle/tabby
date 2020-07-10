
from .bar import Bar
from .tuning import Tuning
from .text import Text
from .cursor import Cursor
from util.logger import logger


class LayoutResult:
    def __init__(self, txt, highlighted = None, strong = None):
        self.txt = txt
        self.highlighted = highlighted or []
        self.strong = strong or []


class Tab:
    def __init__(self):
        self.default_tuning = Tuning()
        self.children = [Text(self, "Hello, world!")] + [Bar(self) for i in range(12)]
        self.max_width = 100
        self.cursor = Cursor(self)

    def bar(self, n):
        i = 0
        for child in self.children:
            if type(child) == Bar:
                if i == n:
                    return child
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

    def layout(self) -> LayoutResult:
        current_width = 0
        system_start = True
        current_bar_num = 0

        cursor_highlight_start = [0, 0]     # line, column
        cursor_highlight_end = [0, 0]

        cursor_strong_highlight_start = [0, 0]
        cursor_strong_highlight_end = [0, 0]

        padding_left = 1
        padding_top = 1

        lines = ["" * padding_top]
        vertical_offset = 0 + padding_top

        current_val = ""
        for child in self.children:
            element_type = type(child)
            if element_type == Text:
                lines.append("")
                for line in child.layout():
                    lines.append(line)
                    vertical_offset += 1
                lines.append("")
                vertical_offset += 2    # for above and below padding
            elif element_type == Bar:
                width = child.get_width(system_start)
                if current_width + width > self.max_width:
                    current_width = width
                    vertical_offset += 8    # TODO this is bar height, should be got from bar layout in future
                    system_start = True
                else:
                    current_width += width

                # Layout bar
                bar_lines = child.layout(system_start)

                # Decide where to put the cursor
                if current_bar_num == self.cursor.bar():
                    cols = child.get_cursor_pos(system_start, self.cursor.column())
                    horizontal = padding_left + cols
                    if not system_start:
                        horizontal += len(lines[vertical_offset])
                    cursor_highlight_start = [vertical_offset, horizontal]
                    cursor_highlight_end = [vertical_offset + child.nstrings() - 1, horizontal]

                    # Specific string highlighting
                    bottom_line = vertical_offset + child.nstrings() - 1
                    cursor_strong_highlight_start = [bottom_line - self.cursor.string, horizontal]
                    cursor_strong_highlight_end   = [bottom_line - self.cursor.string, horizontal]

                for i in range(len(bar_lines)):
                    ind = i + vertical_offset
                    if ind > len(lines) - 1:
                        for j in range(ind - len(lines) + 1):
                            lines.append("")
                    lines[ind] += bar_lines[i]

                system_start = False
                current_bar_num += 1

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



