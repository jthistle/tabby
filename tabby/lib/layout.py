
from enum import Enum
from util.logger import logger

class LayoutAnchorName(Enum):
    HIGHEST_STRING = 1


class LayoutAnchor:
    def __init__(self, name: LayoutAnchorName, line: int):
        self.name = name
        self.line = line


class LayoutFragment:
    def __init__(self, lines: [str], anchors: [LayoutAnchor]):
        self.lines = lines
        self.anchors = anchors

    @property
    def lines(self):
        return self.__lines

    @lines.setter
    def lines(self, lines):
        self.__lines = lines
        self.width = 0
        for line in lines:
            self.width = max(self.width, len(line))

    @property
    def height(self):
        return len(self.lines)

    def pos(self, anchor_name):
        for anchor in self.anchors:
            if anchor.name == anchor_name:
                return anchor.line
        return None

    def form_corrected(self, top_diff, bottom_diff) -> 'LayoutFragment':
        new_lines = []
        offset = 0
        if top_diff < 0:
            offset = -top_diff
            for i in range(abs(top_diff)):
                new_lines.append(" " * self.width)

        new_lines += self.lines

        if bottom_diff > 0:
            for i in range(bottom_diff):
                new_lines.append(" " * self.width)

        new_anchors = []
        for anchor in self.anchors:
            new_anchor = LayoutAnchor(anchor.name, anchor.line + offset)
            new_anchors.append(new_anchor)

        return LayoutFragment(new_lines, new_anchors)

    def merge_with(self, other):
        assert len(self.lines) == len(other.lines)
        new_lines = []
        for i in range(len(self.lines)):
            new_lines.append(self.lines[i] + other.lines[i])

        return LayoutFragment(new_lines, self.anchors)

    def match_with(self, other: 'LayoutFragment') -> 'LayoutFragment':
        origin = None
        target = None
        for my_anchor in self.anchors:
            for other_anchor in other.anchors:
                if my_anchor.name == other_anchor.name:
                    origin = my_anchor
                    target = other_anchor

        if origin is None or target is None:
            return

        top_diff = origin.line - target.line
        bottom_diff =  (len(other.lines) - target.line) - (len(self.lines) - origin.line)
        new_origin = self.form_corrected(top_diff, bottom_diff)
        new_target = other.form_corrected(-top_diff, -bottom_diff)

        return new_origin.merge_with(new_target)

    def __str__(self):
        txt = [""]
        for i in range(len(self.lines)):
            txt.append(self.lines[i])
            for anchor in self.anchors:
                if anchor.line == i:
                    txt[i + 1] += " < {}".format(anchor.name)
        return "\n".join(txt)


class LayoutResult:
    def __init__(self, txt, highlighted = None, strong = None):
        self.txt = txt
        self.highlighted = highlighted or []
        self.strong = strong or []


class Layout:
    def __init__(self, tab):
        self.tab = tab

    def end_system(self, bar_frag, lines, vertical_offset):
        """Renders a layout fragment into the lines array."""
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
        cursor = self.tab.cursor
        for child in self.tab.children:
            if child.is_text:
                if prev_element and prev_element.is_bar:
                    self.end_system(current_bar_frag, lines, vertical_offset)
                    vertical_offset += current_bar_frag.height
                    current_bar_frag = None

                lines.append("")
                has_cursor = cursor.on_text and child == cursor.element
                laid_out = child.layout()
                line_lengths = child.line_lengths
                pos = 0
                for i in range(len(laid_out)):
                    line = laid_out[i]
                    length = line_lengths[i]
                    if has_cursor:
                        vert = vertical_offset + padding_top
                        horz = padding_left
                        if cursor.position < pos + length and cursor.position >= pos:
                            cursor_highlight_strong.append((vert, horz + cursor.position - pos))

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
                if current_width + width > self.tab.max_width and not system_start:
                    current_width = width
                    self.end_system(current_bar_frag, lines, vertical_offset)
                    vertical_offset += current_bar_frag.height + bar_padding_bottom
                    current_bar_frag = None
                    system_start = True
                else:
                    current_width += width

                # Layout bar
                cursor_selecting_annotation = cursor.on_annotation and child == cursor.bar
                must_empty_selected_annotation = False
                if cursor_selecting_annotation and cursor.element.empty:
                    cursor.element.value = " "
                    must_empty_selected_annotation = True

                bar_fragment = child.layout(system_start)

                # Decide where to put the cursor
                if cursor.on_chord and child == cursor.bar:
                    cols, curs_width = child.get_cursor_pos_and_width(system_start, cursor.element)
                    horizontal = padding_left + cols
                    vertical = bar_fragment.pos(LayoutAnchorName.HIGHEST_STRING)
                    if current_bar_frag is not None:
                        horizontal += current_bar_frag.width
                    cursor_highlight_start = [vertical + vertical_offset, horizontal]
                    cursor_highlight_end = [vertical + vertical_offset + child.nstrings - 1, horizontal + curs_width - 1]

                    for y in range(cursor_highlight_start[0], cursor_highlight_end[0] + 1):
                        for x in range(cursor_highlight_start[1], cursor_highlight_end[1] + 1):
                            cursor_highlight.append((y, x))

                    # Specific string highlighting
                    bottom_line = vertical + vertical_offset + child.nstrings - 1
                    cursor_strong_highlight_start = [bottom_line - cursor.position, horizontal]
                    cursor_strong_highlight_end   = [bottom_line - cursor.position, horizontal + curs_width - 1]

                    for y in range(cursor_strong_highlight_start[0], cursor_strong_highlight_end[0] + 1):
                        for x in range(cursor_strong_highlight_start[1], cursor_strong_highlight_end[1] + 1):
                            cursor_highlight_strong.append((y, x))
                elif cursor_selecting_annotation:
                    annotation = cursor.element
                    chord = cursor.element.parent
                    cols, _ = child.get_cursor_pos_and_width(system_start, chord)
                    horizontal = padding_left + cols
                    vertical = bar_fragment.pos(LayoutAnchorName.HIGHEST_STRING) - annotation.height
                    if current_bar_frag is not None:
                        horizontal += current_bar_frag.width

                    # Add annotation highlighting
                    annotation_lines = annotation.lines
                    for i in range(annotation.height):
                        for j in range(len(annotation_lines[i])):
                            cursor_highlight.append((i + vertical + vertical_offset, j + horizontal))

                    total_length = 0
                    for i in range(len(annotation_lines)):
                        line = annotation_lines[i]
                        total_length += len(line)
                        if cursor.position <= total_length:
                            cursor_highlight_strong.append((i + vertical + vertical_offset, horizontal + len(line) - (total_length - cursor.position)))
                            break

                if must_empty_selected_annotation:
                    cursor.element.value = ""

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
