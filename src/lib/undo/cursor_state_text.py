
class CursorStateText:
    def __init__(self, cursor):
        assert cursor.on_text
        self.position = cursor.note.position
        self.text = cursor.text_number

    def __str__(self):
        return "<Text cursor state> ({}, {})".format(self.text, self.position)
