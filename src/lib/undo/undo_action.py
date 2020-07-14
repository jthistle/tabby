
class UndoAction:
    def __init__(self, undo_name = None):
        if undo_name is None:
            self.undo_name = "unnamed action"
        else:
            self.undo_name = undo_name
