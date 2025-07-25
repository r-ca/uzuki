"""
Editor Display

エディタの表示を一元管理するシンプルなクラス
"""

import curses
from typing import List, Tuple
from .color_manager import color_manager

class EditorDisplay:
    """エディタ表示管理クラス"""
    
    def __init__(self):
        self.show_line_numbers = True
        self.current_line_highlight = True
        self.line_num_width = 4
        self.scroll_y = 0
        self.scroll_x = 0
    
    def render(self, stdscr, lines: List[str], cursor_row: int, cursor_col: int, 
               start_y: int, start_x: int, height: int, width: int):
        """エディタを描画"""
        # スクロール位置を更新
        self._update_scroll(cursor_row, cursor_col, height, width)
        
        # 表示範囲を計算
        display_start = self.scroll_y
        display_end = min(display_start + height, len(lines))
        
        # 行番号の幅を計算
        if self.show_line_numbers:
            self.line_num_width = self._calculate_line_num_width(len(lines))
        
        # コンテンツ領域の開始位置
        content_x = start_x + (self.line_num_width if self.show_line_numbers else 0)
        content_width = width - (self.line_num_width if self.show_line_numbers else 0)
        
        # 各行を描画
        for i in range(display_end - display_start):
            y = start_y + i
            line_idx = display_start + i
            line = lines[line_idx] if line_idx < len(lines) else ""
            
            # 行番号を描画
            if self.show_line_numbers:
                self._draw_line_number(stdscr, y, start_x, line_idx + 1)
            
            # 行内容を描画
            self._draw_line_content(stdscr, y, content_x, line, content_width, 
                                  line_idx == cursor_row)
    
    def _update_scroll(self, cursor_row: int, cursor_col: int, height: int, width: int):
        """スクロール位置を更新"""
        # 縦スクロール
        if cursor_row < self.scroll_y:
            self.scroll_y = cursor_row
        elif cursor_row >= self.scroll_y + height:
            self.scroll_y = cursor_row - height + 1
        
        # 横スクロール
        content_width = width - (self.line_num_width if self.show_line_numbers else 0)
        if cursor_col < self.scroll_x:
            self.scroll_x = cursor_col
        elif cursor_col >= self.scroll_x + content_width:
            self.scroll_x = cursor_col - content_width + 1
    
    def _calculate_line_num_width(self, total_lines: int) -> int:
        """行番号の幅を計算"""
        if total_lines <= 0:
            return 4
        digits = len(str(total_lines))
        return max(4, digits + 2)
    
    def _draw_line_number(self, stdscr, y: int, x: int, line_num: int):
        """行番号を描画"""
        line_num_str = str(line_num).rjust(self.line_num_width - 2)
        style = color_manager.get_style(0, 'dim')
        
        try:
            stdscr.addstr(y, x, line_num_str, style)
            stdscr.addstr(y, x + self.line_num_width - 2, "│", style)
        except curses.error:
            pass
    
    def _draw_line_content(self, stdscr, y: int, x: int, line: str, width: int, is_current: bool):
        """行内容を描画"""
        # 横スクロールを適用
        display_line = line[self.scroll_x:self.scroll_x + width]
        
        # スタイルを決定
        style = curses.A_NORMAL
        if is_current and self.current_line_highlight:
            style |= color_manager.get_current_line_style()
        
        try:
            stdscr.addstr(y, x, display_line, style)
        except curses.error:
            safe_line = display_line[:width-1]
            if safe_line:
                try:
                    stdscr.addstr(y, x, safe_line, style)
                except curses.error:
                    pass
    
    def get_cursor_screen_pos(self, cursor_row: int, cursor_col: int, 
                             start_y: int, start_x: int) -> Tuple[int, int]:
        """カーソルの画面座標を取得"""
        screen_y = start_y + (cursor_row - self.scroll_y)
        screen_x = start_x + (self.line_num_width if self.show_line_numbers else 0) + (cursor_col - self.scroll_x)
        return screen_y, screen_x 