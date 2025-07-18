import time

class KeySequenceManager:
    """キーシーケンス管理クラス"""
    def __init__(self, timeout=1000):
        self.timeout = timeout  # ミリ秒
        self.sequence = ""
        self.last_key_time = 0
    
    def add_key(self, key: str) -> str:
        """キーを追加し、完了したシーケンスを返す"""
        current_time = int(time.time() * 1000)
        
        # タイムアウトチェック
        if current_time - self.last_key_time > self.timeout:
            self.sequence = ""
        
        self.sequence += key
        self.last_key_time = current_time
        
        return self.sequence
    
    def clear(self):
        """シーケンスをクリア"""
        self.sequence = ""
    
    def get_sequence(self) -> str:
        """現在のシーケンスを取得"""
        return self.sequence 