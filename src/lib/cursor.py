
from util.logger import logger

class Cursor:
    def __init__(self, tab):
        self.tab = tab
        self.position = [0, 0]      # bar, column

    def bar(self):
        return self.position[0]

    def column(self):
        return self.position[1]

    def move(self, direction):
        """-1 for left, +1 for left"""
        cur_bar = self.tab.bar(self.position[0])
        new_col = self.position[1] + direction
        new_bar = self.position[0]
        if new_col >= cur_bar.width or new_col < 0:
            new_bar += direction
            new_col = 0 if direction == 1 else cur_bar.width - 1
            if new_bar >= self.tab.nbars() or new_bar < 0:
                # Can't move further, no op
                return

        self.position = [new_bar, new_col]
