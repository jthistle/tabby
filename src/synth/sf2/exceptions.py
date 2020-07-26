

class SoundfontException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class RiffReadException(SoundfontException):
    def __init__(self, *args):
        super().__init__(*args)


class SoundfontReadException(SoundfontException):
    def __init__(self, *args):
        super().__init__(*args)
