from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode

class InsertMode(BaseMode):
    def handle_key(self, key: Key, raw_code=None):
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
        elif key == Key.SPACE:
            if cur.col < len(buf.lines[cur.row]):
                buf.insert(cur.row, cur.col, ' ')
                cur.move(0, 1, buf)
        # Cursor navigation keys
        elif key == Key.LEFT:
            if cur.col > 0:
                cur.move(0, -1, buf)
        elif key == Key.RIGHT:
            if cur.col < len(buf.lines[cur.row]):
                cur.move(0, 1, buf)
        elif key == Key.UP:
            if cur.row > 0:
                cur.move(-1, 0, buf)
        elif key == Key.DOWN:
            if cur.row < len(buf.lines) - 1:
                cur.move(1, 0, buf)
        # Handle printable characters (RAW keys)
        elif key == Key.RAW and raw_code is not None:
            if raw_code < 256:  # 印字可能文字のみ
                char = chr(raw_code)
                buf.insert(cur.row, cur.col, char)
                cur.move(0, 1, buf)
