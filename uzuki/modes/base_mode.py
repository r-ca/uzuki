class BaseMode:
    """モード共通インターフェース"""
    def __init__(self, screen, mode_name):
        self.screen = screen
        self.mode_name = mode_name

    def handle_key_info(self, key_info):
        """キー情報を処理"""
        # キーマップからアクションを取得
        action = self.screen.keymap.get_action(self.mode_name, key_info.key_name)
        if action:
            action()
        else:
            # デフォルト処理（文字入力など）
            self.handle_default(key_info)
    
    def handle_default(self, key_info):
        """デフォルトのキー処理（サブクラスでオーバーライド）"""
        pass
    
    def get_action_handlers(self):
        """アクションハンドラーを取得（サブクラスでオーバーライド）"""
        return {}
