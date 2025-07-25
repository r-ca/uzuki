"""
Normal Mode - 通常モード
"""

from uzuki.modes.base_mode import BaseMode

class NormalMode(BaseMode):
    """Normal mode - 通常モード"""
    
    def __init__(self, screen):
        super().__init__(screen, 'normal')
    
    def get_action_handlers(self):
        """Normal modeのアクションハンドラー"""
        return {
            # ナビゲーション
            'move_left': lambda: self.screen.editor.cursor.move(0, -1, self.screen.editor.buffer),
            'move_down': lambda: self.screen.editor.cursor.move(1, 0, self.screen.editor.buffer),
            'move_up': lambda: self.screen.editor.cursor.move(-1, 0, self.screen.editor.buffer),
            'move_right': lambda: self.screen.editor.cursor.move(0, 1, self.screen.editor.buffer),
            'move_beginning_of_line': lambda: self.screen.editor.cursor.move(0, -self.screen.editor.cursor.col, self.screen.editor.buffer),
            'move_end_of_line': lambda: self._move_end_of_line(),
            'move_first_non_blank': lambda: self._move_first_non_blank(),
            'move_beginning_of_file': lambda: self.screen.editor.cursor.move(-self.screen.editor.cursor.row, 0, self.screen.editor.buffer),
            'move_end_of_file': lambda: self._move_end_of_file(),
            
            # モード切り替え
            'enter_insert_mode': lambda: self.screen.set_mode('insert'),
            'append_after_cursor': lambda: self._append_after_cursor(),
            'append_end_of_line': lambda: self._append_end_of_line(),
            'enter_command_mode': lambda: self.screen.set_mode('command'),
            
            # 編集操作
            'delete_char': lambda: self.screen.editor.buffer.delete(self.screen.editor.cursor.row, self.screen.editor.cursor.col),
            'delete_line': self._delete_line,
            
            # 表示切り替え
            'toggle_line_numbers': self._toggle_line_numbers,
            'toggle_current_line_highlight': self._toggle_current_line_highlight,
            'toggle_ruler': self._toggle_ruler,
            
            # ファイル操作
            'save_file': lambda: self.screen.save_file(),
            'quit': lambda: self.screen.quit(),
            'open_file_browser': lambda: self.screen.open_file_browser(),
        }
    
    def handle_default(self, key_info):
        """デフォルト処理"""
        pass
    
    def _move_end_of_line(self):
        """行の末尾に移動"""
        line = self.screen.editor.buffer.lines[self.screen.editor.cursor.row]
        target_col = len(line)
        self.screen.editor.cursor.move(0, target_col - self.screen.editor.cursor.col, self.screen.editor.buffer)
    
    def _move_first_non_blank(self):
        """行の最初の非空白文字に移動"""
        line = self.screen.editor.buffer.lines[self.screen.editor.cursor.row]
        for i, char in enumerate(line):
            if char != ' ' and char != '\t':
                self.screen.editor.cursor.move(0, i - self.screen.editor.cursor.col, self.screen.editor.buffer)
                return
        # 空白文字のみの場合は行頭に移動
        self.screen.editor.cursor.move(0, -self.screen.editor.cursor.col, self.screen.editor.buffer)
    
    def _move_end_of_file(self):
        """ファイルの末尾に移動"""
        target_row = len(self.screen.editor.buffer.lines) - 1
        self.screen.editor.cursor.move(target_row - self.screen.editor.cursor.row, 0, self.screen.editor.buffer)
    
    def _append_after_cursor(self):
        """カーソルの後に挿入"""
        self.screen.editor.cursor.move(0, 1, self.screen.editor.buffer)
        self.screen.set_mode('insert')
    
    def _append_end_of_line(self):
        """行の末尾に挿入"""
        line = self.screen.editor.buffer.lines[self.screen.editor.cursor.row]
        self.screen.editor.cursor.move(0, len(line) - self.screen.editor.cursor.col, self.screen.editor.buffer)
        self.screen.set_mode('insert')
    
    def _new_line_below(self):
        """下に新しい行を作成"""
        self.screen.editor.buffer.split_line(self.screen.editor.cursor.row, self.screen.editor.cursor.col)
        self.screen.editor.cursor.move(1, -self.screen.editor.cursor.col, self.screen.editor.buffer)
        self.screen.set_mode('insert')
    
    def _new_line_above(self):
        """上に新しい行を作成"""
        self.screen.editor.cursor.move(-1, 0, self.screen.editor.buffer)
        self.screen.editor.buffer.split_line(self.screen.editor.cursor.row, 0)
        self.screen.set_mode('insert')
    
    def _delete_line(self):
        """現在の行を削除"""
        line = self.screen.editor.buffer.lines[self.screen.editor.cursor.row]
        if len(self.screen.editor.buffer.lines) > 1:
            del self.screen.editor.buffer.lines[self.screen.editor.cursor.row]
            if self.screen.editor.cursor.row >= len(self.screen.editor.buffer.lines):
                self.screen.editor.cursor.row = len(self.screen.editor.buffer.lines) - 1
            self.screen.editor.cursor.col = min(self.screen.editor.cursor.col, len(self.screen.editor.buffer.lines[self.screen.editor.cursor.row]))
            self.screen.editor.needs_redraw = True
    

    
    def _toggle_line_numbers(self):
        """行番号表示を切り替え"""
        self.screen.toggle_line_numbers()
    
    def _toggle_current_line_highlight(self):
        """カレント行ハイライトを切り替え"""
        self.screen.toggle_current_line_highlight()
    
    def _toggle_ruler(self):
        """ルーラー表示を切り替え"""
        self.screen.toggle_ruler()
