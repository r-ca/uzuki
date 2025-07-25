"""
Viewport Manager

画面表示領域の管理と座標変換を一元化する
"""

from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class ViewportInfo:
    """ビューポート情報"""
    start_y: int
    start_x: int
    height: int
    width: int
    line_num_width: int
    content_start_x: int
    content_width: int

class ViewportManager:
    """ビューポート管理クラス"""
    
    def __init__(self):
        self.vertical_offset = 0
        self.horizontal_offset = 0
        self.line_num_width = 0
    
    def set_line_number_width(self, width: int):
        """行番号の幅を設定"""
        self.line_num_width = width
    
    def get_viewport_info(self, start_y: int, start_x: int, height: int, width: int) -> ViewportInfo:
        """ビューポート情報を取得"""
        content_start_x = start_x + self.line_num_width
        content_width = width - self.line_num_width
        
        return ViewportInfo(
            start_y=start_y,
            start_x=start_x,
            height=height,
            width=width,
            line_num_width=self.line_num_width,
            content_start_x=content_start_x,
            content_width=content_width
        )
    
    def scroll_to_cursor(self, cursor_row: int, cursor_col: int, viewport: ViewportInfo):
        """カーソル位置に合わせてスクロール"""
        # 縦スクロール処理
        if cursor_row < self.vertical_offset:
            # カーソルが表示範囲より上にある場合
            self.vertical_offset = cursor_row
        elif cursor_row >= self.vertical_offset + viewport.height:
            # カーソルが表示範囲より下にある場合
            self.vertical_offset = max(0, cursor_row - viewport.height + 1)
        
        # 横スクロール処理（行番号の幅を考慮）
        if cursor_col < self.horizontal_offset:
            # カーソルが表示範囲より左にある場合
            self.horizontal_offset = cursor_col
        elif cursor_col >= self.horizontal_offset + viewport.content_width:
            # カーソルが表示範囲より右にある場合
            self.horizontal_offset = max(0, cursor_col - viewport.content_width + 1)
    
    def buffer_to_screen(self, buffer_row: int, buffer_col: int, viewport: ViewportInfo) -> Tuple[int, int]:
        """バッファ座標を画面座標に変換"""
        screen_row = buffer_row - self.vertical_offset + viewport.start_y
        screen_col = buffer_col - self.horizontal_offset + viewport.content_start_x
        return screen_row, screen_col
    
    def screen_to_buffer(self, screen_row: int, screen_col: int, viewport: ViewportInfo) -> Tuple[int, int]:
        """画面座標をバッファ座標に変換"""
        buffer_row = screen_row - viewport.start_y + self.vertical_offset
        buffer_col = screen_col - viewport.content_start_x + self.horizontal_offset
        return buffer_row, buffer_col
    
    def is_visible(self, buffer_row: int, buffer_col: int, viewport: ViewportInfo) -> bool:
        """座標が表示範囲内かチェック"""
        screen_row, screen_col = self.buffer_to_screen(buffer_row, buffer_col, viewport)
        return (viewport.start_y <= screen_row < viewport.start_y + viewport.height and
                viewport.content_start_x <= screen_col < viewport.content_start_x + viewport.content_width)
    
    def get_visible_range(self, total_lines: int, viewport: ViewportInfo) -> Tuple[int, int]:
        """表示される行の範囲を取得"""
        start_line = self.vertical_offset
        end_line = min(start_line + viewport.height, total_lines)
        return start_line, end_line
    
    def get_display_line(self, line: str, viewport: ViewportInfo) -> str:
        """行の表示用文字列を取得（横スクロール適用）"""
        return line[self.horizontal_offset:self.horizontal_offset + viewport.content_width] 