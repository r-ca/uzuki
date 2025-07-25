"""
Viewport management for horizontal scrolling

Manages the visible area of the editor, including horizontal scrolling
for long lines that exceed screen width.
"""

from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class Viewport:
    """ビューポート情報"""
    start_x: int = 0
    start_y: int = 0
    width: int = 80
    height: int = 24
    max_x: int = 0
    max_y: int = 0

class ViewportManager:
    """ビューポート管理システム"""
    
    def __init__(self):
        self.viewport = Viewport()
        self.scroll_margin = 5  # スクロール開始マージン
    
    def set_screen_size(self, width: int, height: int):
        """画面サイズを設定"""
        self.viewport.width = width
        self.viewport.height = height
    
    def set_content_size(self, max_x: int, max_y: int):
        """コンテンツサイズを設定"""
        self.viewport.max_x = max_x
        self.viewport.max_y = max_y
    
    def get_visible_range(self) -> Tuple[int, int, int, int]:
        """表示範囲を取得 (start_x, end_x, start_y, end_y)"""
        end_x = min(self.viewport.start_x + self.viewport.width, self.viewport.max_x)
        end_y = min(self.viewport.start_y + self.viewport.height, self.viewport.max_y)
        return (self.viewport.start_x, end_x, self.viewport.start_y, end_y)
    
    def scroll_to_cursor(self, cursor_x: int, cursor_y: int):
        """カーソル位置にスクロール"""
        # 縦スクロール
        if cursor_y < self.viewport.start_y:
            self.viewport.start_y = cursor_y
        elif cursor_y >= self.viewport.start_y + self.viewport.height:
            self.viewport.start_y = cursor_y - self.viewport.height + 1
        
        # 横スクロール
        if cursor_x < self.viewport.start_x + self.scroll_margin:
            self.viewport.start_x = max(0, cursor_x - self.scroll_margin)
        elif cursor_x >= self.viewport.start_x + self.viewport.width - self.scroll_margin:
            self.viewport.start_x = cursor_x - self.viewport.width + self.scroll_margin
        
        # 境界チェック
        self.viewport.start_x = max(0, min(self.viewport.start_x, self.viewport.max_x - self.viewport.width))
        self.viewport.start_y = max(0, min(self.viewport.start_y, self.viewport.max_y - self.viewport.height))
    
    def scroll_horizontal(self, direction: int):
        """横スクロール（direction: 1=右, -1=左）"""
        new_start_x = self.viewport.start_x + direction * (self.viewport.width // 2)
        self.viewport.start_x = max(0, min(new_start_x, self.viewport.max_x - self.viewport.width))
    
    def scroll_vertical(self, direction: int):
        """縦スクロール（direction: 1=下, -1=上）"""
        new_start_y = self.viewport.start_y + direction * (self.viewport.height // 2)
        self.viewport.start_y = max(0, min(new_start_y, self.viewport.max_y - self.viewport.height))
    
    def center_on_cursor(self, cursor_x: int, cursor_y: int):
        """カーソルを中心に配置"""
        self.viewport.start_x = max(0, cursor_x - self.viewport.width // 2)
        self.viewport.start_y = max(0, cursor_y - self.viewport.height // 2)
        
        # 境界チェック
        self.viewport.start_x = min(self.viewport.start_x, self.viewport.max_x - self.viewport.width)
        self.viewport.start_y = min(self.viewport.start_y, self.viewport.max_y - self.viewport.height)
    
    def is_visible(self, x: int, y: int) -> bool:
        """指定位置が表示範囲内かチェック"""
        return (self.viewport.start_x <= x < self.viewport.start_x + self.viewport.width and
                self.viewport.start_y <= y < self.viewport.start_y + self.viewport.height)
    
    def screen_to_content(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """画面座標をコンテンツ座標に変換"""
        content_x = screen_x + self.viewport.start_x
        content_y = screen_y + self.viewport.start_y
        return (content_x, content_y)
    
    def content_to_screen(self, content_x: int, content_y: int) -> Tuple[int, int]:
        """コンテンツ座標を画面座標に変換"""
        screen_x = content_x - self.viewport.start_x
        screen_y = content_y - self.viewport.start_y
        return (screen_x, screen_y)
    
    def get_scroll_info(self) -> dict:
        """スクロール情報を取得"""
        return {
            'horizontal': {
                'position': self.viewport.start_x,
                'max': max(0, self.viewport.max_x - self.viewport.width),
                'percentage': (self.viewport.start_x / max(1, self.viewport.max_x - self.viewport.width)) * 100
            },
            'vertical': {
                'position': self.viewport.start_y,
                'max': max(0, self.viewport.max_y - self.viewport.height),
                'percentage': (self.viewport.start_y / max(1, self.viewport.max_y - self.viewport.height)) * 100
            }
        } 