
class Text:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

    def layout(self):
       return self.value.split("\n")
