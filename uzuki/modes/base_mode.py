class BaseMode:
    """モード共通インターフェース"""
    def __init__(self, screen, mode_name):
        self.screen = screen
        self.mode_name = mode_name

    def handle_default(self, key_info):
        """デフォルトのキー処理（サブクラスでオーバーライド）"""
        pass
    
    def get_action_handlers(self):
        """アクションハンドラーを取得（サブクラスでオーバーライド）"""
        return {}
