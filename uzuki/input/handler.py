from uzuki.input.keycodes import Key

class KeyInfo:
    """キー情報を格納するクラス"""
    def __init__(self, raw_code: int):
        self.raw_code = raw_code
        self.key_name = Key.get_key_name(raw_code)
        self.char = chr(raw_code) if raw_code < 256 else None
        self.is_printable = raw_code < 256

class InputHandler:
    """生キーコード取得とモードへの振り分け"""
    def __init__(self, screen):
        self.screen = screen

    def handle(self, raw_code: int):
        """キー入力を処理"""
        key_info = KeyInfo(raw_code)
        self.screen.mode.handle_key_info(key_info)
