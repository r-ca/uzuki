class BaseMode:
    """モード共通インターフェース"""
    def __init__(self, screen):
        self.screen = screen

    def handle_key(self, key):
        raise NotImplementedError
