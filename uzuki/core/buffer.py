class Buffer:
    """行リストでテキストを管理"""
    def __init__(self):
        self.lines = ['']

    def insert(self, row: int, col: int, char: str):
        line = self.lines[row]
        self.lines[row] = line[:col] + char + line[col:]

    def delete(self, row: int, col: int):
        line = self.lines[row]
        if col < len(line):
            self.lines[row] = line[:col] + line[col+1:]

    def split_line(self, row: int, col: int):
        line = self.lines[row]
        self.lines[row] = line[:col]
        self.lines.insert(row+1, line[col:])
