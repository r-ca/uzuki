import curses
from enum import Enum

class Key(Enum):
    ESC    = 27
    ENTER  = 10
    BACKSP = 127
    SPACE = ord(' ')
    LEFT   = curses.KEY_LEFT
    RIGHT  = curses.KEY_RIGHT
    UP     = curses.KEY_UP
    DOWN   = curses.KEY_DOWN
    COLON  = ord(':')
    # Normal mode navigation keys
    H      = ord('h')
    J      = ord('j')
    K      = ord('k')
    L      = ord('l')
    I      = ord('i')
    X      = ord('x')
    O      = ord('o')
    RAW    = None  # 特殊キー以外の全てのキー

    @staticmethod
    def from_code(code: int):
        for k in Key:
            if k.value == code:
                return k
        # 特殊キー以外は RAW として返す
        return Key.RAW
