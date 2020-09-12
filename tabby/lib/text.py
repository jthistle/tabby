
from .element import ElementBase, ElementType

class Text(ElementBase):
    """Text is a top-level tab element. It is also primitive.
    The value of the text can be any string incl. newlines.
    """
    def __init__(self, parent, value = ""):
        super().__init__(ElementType.TEXT)
        self.parent = parent
        self.value = value

    @property
    def next_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == self.parent.nels - 1:
            return None

        nxt = self.parent.element(my_ind + 1)
        if nxt.is_bar:
            nxt = nxt.first
        return nxt

    @property
    def prev_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == 0:
            return None

        prev = self.parent.element(my_ind - 1)
        if prev.is_bar:
            prev = prev.last
        return prev

    @property
    def text_length(self):
        return len(self.value) + 1

    @property
    def line_lengths(self):
        return [len(line) + 1 for line in self.value.split("\n")]

    def layout(self):
        return [" " if x == "" else x for x in self.value.split("\n")]

    def write(self):
        return {
            "type": "Text",
            "value": self.value
        }

    def read(self, obj):
        assert obj.get("type") == "Text"

        self.value = obj.get("value")
