import curses


class LineInput:
    def __init__(self, win, on_val_change, cursor_offset):
        self.val = ""
        self.win = win
        self.on_val_change = on_val_change
        self.cursor_offset = cursor_offset
        self.cursor_pos = 0

    def reset(self):
        self.cursor_pos = 0
        self.val = ""
        self.update_cursor()

    def update_cursor(self):
        self.win.move(0, self.cursor_offset + self.cursor_pos)

    def handle_input(self):
        key = self.win.getkey()
        if len(key) == 1:
            ord_val = ord(key)
            if ord_val == 27:    # ESC
                self.val = ""
                self.on_val_change(self.val)
                return False
            elif ord_val >= 32 and ord_val <= 126:
                self.val = self.val[:self.cursor_pos] + key + self.val[self.cursor_pos:]
                self.cursor_pos += 1
                self.on_val_change(self.val)
            elif key == "\n":
                # submit
                return False
        elif key == "KEY_LEFT":
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif key == "KEY_RIGHT":
            self.cursor_pos = min(len(self.val), self.cursor_pos + 1)
        elif key == "KEY_DC":
            if self.cursor_pos < len(self.val):
                self.val = self.val[:self.cursor_pos] + self.val[self.cursor_pos + 1:]
            self.on_val_change(self.val)
        elif key == "KEY_BACKSPACE":
            if self.cursor_pos > 0:
                self.val = self.val[:self.cursor_pos - 1] + self.val[self.cursor_pos:]
            self.on_val_change(self.val)
            self.cursor_pos -= 1

        self.update_cursor()

        return True
