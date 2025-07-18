class Buffer:
    """行リストでテキストを管理"""
    def __init__(self):
        self.lines = ['']
        self.on_change = None  # 変更通知コールバック

    def set_change_callback(self, callback):
        """変更通知コールバックを設定"""
        self.on_change = callback

    def _notify_change(self):
        """変更を通知"""
        if self.on_change:
            self.on_change()

    def insert(self, row: int, col: int, char: str):
        line = self.lines[row]
        self.lines[row] = line[:col] + char + line[col:]
        self._notify_change()

    def delete(self, row: int, col: int):
        line = self.lines[row]
        if col < len(line):
            self.lines[row] = line[:col] + line[col+1:]
            self._notify_change()

    def split_line(self, row: int, col: int):
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row+1, line[col:])
        self._notify_change()
