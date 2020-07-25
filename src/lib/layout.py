
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
