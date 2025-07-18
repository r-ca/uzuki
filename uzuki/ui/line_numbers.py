import curses
from typing import List, Tuple, Optional

class LineNumberDisplay:
    """行番号表示クラス"""
    
    def __init__(self):
        self.show_line_numbers = True
        self.line_number_width = 4
        self.current_line_highlight = True
        self.line_number_style = curses.A_DIM
        # カレント行ハイライトを薄いシアン色で
        self.current_line_style = curses.A_DIM | curses.color_pair(6) if curses.has_colors() else curses.A_DIM
        self.separator = "│"
        self.separator_style = curses.A_DIM
    
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
        """行数に応じて行番号の幅を計算"""
        if total_lines <= 0:
            return 3
        
        # 桁数を計算
        digits = len(str(total_lines))
        return max(3, digits + 1)  # 最低3文字 + 区切り文字用のスペース
    
    def format_line_number(self, line_num: int, width: int) -> str:
        """行番号をフォーマット"""
        if line_num <= 0:
            return "~".rjust(width)
        
        return str(line_num).rjust(width)
    
    def render_line_numbers(self, stdscr, lines: List[str], cursor_row: int, 
                           start_y: int, start_x: int, max_height: int, 
                           max_width: int) -> int:
        """行番号を描画し、使用した幅を返す"""
        if not self.show_line_numbers:
            return 0
        
        # 行番号の幅を計算
        total_lines = len(lines)
        line_num_width = self.calculate_line_number_width(total_lines)
        self.set_line_number_width(line_num_width)
        
        # 表示可能な行数を計算
        display_lines = min(len(lines), max_height)
        
        for i in range(display_lines):
            y = start_y + i
            line_num = i + 1
            
            # 行番号をフォーマット
            line_num_str = self.format_line_number(line_num, line_num_width)
            
            # 行番号を描画
            stdscr.addstr(y, start_x, line_num_str, self.line_number_style)
            
            # 区切り文字を描画
            separator_x = start_x + line_num_width
            if separator_x < start_x + max_width:
                stdscr.addstr(y, separator_x, self.separator, self.separator_style)
        
        # 使用した幅を返す（行番号 + 区切り文字 + スペース）
        return line_num_width + 2
    
    def highlight_current_line(self, stdscr, cursor_row: int, start_y: int, 
                              start_x: int, line_width: int, max_height: int):
        """カレント行をハイライト"""
        if not self.current_line_highlight:
            return
        
        # カーソル行が表示範囲内かチェック
        if 0 <= cursor_row < max_height:
            y = start_y + cursor_row
            
            # 行全体をハイライト（より控えめなスタイル）
            line_content = " " * line_width
            stdscr.addstr(y, start_x, line_content, self.current_line_style)

class LineHighlighter:
    """行ハイライト機能"""
    
    def __init__(self):
        self.highlighted_lines = set()  # ハイライトする行番号
        # より控えめなハイライトスタイル
        self.highlight_style = curses.A_DIM
        # エラー行は薄い赤色
        self.error_line_style = curses.A_DIM | curses.color_pair(1) if curses.has_colors() else curses.A_DIM
        # 警告行は薄い黄色
        self.warning_line_style = curses.A_DIM | curses.color_pair(3) if curses.has_colors() else curses.A_DIM
        # 情報行は薄い青色
        self.info_line_style = curses.A_DIM | curses.color_pair(4) if curses.has_colors() else curses.A_DIM
        # 成功行は薄い緑色
        self.success_line_style = curses.A_DIM | curses.color_pair(2) if curses.has_colors() else curses.A_DIM
    
    def add_highlight(self, line_num: int, style: Optional[int] = None):
        """行をハイライトに追加"""
        self.highlighted_lines.add((line_num, style or self.highlight_style))
    
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
        self.add_highlight(line_num, self.error_line_style)
    
    def highlight_warning_line(self, line_num: int):
        """警告行をハイライト"""
        self.add_highlight(line_num, self.warning_line_style)
    
    def highlight_info_line(self, line_num: int):
        """情報行をハイライト"""
        self.add_highlight(line_num, self.info_line_style)
    
    def highlight_success_line(self, line_num: int):
        """成功行をハイライト"""
        self.add_highlight(line_num, self.success_line_style)
    
    def set_highlight_style(self, style: int):
        """デフォルトのハイライトスタイルを設定"""
        self.highlight_style = style
    
    def set_error_style(self, style: int):
        """エラー行のスタイルを設定"""
        self.error_line_style = style
    
    def set_warning_style(self, style: int):
        """警告行のスタイルを設定"""
        self.warning_line_style = style

class LineDisplayManager:
    """行表示管理クラス"""
    
    def __init__(self):
        self.line_numbers = LineNumberDisplay()
        self.highlighter = LineHighlighter()
        self.show_ruler = False  # ルーラー（列番号）表示
        self.ruler_style = curses.A_DIM
    
    def render_editor_content(self, stdscr, lines: List[str], cursor_row: int, 
                             cursor_col: int, start_y: int, start_x: int, 
                             max_height: int, max_width: int) -> Tuple[int, int]:
        """エディタコンテンツを描画し、使用した幅と高さを返す"""
        # 行番号を描画
        line_num_width = self.line_numbers.render_line_numbers(
            stdscr, lines, cursor_row, start_y, start_x, max_height, max_width
        )
        
        # コンテンツエリアの開始位置
        content_start_x = start_x + line_num_width
        content_width = max_width - line_num_width
        
        # 行を描画
        display_lines = min(len(lines), max_height)
        
        for i in range(display_lines):
            y = start_y + i
            line = lines[i]
            
            # 行のスタイルを取得
            line_style = self.highlighter.get_line_style(i + 1) or curses.A_NORMAL
            
            # 行を描画（幅に収まるように切り詰め）
            display_line = line[:content_width]
            stdscr.addstr(y, content_start_x, display_line, line_style)
        
        # カレント行をハイライト
        self.line_numbers.highlight_current_line(
            stdscr, cursor_row, start_y, content_start_x, content_width, max_height
        )
        
        # ルーラーを描画（オプション）
        if self.show_ruler:
            self._render_ruler(stdscr, cursor_col, start_y, content_start_x, content_width, max_height)
        
        return line_num_width, display_lines
    
    def _render_ruler(self, stdscr, cursor_col: int, start_y: int, 
                     start_x: int, width: int, height: int):
        """ルーラー（列番号）を描画"""
        # 10文字ごとにマーカーを表示
        for col in range(0, width, 10):
            if col < width:
                marker = str(col + 1)
                if col + len(marker) <= width:
                    stdscr.addstr(start_y, start_x + col, marker, self.ruler_style)
    
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
            'highlighted_lines': len(self.highlighter.highlighted_lines),
        } 