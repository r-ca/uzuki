import curses

class Key:
    """キーコード処理クラス"""
    ESC = 27
    ENTER = 10
    BACKSPACE = 127
    SPACE = ord(' ')
    TAB = ord('\t')
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    RAW = None  # 特殊キー以外の全てのキー

    @staticmethod
    def from_code(code: int):
        """キーコードからKey定数を取得"""
        # 特殊キーの判定
        special_keys = [
            Key.ESC, Key.ENTER, Key.BACKSPACE, Key.SPACE, Key.TAB,
            Key.LEFT, Key.RIGHT, Key.UP, Key.DOWN
        ]
        
        if code in special_keys:
            return code
        else:
            return Key.RAW

    @staticmethod
    def get_key_name(code: int) -> str:
        """キーコードからキー名を取得"""
        # 特殊キーのマッピング
        special_keys = {
            Key.ESC: 'escape',
            Key.ENTER: 'enter',
            Key.BACKSPACE: 'backspace',
            Key.SPACE: 'space',
            Key.TAB: 'tab',
            Key.LEFT: 'left',
            Key.RIGHT: 'right',
            Key.UP: 'up',
            Key.DOWN: 'down',
        }
        
        if code in special_keys:
            return special_keys[code]
        
        # 印字可能文字
        if code < 256:
            return chr(code)
        
        return f'key_{code}'
