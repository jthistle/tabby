
from .element import ElementBase, ElementType

class Text(ElementBase):
    def __init__(self, parent, value):
        super().__init__(ElementType.TEXT)
        self.parent = parent
        self.value = value

    @property
    def next_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == self.parent.nels - 1:
            return None

        return self.parent.element(my_ind + 1).first

    @property
    def prev_el(self):
        my_ind = self.parent.el_number(self)
        if my_ind == 0:
            return None

        return self.parent.element(my_ind - 1).last

    @property
    def text_length(self):
        return len(self.value.replace("\n", ""))

    def layout(self):
        return self.value.split("\n")

    def write(self):
        return {
            "type": "Text",
            "value": self.value
        }

    def read(self, obj):
        assert obj.get("type") == "Text"

        self.value = obj.get("value")
