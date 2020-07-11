
class Note:
    def __init__(self, parent, string, value):
        self.parent = parent
        self.string = string        # 0 is bottom string
        self.value = value

    def layout(self):
        return self.value

    def get_width(self):
        return len(self.value)
