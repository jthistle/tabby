
class CursorState:
    def __init__(self, cursor):
        self.string = cursor.note().string
        self.chord = cursor.chord_number()
        self.bar = cursor.bar_number()
