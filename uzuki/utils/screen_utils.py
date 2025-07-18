import curses
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class ScreenSize:
    """画面サイズ情報"""
    width: int
    height: int
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
    
    def is_valid(self) -> bool:
        """有効なサイズかチェック"""
        return self.width > 0 and self.height > 0
    
    def fits(self, content_width: int, content_height: int) -> bool:
        """指定されたサイズが収まるかチェック"""
        return content_width <= self.width and content_height <= self.height

class ScreenUtils:
    """画面サイズ関連のユーティリティ"""
    
    @staticmethod
    def get_screen_size(stdscr) -> ScreenSize:
        """現在の画面サイズを取得"""
        height, width = stdscr.getmaxyx()
        return ScreenSize(width, height)
    
    @staticmethod
    def center_text(text: str, width: int) -> str:
        """テキストを中央揃え"""
        if len(text) >= width:
            return text[:width]
        
        padding = (width - len(text)) // 2
        return " " * padding + text
    
    @staticmethod
    def center_box(width: int, height: int, content_width: int, content_height: int) -> Tuple[int, int]:
        """ボックスの中央位置を計算"""
        start_x = (width - content_width) // 2
        start_y = (height - content_height) // 2
        return start_x, start_y
    
    @staticmethod
    def wrap_text(text: str, max_width: int) -> List[str]:
        """テキストを指定幅で折り返し"""
        if len(text) <= max_width:
            return [text]
        
        lines = []
        current_line = ""
        
        for word in text.split():
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += (word + " ")
            else:
                if current_line:
                    lines.append(current_line.rstrip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.rstrip())
        
        return lines
    
    @staticmethod
    def truncate_text(text: str, max_width: int, suffix: str = "...") -> str:
        """テキストを指定幅で切り詰め"""
        if len(text) <= max_width:
            return text
        
        available_width = max_width - len(suffix)
        if available_width <= 0:
            return suffix[:max_width]
        
        return text[:available_width] + suffix
    
    @staticmethod
    def create_border_box(width: int, height: int, title: Optional[str] = None) -> List[str]:
        """ボーダーボックスを作成"""
        if width < 3 or height < 3:
            return []
        
        lines = []
        
        # 上辺
        if title and len(title) <= width - 4:
            title_start = (width - len(title)) // 2
            top_line = "┌" + "─" * (title_start - 1) + title + "─" * (width - title_start - len(title) - 1) + "┐"
        else:
            top_line = "┌" + "─" * (width - 2) + "┐"
        lines.append(top_line)
        
        # 中身
        for _ in range(height - 2):
            lines.append("│" + " " * (width - 2) + "│")
        
        # 下辺
        lines.append("└" + "─" * (width - 2) + "┘")
        
        return lines
    
    @staticmethod
    def create_simple_box(width: int, height: int) -> List[str]:
        """シンプルなボックスを作成"""
        if width < 3 or height < 3:
            return []
        
        lines = []
        lines.append("+" + "-" * (width - 2) + "+")
        
        for _ in range(height - 2):
            lines.append("|" + " " * (width - 2) + "|")
        
        lines.append("+" + "-" * (width - 2) + "+")
        return lines
    
    @staticmethod
    def draw_box(stdscr, start_y: int, start_x: int, lines: List[str], style: int = curses.A_NORMAL):
        """ボックスを描画"""
        for i, line in enumerate(lines):
            if start_y + i < 0:
                continue
            stdscr.addstr(start_y + i, start_x, line, style)
    
    @staticmethod
    def draw_centered_text(stdscr, text: str, y: int, width: int, style: int = curses.A_NORMAL):
        """中央揃えテキストを描画"""
        centered_text = ScreenUtils.center_text(text, width)
        x = (width - len(centered_text)) // 2
        stdscr.addstr(y, x, centered_text, style)
    
    @staticmethod
    def draw_multiline_text(stdscr, lines: List[str], start_y: int, start_x: int, 
                           max_width: int, style: int = curses.A_NORMAL):
        """複数行テキストを描画"""
        for i, line in enumerate(lines):
            if start_y + i < 0:
                continue
            display_line = ScreenUtils.truncate_text(line, max_width)
            stdscr.addstr(start_y + i, start_x, display_line, style)
    
    @staticmethod
    def is_screen_too_small(width: int, height: int, min_width: int = 40, min_height: int = 10) -> bool:
        """画面が小さすぎるかチェック"""
        return width < min_width or height < min_height
    
    @staticmethod
    def get_safe_display_area(width: int, height: int, margin: int = 1) -> ScreenSize:
        """安全な表示エリアを取得"""
        safe_width = max(1, width - (margin * 2))
        safe_height = max(1, height - (margin * 2))
        return ScreenSize(safe_width, safe_height)

class GreetingRenderer:
    """シンプルなGreeting表示クラス"""
    
    def __init__(self):
        self.content_lines = []
        self.bottom_text = ""
    
    def set_content(self, lines: List[str]):
        """コンテンツを設定"""
        self.content_lines = lines
    
    def add_content_line(self, line: str):
        """コンテンツ行を追加"""
        self.content_lines.append(line)
    
    def clear_content(self):
        """コンテンツをクリア"""
        self.content_lines.clear()
    
    def set_bottom_text(self, text: str):
        """下部テキストを設定"""
        self.bottom_text = text
    
    def render_greeting(self, stdscr) -> bool:
        """Greetingを表示"""
        screen_size = ScreenUtils.get_screen_size(stdscr)
        
        # 最小サイズチェック
        if ScreenUtils.is_screen_too_small(screen_size.width, screen_size.height, 30, 10):
            self._render_small_screen_message(stdscr, screen_size)
            return False
        
        # メインのGreetingを表示
        return self._render_main_greeting(stdscr, screen_size)
    
    def _render_main_greeting(self, stdscr, screen_size: ScreenSize) -> bool:
        """メインのGreetingを表示"""
        # 必要な高さを計算
        required_height = len(self.content_lines)
        if self.bottom_text:
            required_height += 2  # 空行 + 下部テキスト
        
        # ボックスのサイズを計算
        box_width = min(80, screen_size.width - 4)
        box_height = min(required_height + 2, screen_size.height - 4)  # ボーダー分を追加
        
        # ボックスを中央に配置
        start_x, start_y = ScreenUtils.center_box(screen_size.width, screen_size.height, box_width, box_height)
        
        # ボックスを作成
        box_lines = ScreenUtils.create_border_box(box_width, box_height)
        
        # ボックスを描画
        ScreenUtils.draw_box(stdscr, start_y, start_x, box_lines, curses.A_BOLD)
        
        # 内容を描画
        content_y = start_y + 1
        content_width = box_width - 2  # ボーダー分を引く
        
        # コンテンツ行を描画
        for line in self.content_lines:
            if content_y < start_y + box_height - 2:
                ScreenUtils.draw_centered_text(stdscr, line, content_y, content_width, curses.A_NORMAL)
                content_y += 1
        
        # 下部テキストを描画
        if self.bottom_text and content_y < start_y + box_height - 2:
            content_y += 1  # 空行
            ScreenUtils.draw_centered_text(stdscr, self.bottom_text, content_y, content_width, curses.A_BOLD)
        
        stdscr.refresh()
        return True
    
    def _render_small_screen_message(self, stdscr, screen_size: ScreenSize):
        """小さな画面用のメッセージを表示"""
        message = "Screen too small. Please resize to at least 30x10."
        centered_message = ScreenUtils.center_text(message, screen_size.width)
        
        y = screen_size.height // 2
        x = (screen_size.width - len(centered_message)) // 2
        
        stdscr.addstr(y, x, centered_message, curses.A_BOLD)
        stdscr.refresh()

# プリセットAA
class PresetAsciiArt:
    """プリセットAAコレクション"""
    
    @staticmethod
    def get_uzuki_logo() -> List[str]:
        """Uzukiロゴ"""
        return [
            "  _   _                     _ _ ",
            " | | | |                   (_) |",
            " | | | |_   _ _ __   __ _   _| |",
            " | | | | | | | '_ \\ / _` | | | |",
            " | |_| | |_| | | | | (_| | | | |",
            "  \\___/ \\__,_|_| |_|\\__, | |_|_|",
            "                      __/ |      ",
            "                     |___/       "
        ]
    
    @staticmethod
    def get_simple_logo() -> List[str]:
        """シンプルロゴ"""
        return [
            "  _   _",
            " | | | |",
            " | | | |_   _ _ __",
            " | | | | | | | '_ \\",
            " | |_| | |_| | | | |",
            "  \\___/ \\__,_|_| |_|"
        ]
    
    @staticmethod
    def get_minimal_logo() -> List[str]:
        """ミニマルロゴ"""
        return [
            " _   _",
            "| | | |",
            "| | | |_   _ _ __",
            "| |_| | | | | '_ \\",
            " \\___/ \\__,_|_| |_|"
        ]
    
    @staticmethod
    def get_cat() -> List[str]:
        """猫のAA"""
        return [
            " /\\_/\\",
            "( o.o )",
            " > ^ <",
            "  \\_/ "
        ]
    
    @staticmethod
    def get_robot() -> List[str]:
        """ロボットのAA"""
        return [
            "  [o.o]",
            " /|___|\\",
            "  |   |",
            " / \\___/ \\",
            "  |     |"
        ]
    
    @staticmethod
    def get_star() -> List[str]:
        """星のAA"""
        return [
            "    *",
            "   ***",
            "  *****",
            " *******",
            "*********",
            " *******",
            "  *****",
            "   ***",
            "    *"
        ] 