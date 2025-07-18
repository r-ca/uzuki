from uzuki.input.keycodes import Key

class InputHandler:
    """生キーコード取得とモードへの振り分け"""
    def __init__(self, screen):
        self.screen = screen

    def handle(self, raw_code: int):
        key = Key.from_code(raw_code)
        if key:
            self.screen.mode.handle_key(key)
