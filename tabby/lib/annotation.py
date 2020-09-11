
from .element import ElementBase, ElementType


class Annotation(ElementBase):
    def __init__(self, parent):
        super().__init__(ElementType.ANNOTATION)
        self.value = ""
        self.parent = parent

    @property
    def height(self):
        return len(self.lines)

    @property
    def width(self):
        return max(*[len(x) for x in self.lines])

    @property
    def lines(self):
        return self.value.split("\n")

    @property
    def empty(self):
        return self.value == ""

    def write(self):
        return {
            "type": "Annotation",
            "value": self.value
        }

    def read(self, obj):
        assert obj.get("type") == "Annotation"
        self.value = obj.get("value")

