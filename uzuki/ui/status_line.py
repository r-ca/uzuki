import curses
from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass

@dataclass
class StatusSegment:
    """ステータスラインのセグメント"""
    content: str
    width: Optional[int] = None  # Noneの場合は内容に応じて自動調整
    align: str = 'left'  # 'left', 'center', 'right'
    style: int = curses.A_NORMAL
    priority: int = 0  # 表示優先度（高いほど優先）

class StatusLineManager:
    """ステータスライン管理クラス"""
    def __init__(self):
        self.segments: Dict[str, StatusSegment] = {}
        self.segment_order: List[str] = []
        self.separator = ' | '
        self.default_style = curses.A_REVERSE
        
    def add_segment(self, name: str, content: str, width: Optional[int] = None, 
                   align: str = 'left', style: int = curses.A_NORMAL, priority: int = 0):
        """セグメントを追加"""
        self.segments[name] = StatusSegment(content, width, align, style, priority)
        if name not in self.segment_order:
            self.segment_order.append(name)
    
    def update_segment(self, name: str, content: str):
        """セグメントの内容を更新"""
        if name in self.segments:
            self.segments[name].content = content
    
    def remove_segment(self, name: str):
        """セグメントを削除"""
        if name in self.segments:
            del self.segments[name]
        if name in self.segment_order:
            self.segment_order.remove(name)
    
    def clear(self):
        """すべてのセグメントをクリア"""
        self.segments.clear()
        self.segment_order.clear()
    
    def set_separator(self, separator: str):
        """セパレータを設定"""
        self.separator = separator
    
    def render_content(self, width: int) -> str:
        """ステータスラインの内容をレンダリング"""
        if not self.segments:
            return ''
        
        # 優先度順にソート
        sorted_segments = sorted(
            [(name, segment) for name, segment in self.segments.items()],
            key=lambda x: x[1].priority,
            reverse=True
        )
        
        # 各セグメントの幅を計算
        available_width = width
        segment_widths = {}
        
        # まず固定幅のセグメントを処理
        for name, segment in sorted_segments:
            if segment.width is not None:
                segment_widths[name] = segment.width
                available_width -= segment.width
            else:
                segment_widths[name] = 0
        
        # 残りの幅を可変幅セグメントに分配
        variable_segments = [name for name, segment in sorted_segments if segment.width is None]
        if variable_segments and available_width > 0:
            base_width = available_width // len(variable_segments)
            remainder = available_width % len(variable_segments)
            
            for i, name in enumerate(variable_segments):
                segment_widths[name] = base_width + (1 if i < remainder else 0)
        
        # セグメントを構築
        result_parts = []
        for name, segment in sorted_segments:
            if name not in segment_widths or segment_widths[name] <= 0:
                continue
                
            content = segment.content
            seg_width = segment_widths[name]
            
            # 幅に合わせて切り詰めまたはパディング
            if len(content) > seg_width:
                content = content[:seg_width-3] + "..."
            elif len(content) < seg_width:
                if segment.align == 'center':
                    padding = (seg_width - len(content)) // 2
                    content = ' ' * padding + content + ' ' * (seg_width - len(content) - padding)
                elif segment.align == 'right':
                    content = ' ' * (seg_width - len(content)) + content
                else:  # left
                    content = content + ' ' * (seg_width - len(content))
            
            result_parts.append(content)
        
        return self.separator.join(result_parts)
    
    def update(self, content: str):
        """ステータスラインの内容を更新"""
        # 一時的なセグメントとして保存
        self.add_segment('temp', content, width=None, align='left', priority=0)
    
    def render(self, stdscr):
        """ステータスラインを描画"""
        height, width = stdscr.getmaxyx()
        content = self.render_content(width)
        
        # 最下行に描画
        y = height - 1
        try:
            stdscr.addstr(y, 0, content, self.default_style)
        except curses.error:
            # 画面端でのエラーを防ぐ
            safe_content = content[:width-1]
            if safe_content:
                stdscr.addstr(y, 0, safe_content, self.default_style)
    
    def get_style(self, name: str) -> int:
        """セグメントのスタイルを取得"""
        if name in self.segments:
            return self.segments[name].style
        return self.default_style

class StatusLineBuilder:
    """ステータスライン構築用のビルダークラス"""
    def __init__(self, manager: StatusLineManager):
        self.manager = manager
    
    def add_segment(self, name: str, content: str, width=None, align: str = 'left', priority: int = 0):
        """セグメントを追加"""
        self.manager.add_segment(name, content, width, align, priority)
        return self
    
    def build(self) -> str:
        """ステータスラインを構築"""
        # 画面幅を取得（仮の値、実際は適切に取得する必要がある）
        width = 80
        return self.manager.render_content(width)
    
    def mode(self, mode_name: str):
        """モード表示セグメント"""
        self.manager.add_segment('mode', f"--{mode_name.upper()}--", 
                                width=15, align='left', priority=100)
        return self
    
    def filename(self, filename: str):
        """ファイル名セグメント"""
        self.manager.add_segment('filename', filename, 
                                width=30, align='left', priority=90)
        return self
    
    def position(self, row: int, col: int):
        """カーソル位置セグメント"""
        self.manager.add_segment('position', f"{row+1}:{col+1}", 
                                width=10, align='right', priority=80)
        return self
    
    def sequence(self, sequence: str):
        """キーシーケンスセグメント"""
        if sequence:
            self.manager.add_segment('sequence', f"[{sequence}]", 
                                    width=20, align='center', priority=70)
        return self
    
    def command(self, command: str):
        """コマンド入力セグメント"""
        self.manager.add_segment('command', f":{command}", 
                                width=None, align='left', priority=95)
        return self
    
    def encoding(self, encoding: str):
        """文字エンコーディングセグメント"""
        self.manager.add_segment('encoding', f"[{encoding}]", 
                                width=12, align='right', priority=60)
        return self
    
    def line_count(self, total_lines: int):
        """行数セグメント"""
        self.manager.add_segment('line_count', f"L{total_lines}", 
                                width=8, align='right', priority=50)
        return self
    
    def custom(self, name: str, content: str, width: Optional[int] = None, 
               align: str = 'left', priority: int = 0):
        """カスタムセグメント"""
        self.manager.add_segment(name, content, width, align, priority)
        return self 