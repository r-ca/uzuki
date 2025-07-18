class History:
    """Undo/Redo 操作用スタック管理"""
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def record(self, state):
        self.undo_stack.append(state)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return None
        state = self.undo_stack.pop()
        self.redo_stack.append(state)
        return state

    def redo(self):
        if not self.redo_stack:
            return None
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        return state
