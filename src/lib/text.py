
class Text:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

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
