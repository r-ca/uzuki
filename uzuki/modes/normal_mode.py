from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode

class NormalMode(BaseMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.cmd_buf = ''

    def handle_key(self, key: Key):
        buf = self.screen.buffer
        cur = self.screen.cursor
        # h/j/k/l
        if key == Key.H:
            cur.move(0, -1, buf)
        elif key == Key.J:
            cur.move(1, 0, buf)
        elif key == Key.K:
            cur.move(-1, 0, buf)
        elif key == Key.L:
            cur.move(0, 1, buf)
        # i, x, o, :
        elif key == Key.I:
            self.screen.mode = self.screen.insert_mode
        elif key == Key.X:
            buf.delete(cur.row, cur.col)
        elif key == Key.O:
            buf.split_line(cur.row, cur.col)
            cur.move(1, -cur.col, buf)
            self.screen.mode = self.screen.insert_mode
        elif key == Key.COLON:
            self.cmd_buf = ''
            self.screen.mode = self.screen.command_mode
