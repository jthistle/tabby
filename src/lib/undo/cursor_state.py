
class CursorState:
    def __init__(self, cursor):
        self.string = cursor.note.string
        self.chord = cursor.chord_number
        self.bar = cursor.bar_number

    def __str__(self):
        return "<Cursor state> ({}, {}, {})".format(self.bar, self.chord, self.string)
