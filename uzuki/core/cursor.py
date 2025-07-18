class Cursor:
    """カーソル位置(row, col)管理"""
    def __init__(self):
        self.row = 0
        self.col = 0

    def move(self, d_row: int, d_col: int, buffer):
        self.row = max(0, min(self.row + d_row, len(buffer.lines)-1))
        line_len = len(buffer.lines[self.row])
        self.col = max(0, min(self.col + d_col, line_len))
