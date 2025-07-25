"""
Color Manager - True Color対応のカラー管理

coloramaライブラリを使用して確実なTrue Color対応を実現
"""

import curses
import colorama
from colorama import Fore, Back, Style
from typing import Dict, Optional, Tuple

class ColorManager:
    """True Color対応のカラーマネージャー"""
    
    def __init__(self):
        self._initialized = False
        self._color_pairs = {}
        self._true_color_support = False
        self._fallback_mode = False
        
        # 基本色定義
        self.colors = {
            'black': 0,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magenta': 5,
            'cyan': 6,
            'white': 7,
            'bright_black': 8,
            'bright_red': 9,
            'bright_green': 10,
            'bright_yellow': 11,
            'bright_blue': 12,
            'bright_magenta': 13,
            'bright_cyan': 14,
            'bright_white': 15,
        }
        
        # スタイル定義
        self.styles = {
            'normal': curses.A_NORMAL,
            'bold': curses.A_BOLD,
            'dim': curses.A_DIM,
            'reverse': curses.A_REVERSE,
            'standout': curses.A_STANDOUT,
            'underline': curses.A_UNDERLINE,
        }
    
    def initialize(self):
        """カラーシステムを初期化"""
        if self._initialized:
            return
        
        # coloramaを初期化
        colorama.init()
        
        try:
            # cursesの色サポートを確認
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
                
                # True Color対応を確認
                self._true_color_support = self._check_true_color_support()
                
                if self._true_color_support:
                    self._initialize_true_color()
                else:
                    self._initialize_256_color()
            else:
                self._fallback_mode = True
                self._initialize_fallback()
                
        except Exception as e:
            # エラーが発生した場合はフォールバックモード
            self._fallback_mode = True
            self._initialize_fallback()
        
        self._initialized = True
    
    def _check_true_color_support(self) -> bool:
        """True Color対応を確認"""
        try:
            # 環境変数で確認
            import os
            term = os.environ.get('TERM', '')
            if 'truecolor' in term.lower() or '24bit' in term.lower():
                return True
            
            # 色数を確認
            if curses.COLORS >= 16777216:  # 24bit color
                return True
            
            return False
        except:
            return False
    
    def _initialize_true_color(self):
        """True Colorモードを初期化"""
        # 基本色ペアを定義
        self._define_color_pairs()
    
    def _initialize_256_color(self):
        """256色モードを初期化"""
        # 256色の色ペアを定義
        for i in range(1, 17):
            try:
                curses.init_pair(i, i, -1)
            except:
                pass
    
    def _initialize_fallback(self):
        """フォールバックモードを初期化"""
        # 基本的な色ペアのみ定義
        try:
            curses.init_pair(1, curses.COLOR_RED, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_BLUE, -1)
            curses.init_pair(5, curses.COLOR_MAGENTA, -1)
            curses.init_pair(6, curses.COLOR_CYAN, -1)
            curses.init_pair(7, curses.COLOR_WHITE, -1)
        except:
            pass
    
    def _define_color_pairs(self):
        """色ペアを定義"""
        # 基本色ペア
        color_definitions = [
            (1, 'red', -1),
            (2, 'green', -1),
            (3, 'yellow', -1),
            (4, 'blue', -1),
            (5, 'magenta', -1),
            (6, 'cyan', -1),
            (7, 'white', -1),
            (8, 'black', 'white'),  # 反転（黒文字白背景）
            (9, 'bright_red', -1),
            (10, 'bright_green', -1),
            (11, 'bright_yellow', -1),
            (12, 'bright_blue', -1),
            (13, 'bright_magenta', -1),
            (14, 'bright_cyan', -1),
            (15, 'bright_white', -1),
            # カレント行用の色ペア（背景色付き）
            (16, 'black', 'bright_cyan'),  # 黒文字 + 明るいシアン背景
        ]
        
        for pair_id, fg_color, bg_color in color_definitions:
            try:
                fg = self.colors.get(fg_color, 7)
                bg = self.colors.get(bg_color, -1) if bg_color != -1 else -1
                curses.init_pair(pair_id, fg, bg)
            except:
                pass
    
    def get_color_pair(self, pair_id: int) -> int:
        """色ペアを取得"""
        if not self._initialized:
            self.initialize()
        
        try:
            return curses.color_pair(pair_id)
        except:
            return curses.A_NORMAL
    
    def get_style(self, color_pair: int = 0, style: str = 'normal') -> int:
        """スタイルを取得"""
        if not self._initialized:
            self.initialize()
        
        result = self.styles.get(style, curses.A_NORMAL)
        if color_pair > 0:
            try:
                result |= curses.color_pair(color_pair)
            except:
                pass
        
        return result
    
    def create_style(self, fg_color: str = 'white', bg_color: str = None, 
                    style: str = 'normal') -> int:
        """カスタムスタイルを作成"""
        if not self._initialized:
            self.initialize()
        
        # 色ペアIDを生成
        pair_id = self._get_or_create_pair_id(fg_color, bg_color)
        
        return self.get_style(pair_id, style)
    
    def _get_or_create_pair_id(self, fg_color: str, bg_color: str = None) -> int:
        """色ペアIDを取得または作成"""
        key = f"{fg_color}_{bg_color or 'default'}"
        
        if key in self._color_pairs:
            return self._color_pairs[key]
        
        # 新しいペアIDを割り当て
        pair_id = len(self._color_pairs) + 16  # 基本色ペアの後に配置
        
        try:
            fg = self.colors.get(fg_color, 7)
            bg = self.colors.get(bg_color, -1) if bg_color else -1
            curses.init_pair(pair_id, fg, bg)
            self._color_pairs[key] = pair_id
        except:
            pair_id = 7  # フォールバック
        
        return pair_id
    
    def get_error_style(self) -> int:
        """エラー用スタイル"""
        return self.get_style(9, 'bold')  # 明るい赤 + 太字
    
    def get_warning_style(self) -> int:
        """警告用スタイル"""
        return self.get_style(11, 'bold')  # 明るい黄 + 太字
    
    def get_success_style(self) -> int:
        """成功用スタイル"""
        return self.get_style(10, 'bold')  # 明るい緑 + 太字
    
    def get_info_style(self) -> int:
        """情報用スタイル"""
        return self.get_style(12, 'bold')  # 明るい青 + 太字
    
    def get_highlight_style(self) -> int:
        """ハイライト用スタイル"""
        return self.get_style(13, 'bold')  # 明るいマゼンタ + 太字
    
    def get_current_line_style(self) -> int:
        """カレント行用スタイル（反転色）"""
        try:
            if curses.has_colors():
                # カレント行は反転色（背景色付き）
                return curses.color_pair(8)  # 反転色ペア
            else:
                # 色が使えない場合は反転
                return curses.A_REVERSE
        except:
            return curses.A_REVERSE
    
    def get_reverse_style(self) -> int:
        """反転用スタイル"""
        return self.get_style(8)  # 黒背景白文字
    
    def cleanup(self):
        """クリーンアップ"""
        colorama.deinit()

# グローバルインスタンス
color_manager = ColorManager() 