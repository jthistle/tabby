import curses


class Header:
    def __init__(self):
        self.width = curses.COLS
        self.win = curses.newwin(1, self.width)
        self.win.bkgd(" ", curses.A_REVERSE | curses.A_BOLD)
        self.filename = "Untitled"
        self.file_location = None

        # Initial update
        self.update()
        self.draw()

    def update(self):
        header_txt = self.filename + " - Tab Editor"
        self.win.addstr(0, (self.width - len(header_txt)) // 2, header_txt)

    def draw(self):
        self.win.refresh()

