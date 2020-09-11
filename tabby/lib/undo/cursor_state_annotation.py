
class CursorStateAnnotation:
    def __init__(self, cursor):
        assert cursor.on_annotation
        self.position = cursor.position
        chord = cursor.element.parent
        bar  = chord.parent
        self.chord = bar.chord_number(chord)
        self.bar = cursor.tab.el_number(bar)

    def __str__(self):
        return "<Annotation cursor state> ({}, {}, {})".format(self.bar, self.chord, self.position)
