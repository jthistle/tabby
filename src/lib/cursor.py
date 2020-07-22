
from util.logger import logger
from .note import Note

class Cursor:
    def __init__(self, tab):
        self.tab = tab
        self.element = tab.children[0].chord(0)
        self.position = 0                # < generic position, e.g. string or pos in text

    @property
    def on_chord(self):
        return self.element.is_chord

    @property
    def on_text(self):
        return self.element.is_text

    @property
    def bar(self):
        assert self.on_chord
        return self.element.parent

    @property
    def note(self):
        assert self.on_chord
        return self.element.get_note(self.position)

    @property
    def el_number(self):
        assert not self.on_chord
        return self.tab.el_number(self.element)

    @property
    def bar_number(self):
        """Slightly confusingly, this is actually the _element_ number of the current bar,
        not the bar number."""
        assert self.on_chord
        return self.tab.el_number(self.bar)

    @property
    def chord_number(self):
        assert self.on_chord
        return self.bar.chord_number(self.element)

    def move(self, direction):
        """- for left, + for right"""
        last_type = self.element.type
        for i in range(abs(direction)):
            new_el = None
            if direction < 0:
                new_el = self.element.prev_el
            elif direction > 0:
                new_el = self.element.next_el

            if new_el is None:
                break
            self.element = new_el

        # Reset position to prevent out of bounds crash
        if self.element.type != last_type:
            self.position = 0

    def move_big(self, direction):
        """Moves around by the bar. -1 for left, +1 for right"""
        last = None
        last_major = self.bar if self.on_chord else self.element
        while self.element != last:
            last = self.element
            self.move(direction)
            new_major = self.bar if self.on_chord else self.element
            if new_major != last_major:
                break

    def move_string(self, direction):
        cur_bar = self.bar
        max_s = cur_bar.nstrings - 1
        self.position = min(max_s, max(0, self.position + direction))

    def move_text_pos(self, direction):
        max_pos = self.element.text_length - 1
        self.position = min(max_pos, max(0, self.position + direction))

    def move_position(self, direction):
        """+1 for up, -1 for down in chord mode, otherwise right and left respectively."""
        if self.on_chord:
            self.move_string(direction)
        elif self.on_text:
            self.move_text_pos(direction)
