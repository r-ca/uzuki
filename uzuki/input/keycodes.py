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
    TAB    = ord('\t')
    # Normal mode navigation keys
    H      = ord('h')
    J      = ord('j')
    K      = ord('k')
    L      = ord('l')
    I      = ord('i')
    X      = ord('x')
    O      = ord('o')
    A      = ord('a')
    P      = ord('p')
    Y      = ord('y')
    D      = ord('d')
    RAW    = None  # 特殊キー以外の全てのキー

    @staticmethod
    def from_code(code: int):
        for k in Key:
            if k.value == code:
                return k
        # 特殊キー以外は RAW として返す
        return Key.RAW
    
    @staticmethod
    def get_key_name(code: int) -> str:
        """キーコードからキー名を取得"""
        # 特殊キーのマッピング
        special_keys = {
            27: 'escape',
            10: 'enter',
            127: 'backspace',
            32: 'space',
            9: 'tab',
            curses.KEY_LEFT: 'left',
            curses.KEY_RIGHT: 'right',
            curses.KEY_UP: 'up',
            curses.KEY_DOWN: 'down',
        }
        
        if code in special_keys:
            return special_keys[code]
        
        # 印字可能文字
        if code < 256:
            return chr(code)
        
        return f'key_{code}'
