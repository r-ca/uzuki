from uzuki.modes.base_mode import BaseMode

class InsertMode(BaseMode):
    """Insert mode - テキスト入力モード"""
    def __init__(self, screen):
        super().__init__(screen, 'insert')
    
    def get_action_handlers(self):
        """Insert modeのアクションハンドラー"""
        return {
            # モード切り替え
            'enter_normal_mode': lambda: self.screen.set_mode('normal'),
            
            # 編集操作
            'new_line': self._new_line,
            'delete_backward': self._delete_backward,
            'indent': self._indent,
            'unindent': self._unindent,
        }
    
    def handle_default(self, key_info):
        """デフォルト処理：文字入力"""
        if key_info.is_printable and key_info.char:
            buf = self.screen.buffer
            cur = self.screen.cursor
            buf.insert(cur.row, cur.col, key_info.char)
            cur.move(0, 1, buf)
            # 画面更新フラグを設定
            self.screen.needs_redraw = True
    
    def _new_line(self):
        """新しい行を挿入"""
        self.screen.buffer.split_line(self.screen.cursor.row, self.screen.cursor.col)
        self.screen.cursor.move(1, -self.screen.cursor.col, self.screen.buffer)
        # 画面更新フラグを設定
        self.screen.needs_redraw = True
    
    def _delete_backward(self):
        """後方削除"""
        if self.screen.cursor.col > 0:
            self.screen.buffer.delete(self.screen.cursor.row, self.screen.cursor.col - 1)
            self.screen.cursor.move(0, -1, self.screen.buffer)
            # 画面更新フラグを設定
            self.screen.needs_redraw = True
    
    def _indent(self):
        """インデント"""
        self.screen.buffer.insert(self.screen.cursor.row, 0, '    ')
        self.screen.cursor.move(0, 4, self.screen.buffer)
        # 画面更新フラグを設定
        self.screen.needs_redraw = True
    
    def _unindent(self):
        """アンインデント"""
        # TODO: インデント削除の実装
        pass
