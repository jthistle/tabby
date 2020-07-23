
class CursorStateGeneric:
    def __init__(self, cursor):
        if cursor.on_chord:
            self.element = cursor.bar_number
        else:
            self.element = cursor.el_number
        self.position = cursor.position

    def __str__(self):
        return "<Generic cursor state> ({}, {})".format(self.element, self.position)
