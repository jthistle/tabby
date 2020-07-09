
DEFAULT_WIDTH = 16

class Bar:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.tuning = self.parent.default_tuning

        self.width = DEFAULT_WIDTH

    def nstrings(self):
        return len(self.tuning.strings)

    def get_width(self, is_system_start):
        # 2 for padding either side, 1 for end barline, 2 if system start for tuning and start barline
        return self.width + 2 + 1 + (2 if is_system_start else 0)

    def layout(self, is_system_start) -> [str]:
        lines = []
        for i in range(self.nstrings()):
            line = []

            if is_system_start:
                line.append(self.tuning.at(i))
                line.append("|")

            # Initial padding
            line.append("-")

            for j in range(self.width):
                line.append("-")

            # Final padding
            line.append("-")
            line.append("|")

            lines.insert(0, line)

        return ["".join(line) for line in lines]

    def get_cursor_pos(self, is_system_start, cursor_columns):
        """Returns the position of the cursor relative to the start of the bar"""
        return 1 + cursor_columns + (2 if is_system_start else 0)
