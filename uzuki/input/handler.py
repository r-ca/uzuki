from uzuki.input.keycodes import Key

class KeyInfo:
    """キー情報を格納するクラス"""
    def __init__(self, raw_code: int):
        self.raw_code = raw_code
        self.key_name = Key.get_key_name(raw_code)
        self.char = chr(raw_code) if raw_code < 256 else None
        self.is_printable = raw_code < 256

class InputHandler:
    """キー情報作成クラス"""
    def __init__(self, screen):
        self.screen = screen

    def create_key_info(self, raw_code: int) -> KeyInfo:
        """KeyInfoオブジェクトを作成"""
        return KeyInfo(raw_code)
