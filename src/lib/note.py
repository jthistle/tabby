
class Note:
    def __init__(self, string, value):
        self.string = string        # 0 is bottom string
        self.value = value

    def layout(self):
        return self.value

    def width(self):
        return len(self.value)
