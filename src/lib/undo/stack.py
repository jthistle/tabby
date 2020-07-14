
from config import UNDO_STACK_LIMIT

class UndoStack:
    def __init__(self, tab):
        self.tab = tab
        self.actions = []
        self.position = -1

    def do(self, action):
        self.actions = self.actions[:self.position + 1]
        if len(self.actions) == UNDO_STACK_LIMIT:
            del self.actions[0]
            self.position -= 1

        self.actions.append(action)

    def redo(self):
        if self.position >= len(self.actions) - 1:
            return False, None

        action = self.actions[self.position + 1]
        action.redo(self.tab)
        self.position += 1
        return True, action

    def undo(self):
        """Returns result, UndoAction"""
        if self.position < 0:
            return False, None

        action = self.actions[self.position]
        action.undo(self.tab)
        self.position -= 1
        return True, action
