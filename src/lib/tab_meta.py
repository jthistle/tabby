
class TabMeta:
    def __init__(self, api_version, name):
        self.api_version = api_version
        self.name = name

    def write(self):
        return {
            "api_version": self.api_version,
            "name": self.name,
        }

    def read(self, obj):
        self.api_version = obj.get("api_version")
        self.name = obj.get("name")
