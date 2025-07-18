from uzuki.input.keycodes import Key

class InputHandler:
    """生キーコード取得とモードへの振り分け"""
    def __init__(self, screen):
        self.screen = screen

    def handle(self, raw_code: int):
        key = Key.from_code(raw_code)
        if key == Key.RAW:
            # RAWキーの場合、生のキーコードも渡す
            self.screen.mode.handle_key(key, raw_code)
        else:
            self.screen.mode.handle_key(key)
