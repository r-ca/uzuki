"""
カーソル表示管理

各モードでカーソル形状を定義・管理する（cursesのシステムカーソルを使用）
"""

import curses
from typing import Dict

class CursorDisplay:
    """カーソル表示管理クラス（cursesシステムカーソル使用）"""
    
    def __init__(self):
        # 各モードのカーソル形状を定義
        # 0: 非表示, 1: 通常, 2: ブロック, 3: 下線
        self.mode_cursors: Dict[str, int] = {
            'normal': 1,      # 通常カーソル
            'insert': 1,      # 通常カーソル
            'command': 1,     # 通常カーソル
            'file_browser': 1, # 通常カーソル
        }
        self.current_mode = 'normal'
    
    def set_mode(self, mode: str):
        """モードを設定し、対応するカーソル形状に変更"""
        self.current_mode = mode
        cursor_type = self.mode_cursors.get(mode, 2)  # デフォルトはブロック
        try:
            curses.curs_set(cursor_type)
        except:
            pass
    
    def set_cursor_for_mode(self, mode: str, cursor_type: int):
        """特定のモードのカーソル形状を設定"""
        self.mode_cursors[mode] = cursor_type
        if mode == self.current_mode:
            try:
                curses.curs_set(cursor_type)
            except:
                pass

# グローバルインスタンス
cursor_display = CursorDisplay() 