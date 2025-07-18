from uzuki.modes.base_mode import BaseMode

class NormalMode(BaseMode):
    """Normal mode - メインのナビゲーションモード"""
    def __init__(self, screen):
        super().__init__(screen, 'normal')
    
    def get_action_handlers(self):
        """Normal modeのアクションハンドラー"""
        return {
            # ナビゲーション
            'move_left': lambda: self.screen.cursor.move(0, -1, self.screen.buffer),
            'move_down': lambda: self.screen.cursor.move(1, 0, self.screen.buffer),
            'move_up': lambda: self.screen.cursor.move(-1, 0, self.screen.buffer),
            'move_right': lambda: self.screen.cursor.move(0, 1, self.screen.buffer),
            
            # モード切り替え
            'enter_insert_mode': lambda: self.screen.set_mode('insert'),
            'enter_command_mode': lambda: self.screen.set_mode('command'),
            'open_file_browser': self._open_file_browser,
            
            # 編集操作
            'delete_char': lambda: self.screen.buffer.delete(self.screen.cursor.row, self.screen.cursor.col),
            'new_line_below': self._new_line_below,
            'new_line_above': self._new_line_above,
            'append': self._append,
            'append_end': self._append_end,
            'delete_line': self._delete_line,
            'yank_line': self._yank_line,
            'paste': self._paste,
            'paste_before': self._paste_before,
            
            # その他
            'noop': lambda: None,
        }
    
    def _open_file_browser(self):
        """ファイルブラウザーを開く"""
        self.screen.open_file_browser()
    
    def _new_line_below(self):
        """現在行の下に新しい行を挿入"""
        self.screen.buffer.split_line(self.screen.cursor.row, self.screen.cursor.col)
        self.screen.cursor.move(1, -self.screen.cursor.col, self.screen.buffer)
        self.screen.set_mode('insert')
    
    def _new_line_above(self):
        """現在行の上に新しい行を挿入"""
        if self.screen.cursor.row > 0:
            self.screen.cursor.move(-1, 0, self.screen.buffer)
        self.screen.buffer.split_line(self.screen.cursor.row, 0)
        self.screen.set_mode('insert')
    
    def _append(self):
        """現在位置の後に挿入モードに入る"""
        self.screen.cursor.move(0, 1, self.screen.buffer)
        self.screen.set_mode('insert')
    
    def _append_end(self):
        """行末に挿入モードに入る"""
        line = self.screen.buffer.lines[self.screen.cursor.row]
        self.screen.cursor.col = len(line)
        self.screen.set_mode('insert')
    
    def _delete_line(self):
        """現在行を削除"""
        if len(self.screen.buffer.lines) > 1:
            del self.screen.buffer.lines[self.screen.cursor.row]
            if self.screen.cursor.row >= len(self.screen.buffer.lines):
                self.screen.cursor.row = len(self.screen.buffer.lines) - 1
            self.screen.cursor.col = min(self.screen.cursor.col, len(self.screen.buffer.lines[self.screen.cursor.row]))
    
    def _yank_line(self):
        """現在行をヤンク（コピー）"""
        # TODO: クリップボード機能の実装
        pass
    
    def _paste(self):
        """現在位置の後にペースト"""
        # TODO: クリップボード機能の実装
        pass
    
    def _paste_before(self):
        """現在位置の前にペースト"""
        # TODO: クリップボード機能の実装
        pass
