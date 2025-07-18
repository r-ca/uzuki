class Cursor:
    """カーソル位置(row, col)管理"""
    def __init__(self):
        self.row = 0
        self.col = 0
        self.on_move = None  # 移動通知コールバック

    def set_move_callback(self, callback):
        """移動通知コールバックを設定"""
        self.on_move = callback

    def _notify_move(self):
        """移動を通知"""
        if self.on_move:
            self.on_move()

    def move(self, d_row: int, d_col: int, buffer):
        old_row, old_col = self.row, self.col
        self.row = max(0, min(self.row + d_row, len(buffer.lines)-1))
        line_len = len(buffer.lines[self.row])
        self.col = max(0, min(self.col + d_col, line_len))
        
        # 位置が実際に変更された場合のみ通知
        if (old_row, old_col) != (self.row, self.col):
            self._notify_move()
