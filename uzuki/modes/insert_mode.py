"""
Insert Mode - 挿入モード
"""

from uzuki.modes.base_mode import BaseMode
from uzuki.input.keycodes import Key

class InsertMode(BaseMode):
    """Insert mode - テキスト挿入モード"""
    
    def __init__(self, screen):
        super().__init__(screen, 'insert')
    
    def get_action_handlers(self):
        """Insert modeのアクションハンドラー"""
        return {
            'enter_normal_mode': lambda: self.screen.set_mode('normal'),
            'new_line': self._new_line,
            'delete_backward': self._delete_backward,
            'indent': self._indent,
        }
    
    def handle_default(self, key_info):
        """デフォルト処理 - 文字を挿入"""
        if key_info.is_printable and key_info.char:
            buf = self.screen.editor.buffer
            buf.insert(self.screen.editor.cursor.row, self.screen.editor.cursor.col, key_info.char)
            self.screen.editor.cursor.move(0, 1, buf)
            self.screen.editor.needs_redraw = True
    
    def _new_line(self):
        """新しい行を作成"""
        self.screen.editor.buffer.split_line(self.screen.editor.cursor.row, self.screen.editor.cursor.col)
        # 新しい行の先頭に移動
        self.screen.editor.cursor.row += 1
        self.screen.editor.cursor.col = 0
        self.screen.editor.needs_redraw = True
    
    def _delete_backward(self):
        """後方削除"""
        if self.screen.editor.cursor.col > 0:
            self.screen.editor.buffer.delete(self.screen.editor.cursor.row, self.screen.editor.cursor.col - 1)
            self.screen.editor.cursor.move(0, -1, self.screen.editor.buffer)
            self.screen.editor.needs_redraw = True
    
    def _indent(self):
        """インデント"""
        self.screen.editor.buffer.insert(self.screen.editor.cursor.row, 0, '    ')
        self.screen.editor.cursor.move(0, 4, self.screen.editor.buffer)
        self.screen.editor.needs_redraw = True
