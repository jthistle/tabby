
from .bar import Bar
from .tuning import Tuning
from .text import Text
from util.logger import logger


class Tab:
    def __init__(self):
        self.default_tuning = Tuning()
        self.children = [Text(self, "Hello, world!")] + [Bar(self) for i in range(12)]
        self.max_width = 100
        logger.info("init tab")

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

    def layout(self) -> str:
        current_width = 0
        system_start = True

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

                bar_lines = child.layout(system_start)
                for i in range(len(bar_lines)):
                    ind = i + vertical_offset
                    if ind > len(lines) - 1:
                        for j in range(ind - len(lines) + 1):
                            lines.append("")
                    lines[ind] += bar_lines[i]

                system_start = False

        return "\n".join([" " * padding_left + x for x in lines])




