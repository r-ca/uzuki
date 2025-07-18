import curses
from typing import List, Tuple, Optional

class LineNumberDisplay:
    """行番号表示クラス"""
    
    def __init__(self):
        self.show_line_numbers = True
        self.line_number_width = 4
        self.current_line_highlight = True
        self.line_number_style = curses.A_DIM
        # カレント行ハイライトをより控えめに
        self.current_line_style = curses.A_DIM
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
            
            # 行番号を描画（幅チェック）
            if start_x + len(line_num_str) <= max_width:
                stdscr.addstr(y, start_x, line_num_str, self.line_number_style)
            
            # 区切り文字を描画（幅チェック）
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
            safe_width = min(line_width, max_height)  # 安全な幅を計算
            line_content = " " * safe_width
            stdscr.addstr(y, start_x, line_content, self.current_line_style)

class LineHighlighter:
    """行ハイライト機能"""
    
    def __init__(self):
        self.highlighted_lines = set()  # ハイライトする行番号
        # より控えめなハイライトスタイル
        self.highlight_style = curses.A_DIM
        # 色スタイルは初期化時に設定（curses初期化後）
        self.error_line_style = None
        self.warning_line_style = None
        self.info_line_style = None
        self.success_line_style = None
        self._colors_initialized = False
    
    def _init_colors(self):
        """色を初期化（curses初期化後に呼び出し）"""
        if self._colors_initialized:
            return
        
        try:
            if curses.has_colors():
                # エラー行は薄い赤色
                self.error_line_style = curses.A_DIM | curses.color_pair(1)
                # 警告行は薄い黄色
                self.warning_line_style = curses.A_DIM | curses.color_pair(3)
                # 情報行は薄い青色
                self.info_line_style = curses.A_DIM | curses.color_pair(4)
                # 成功行は薄い緑色
                self.success_line_style = curses.A_DIM | curses.color_pair(2)
            else:
                # 色が使えない場合はすべてA_DIM
                self.error_line_style = curses.A_DIM
                self.warning_line_style = curses.A_DIM
                self.info_line_style = curses.A_DIM
                self.success_line_style = curses.A_DIM
        except:
            # エラーが発生した場合はすべてA_DIM
            self.error_line_style = curses.A_DIM
            self.warning_line_style = curses.A_DIM
            self.info_line_style = curses.A_DIM
            self.success_line_style = curses.A_DIM
        
        self._colors_initialized = True
    
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
        self._init_colors()
        self.add_highlight(line_num, self.error_line_style)
    
    def highlight_warning_line(self, line_num: int):
        """警告行をハイライト"""
        self._init_colors()
        self.add_highlight(line_num, self.warning_line_style)
    
    def highlight_info_line(self, line_num: int):
        """情報行をハイライト"""
        self._init_colors()
        self.add_highlight(line_num, self.info_line_style)
    
    def highlight_success_line(self, line_num: int):
        """成功行をハイライト"""
        self._init_colors()
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
            
            # 行を描画（幅に収まるように切り詰め、安全な描画）
            display_line = line[:content_width]
            try:
                stdscr.addstr(y, content_start_x, display_line, line_style)
            except curses.error:
                # 画面端でのエラーを防ぐ
                safe_line = display_line[:content_width-1]
                if safe_line:
                    stdscr.addstr(y, content_start_x, safe_line, line_style)
        
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
        if height < 2:
            return
        
        # ルーラー行
        ruler_y = start_y + height - 1
        ruler_text = ""
        
        for i in range(0, width, 10):
            ruler_text += str(i).ljust(10)
        
        # 安全な描画
        safe_ruler = ruler_text[:width]
        try:
            stdscr.addstr(ruler_y, start_x, safe_ruler, self.ruler_style)
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
            'ruler': self.show_ruler
        } 