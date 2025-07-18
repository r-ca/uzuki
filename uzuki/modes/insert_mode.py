from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode

class InsertMode(BaseMode):
    def handle_key(self, key: Key):
        buf = self.screen.buffer
        cur = self.screen.cursor
        if key == Key.ESC:
            self.screen.mode = self.screen.normal_mode
        elif key == Key.ENTER:
            buf.split_line(cur.row, cur.col)
            cur.move(1, -cur.col, buf)
        elif key == Key.BACKSP:
            if cur.col > 0:
                buf.delete(cur.row, cur.col-1)
                cur.move(0, -1, buf)
        else:
            buf.insert(cur.row, cur.col, chr(key.value))
            cur.move(0, 1, buf)
