
from .element import ElementBase, ElementType

class Note(ElementBase):
    """A note is a child of a chord. It is a primitive object and has
    no children. Its value need not be a number, any string is acceptable.
    """
    def __init__(self, parent, string, value):
        super().__init__(ElementType.NOTE)
        self.parent = parent
        self.string = string        # 0 is bottom string
        self.value = value

    def layout(self):
        return self.value

    def get_width(self):
        return len(self.value)

    def write(self):
        obj = {
            "type": "Note",
            "string": self.string,
            "value": self.value,
        }

        return obj

    def read(self, obj):
        assert obj.get("type") == "Note"

        self.string = obj.get("string")
        self.value = obj.get("value")
