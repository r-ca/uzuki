"""
UI Controller

Manages UI rendering including screen drawing, status line, notifications,
line display, and greeting screen.
"""

import curses
from typing import List, Optional
from uzuki.ui.status_line import StatusLineManager, StatusLineBuilder
from uzuki.ui.notification import NotificationLevel, NotificationManager
from uzuki.ui.line_numbers import LineDisplayManager
from uzuki.ui.color_manager import color_manager
from uzuki.ui.cursor_display import cursor_display
from uzuki.utils.screen_utils import GreetingRenderer
from uzuki.utils.debug import get_debug_logger
from .editor_display import EditorDisplay

class UIController:
    """UI描画を制御するコントローラー"""
    
    def __init__(self, screen):
        self.screen = screen
        self.logger = get_debug_logger()
        
        # 表示管理
        self.editor_display = EditorDisplay()
        
        # ステータスライン
        self.status_line = StatusLineManager()
        self.status_builder = StatusLineBuilder(self.status_line)
        
        # 通知
        self.notifications = NotificationManager()
        
        # Greeting
        self.greeting = GreetingRenderer()
        self.greeting_content = []
        self.greeting_bottom_text = ""
        self.show_greeting = True
        
        # Greetingの内容を設定
        self.greeting.set_content(self.greeting_content)
        self.greeting.set_bottom_text(self.greeting_bottom_text)
        
        self.logger.debug("UIController initialized")
    
    def draw(self, stdscr):
        """画面を描画"""
        try:
            # 画面サイズを取得
            height, width = stdscr.getmaxyx()
            
            # 画面をクリア
            stdscr.clear()
            
            # Greeting表示中でない場合はエディタコンテンツを描画
            if not self.show_greeting:
                self._draw_editor_content(stdscr, width, height)
            
            # ステータスラインを描画
            self._draw_status_line(stdscr, width, height)
            
            # 画面を更新
            stdscr.refresh()
            
        except Exception as e:
            self.logger.log_error(e, "UIController.draw")
    
    def _draw_editor_content(self, stdscr, width: int, height: int):
        """エディタコンテンツの描画"""
        try:
            # ファイルブラウザモードの場合は専用描画
            if self.screen.editor.mode.mode_name == 'file_browser':
                self._draw_file_browser(stdscr, width, height)
                return
            
            # 通常のエディタコンテンツ描画（コマンドモードも含む）
            # コマンドモードの場合は、バッファの内容を表示し、ステータスラインでコマンドを表示
            content_height = height - 1  # ステータスライン分を除く
            
            # バッファの内容を取得
            lines = self.screen.editor.buffer.lines
            if not lines or (len(lines) == 1 and lines[0] == ""):
                # バッファが空の場合は空行を追加
                self.screen.editor.buffer.lines = [""]
                lines = self.screen.editor.buffer.lines
            
            # エディタを描画（コマンドモードでもバッファの内容を表示）
            cursor_row = self.screen.editor.cursor.row
            cursor_col = self.screen.editor.cursor.col
            self.editor_display.render(stdscr, lines, cursor_row, cursor_col, 
                                     0, 0, content_height, width)
            
        except Exception as e:
            self.logger.log_error(e, "UIController._draw_editor_content")
    
    def _draw_file_browser(self, stdscr, width: int, height: int):
        """ファイルブラウザモードの描画"""
        try:
            # ファイルブラウザの内容を取得
            browser_content = self.screen.file.get_file_browser_content()
            selection = self.screen.file.get_file_browser_selection()
            
            # 利用可能な高さを計算（ステータスライン分を除く）
            available_height = height - 2
            
            # ファイルリストを描画
            for i, item in enumerate(browser_content[:available_height]):
                try:
                    # 選択されたアイテムは反転表示
                    if i == selection:
                        style = color_manager.get_reverse_style()
                    else:
                        style = curses.A_NORMAL
                    
                    # アイテムを描画
                    display_item = item[:width-1]  # 画面幅に収める
                    stdscr.addstr(i, 0, display_item, style)
                    
                except curses.error:
                    pass
                    
        except Exception as e:
            self.logger.log_error(e, "UIController._draw_file_browser")
    
    def _draw_status_line(self, stdscr, width: int, height: int):
        """ステータスラインを描画"""
        try:
            # ステータスラインを構築
            self._build_status_line()
            
            # ステータスラインを描画
            self.status_line.render(stdscr)
            
        except Exception as e:
            self.logger.log_error(e, "UIController._draw_status_line")
    
    def _build_status_line(self):
        """ステータスラインを構築"""
        try:
            self.status_line.clear()
            # 現在のモードを取得
            mode_name = self.screen.editor.mode.mode_name
            
            # モード名を表示
            self.status_builder.mode(mode_name.upper())
            
            # ファイル情報を表示
            file_info = self.screen.file.get_file_info()
            if file_info.get('filename'):
                self.status_builder.filename(file_info['filename'])
                if file_info.get('encoding'):
                    self.status_builder.encoding(file_info['encoding'])
                if file_info.get('modified'):
                    self.status_builder.add_segment('modified', '[+]', width=3, align='left', priority=10)
            
            # カーソル位置を表示
            cursor_row = self.screen.editor.cursor.row
            cursor_col = self.screen.editor.cursor.col
            total_lines = len(self.screen.editor.buffer.lines)
            self.status_builder.position(cursor_row, cursor_col)
            self.status_builder.line_count(total_lines)
            
            # コマンドモードの場合はコマンドバッファを表示
            if mode_name == 'command':
                cmd_text = self.screen.editor.mode.cmd_buf
                self.status_builder.command(cmd_text)
            
        except Exception as e:
            self.logger.log_error(e, "UIController._build_status_line")
    
    def display_greeting(self, stdscr) -> bool:
        """Greetingを表示"""
        try:
            # Greetingを描画
            self.greeting.render_greeting(stdscr)
            return True
        except Exception as e:
            self.logger.log_error(e, "UIController.display_greeting")
            return False
    
    def set_greeting_content(self, lines: List[str]):
        """Greetingの内容を設定"""
        self.greeting_content = lines
        self.logger.debug("Greeting content updated")
    
    def add_greeting_content_line(self, line: str):
        """Greetingに行を追加"""
        self.greeting_content.append(line)
        self.logger.debug("Greeting content line added")
    
    def clear_greeting_content(self):
        """Greetingの内容をクリア"""
        self.greeting_content = []
        self.logger.debug("Greeting content cleared")
    
    def set_greeting_bottom_text(self, text: str):
        """Greetingの下部テキストを設定"""
        self.greeting_bottom_text = text
        self.logger.debug("Greeting bottom text updated")
    
    def set_show_greeting(self, show: bool):
        """Greeting表示を設定"""
        self.show_greeting = show
        self.logger.debug(f"Show greeting set to: {show}")
    
    def toggle_line_numbers(self):
        """行番号表示を切り替え"""
        self.editor_display.show_line_numbers = not self.editor_display.show_line_numbers
    
    def toggle_current_line_highlight(self):
        """カレント行ハイライトを切り替え"""
        self.editor_display.current_line_highlight = not self.editor_display.current_line_highlight
    
    def toggle_ruler(self):
        """ルーラー表示を切り替え"""
        # ルーラー機能は現在未実装
        pass
    
    def set_horizontal_offset(self, offset: int):
        """横スクロールオフセットを設定"""
        self.editor_display.scroll_x = max(0, offset)
    
    def get_horizontal_offset(self) -> int:
        """横スクロールオフセットを取得"""
        return self.editor_display.scroll_x
    
    def set_vertical_offset(self, offset: int):
        """縦スクロールオフセットを設定"""
        self.editor_display.scroll_y = max(0, offset)
    
    def get_vertical_offset(self) -> int:
        """縦スクロールオフセットを取得"""
        return self.editor_display.scroll_y
    
    def get_display_info(self) -> dict:
        """表示情報を取得"""
        return {
            'line_numbers': self.editor_display.show_line_numbers,
            'current_line_highlight': self.editor_display.current_line_highlight,
            'horizontal_offset': self.editor_display.scroll_x,
            'vertical_offset': self.editor_display.scroll_y
        } 