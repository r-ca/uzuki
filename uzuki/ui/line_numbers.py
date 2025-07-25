"""
Line Numbers and Highlighting

行番号表示とハイライト機能を提供
"""

import curses
from typing import List, Optional, Tuple
from .color_manager import color_manager
from .viewport_manager import ViewportManager, ViewportInfo

class LineNumberDisplay:
    """行番号表示クラス"""
    
    def __init__(self):
        self.show_line_numbers = True
        self.current_line_highlight = True
        self.line_number_width = 4
    
    def set_line_number_width(self, width: int):
        """行番号の幅を設定"""
        self.line_number_width = max(3, width)
    
    def toggle_line_numbers(self):
        """行番号表示を切り替え"""
        self.show_line_numbers = not self.show_line_numbers
    
    def toggle_current_line_highlight(self):
        """カレント行ハイライトを切り替え"""
        self.current_line_highlight = not self.current_line_highlight
    
    def calculate_line_number_width(self, total_lines: int) -> int:
        """行番号の幅を計算"""
        if total_lines <= 0:
            return 4  # 最小幅（行番号 + 縦棒 + スペース）
        # 行番号の桁数を計算
        digits = len(str(total_lines))
        return max(4, digits + 2)  # 最小4文字（行番号 + 縦棒 + スペース）
    
    def format_line_number(self, line_num: int, width: int) -> str:
        """行番号をフォーマット"""
        return str(line_num).rjust(width - 2)  # 縦棒とスペース分を除く
    
    def render_line_numbers(self, stdscr, lines: List[str], cursor_row: int, 
                           start_y: int, start_x: int, max_height: int, 
                           max_width: int, scroll_offset: int = 0) -> int:
        """行番号を描画し、使用した幅を返す"""
        if not self.show_line_numbers:
            return 0
        
        # 行番号の幅を計算（バッファ全体の行数で計算）
        total_lines = len(lines)
        line_num_width = self.calculate_line_number_width(total_lines)
        self.set_line_number_width(line_num_width)
        
        # 表示可能な行数を計算
        display_lines = min(len(lines), max_height)
        
        # 行番号用のスタイル（暗い色）
        line_num_style = color_manager.get_style(0, 'dim')
        
        for i in range(display_lines):
            y = start_y + i
            # バッファ全体での行番号を計算（スクロールオフセットを考慮）
            line_num = scroll_offset + i + 1
            
            # 行番号をフォーマット
            line_num_str = self.format_line_number(line_num, line_num_width)
            
            # 行番号を描画（幅チェック）
            if start_x + len(line_num_str) <= max_width:
                try:
                    stdscr.addstr(y, start_x, line_num_str, line_num_style)
                except curses.error:
                    pass
            
            # 縦棒を描画（行番号の右隣）
            separator_x = start_x + line_num_width - 2  # 行番号幅から縦棒とスペース分を引く
            if separator_x < start_x + max_width:
                try:
                    stdscr.addstr(y, separator_x, "│", line_num_style)
                except curses.error:
                    pass
        
        # 使用した幅を返す（行番号 + 区切り文字 + スペース）
        return line_num_width + 2
    


class LineHighlighter:
    """行ハイライト機能"""
    
    def __init__(self):
        self.highlighted_lines = set()  # ハイライトする行番号
    
    def add_highlight(self, line_num: int, style: Optional[int] = None):
        """行をハイライトに追加"""
        if style is None:
            style = color_manager.get_highlight_style()
        self.highlighted_lines.add((line_num, style))
    
    def remove_highlight(self, line_num: int):
        """行のハイライトを削除"""
        self.highlighted_lines = {(ln, style) for ln, style in self.highlighted_lines if ln != line_num}
    
    def clear_highlights(self):
        """すべてのハイライトをクリア"""
        self.highlighted_lines.clear()
    
    def get_line_style(self, line_num: int) -> Optional[int]:
        """行のスタイルを取得"""
        for ln, style in self.highlighted_lines:
            if ln == line_num:
                return style
        return None
    
    def highlight_error_line(self, line_num: int):
        """エラー行をハイライト"""
        self.add_highlight(line_num, color_manager.get_error_style())
    
    def highlight_warning_line(self, line_num: int):
        """警告行をハイライト"""
        self.add_highlight(line_num, color_manager.get_warning_style())
    
    def highlight_info_line(self, line_num: int):
        """情報行をハイライト"""
        self.add_highlight(line_num, color_manager.get_info_style())
    
    def highlight_success_line(self, line_num: int):
        """成功行をハイライト"""
        self.add_highlight(line_num, color_manager.get_success_style())
    
    def set_highlight_style(self, style: int):
        """デフォルトのハイライトスタイルを設定"""
        # このメソッドは後方互換性のため残す
        pass
    
    def set_error_style(self, style: int):
        """エラー行のスタイルを設定"""
        # このメソッドは後方互換性のため残す
        pass
    
    def set_warning_style(self, style: int):
        """警告行のスタイルを設定"""
        # このメソッドは後方互換性のため残す
        pass

class LineDisplayManager:
    """行表示管理クラス"""
    
    def __init__(self):
        self.line_numbers = LineNumberDisplay()
        self.highlighter = LineHighlighter()
        self.show_ruler = False
        self.viewport = ViewportManager()
    
    def render_editor_content(self, stdscr, lines: List[str], cursor_row: int, 
                             cursor_col: int, start_y: int, start_x: int, 
                             max_height: int, max_width: int) -> Tuple[int, int]:
        """エディタコンテンツを描画し、使用した幅と高さを返す"""
        # ビューポート情報を取得
        viewport = self.viewport.get_viewport_info(start_y, start_x, max_height, max_width)
        
        # 行番号の幅を計算して設定
        total_lines = len(lines)
        line_num_width = self.line_numbers.calculate_line_number_width(total_lines)
        self.viewport.set_line_number_width(line_num_width)
        
        # ビューポート情報を更新
        viewport = self.viewport.get_viewport_info(start_y, start_x, max_height, max_width)
        
        # カーソル追従スクロール
        self.viewport.scroll_to_cursor(cursor_row, cursor_col, viewport)
        
        # 表示される行の範囲を取得
        start_line, end_line = self.viewport.get_visible_range(len(lines), viewport)
        
        # 行番号を描画
        line_num_width = self.line_numbers.render_line_numbers(
            stdscr, lines[start_line:end_line], cursor_row - start_line, 
            viewport.start_y, viewport.start_x, viewport.height, viewport.width,
            start_line  # スクロールオフセットを渡す
        )
        
        # 行を描画
        display_lines = min(end_line - start_line, viewport.height)
        
        for i in range(display_lines):
            y = viewport.start_y + i
            line = lines[start_line + i]
            line_num = start_line + i + 1
            
            # 行のスタイルを取得（ハイライト優先）
            line_style = self.highlighter.get_line_style(line_num) or curses.A_NORMAL
            
            # カレント行の場合は背景色を追加
            if line_num == cursor_row + 1 and self.line_numbers.current_line_highlight:
                current_line_style = color_manager.get_current_line_style()
                line_style |= current_line_style
            
            # 表示用文字列を取得
            display_line = self.viewport.get_display_line(line, viewport)
            
            # 行を描画
            try:
                stdscr.addstr(y, viewport.content_start_x, display_line, line_style)
            except curses.error:
                safe_line = display_line[:viewport.content_width-1]
                if safe_line:
                    try:
                        stdscr.addstr(y, viewport.content_start_x, safe_line, line_style)
                    except curses.error:
                        pass
        
        # ルーラーを描画（オプション）
        if self.show_ruler:
            self._render_ruler(stdscr, cursor_col, viewport)
        
        return line_num_width, display_lines
    
    def _render_ruler(self, stdscr, cursor_col: int, viewport: ViewportInfo):
        """ルーラー（列番号）を描画"""
        if viewport.height < 2:
            return
        
        # ルーラー行
        ruler_y = viewport.start_y + viewport.height - 1
        ruler_text = ""
        
        # 横スクロールオフセットを考慮
        for i in range(viewport.horizontal_offset, viewport.horizontal_offset + viewport.width, 10):
            ruler_text += str(i).ljust(10)
        
        # ルーラー用のスタイル
        ruler_style = color_manager.get_style(0, 'dim')
        
        # 安全な描画
        safe_ruler = ruler_text[:viewport.width]
        try:
            stdscr.addstr(ruler_y, viewport.start_x, safe_ruler, ruler_style)
        except curses.error:
            pass
    
    def toggle_line_numbers(self):
        """行番号表示を切り替え"""
        self.line_numbers.toggle_line_numbers()
    
    def toggle_current_line_highlight(self):
        """カレント行ハイライトを切り替え"""
        self.line_numbers.toggle_current_line_highlight()
    
    def toggle_ruler(self):
        """ルーラー表示を切り替え"""
        self.show_ruler = not self.show_ruler
    
    def get_display_info(self) -> dict:
        """表示情報を取得"""
        return {
            'line_numbers': self.line_numbers.show_line_numbers,
            'current_line_highlight': self.line_numbers.current_line_highlight,
            'ruler': self.show_ruler,
            'horizontal_offset': self.viewport.horizontal_offset,
            'vertical_offset': self.viewport.vertical_offset
        } 

    def set_horizontal_offset(self, offset: int):
        """横スクロールオフセットを設定"""
        self.viewport.horizontal_offset = max(0, offset)
    
    def get_horizontal_offset(self) -> int:
        """横スクロールオフセットを取得"""
        return self.viewport.horizontal_offset
    
    def set_vertical_offset(self, offset: int):
        """縦スクロールオフセットを設定"""
        self.viewport.vertical_offset = max(0, offset)
    
    def get_vertical_offset(self) -> int:
        """縦スクロールオフセットを取得"""
        return self.viewport.vertical_offset 