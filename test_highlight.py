#!/usr/bin/env python3
"""
ハイライト機能テストスクリプト
"""

import curses
import sys
import os

# uzukiパッケージをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uzuki.ui.line_numbers import LineDisplayManager, LineHighlighter
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor

def test_highlight(stdscr):
    """ハイライト機能をテスト"""
    # 色の初期化
    curses.start_color()
    curses.use_default_colors()
    
    # 256色対応の確認
    if curses.COLORS >= 256:
        # 256色モードで色ペアを定義
        for i in range(1, 16):
            curses.init_pair(i, i, -1)
    else:
        # 標準8色で色ペアを定義
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    # コンポーネントを初期化
    line_display = LineDisplayManager()
    buffer = Buffer()
    cursor = Cursor()
    
    # テスト用のコンテンツを設定
    test_lines = [
        "This is a normal line",
        "This line has an error",
        "This line has a warning",
        "This line has info",
        "This line has success",
        "This is another normal line",
        "This line is very long and should trigger horizontal scrolling when the cursor is at the end of this line",
        "Short line",
        "Another line",
        "Last line"
    ]
    buffer.lines = test_lines
    
    # ハイライトを設定
    line_display.highlighter.highlight_error_line(2)    # 2行目をエラー
    line_display.highlighter.highlight_warning_line(3)  # 3行目を警告
    line_display.highlighter.highlight_info_line(4)     # 4行目を情報
    line_display.highlighter.highlight_success_line(5)  # 5行目を成功
    
    # カーソル位置を設定
    cursor.row = 0
    cursor.col = 0
    
    # 画面サイズを取得
    height, width = stdscr.getmaxyx()
    
    # メインループ
    while True:
        # 画面をクリア
        stdscr.clear()
        
        # エディタコンテンツを描画
        line_num_width, display_lines = line_display.render_editor_content(
            stdscr, buffer.lines, cursor.row, cursor.col,
            0, 0, height - 1, width
        )
        
        # カーソル位置を設定
        screen_cursor_row = cursor.row - line_display.get_vertical_offset()
        screen_cursor_col = cursor.col - line_display.get_horizontal_offset()
        
        if (0 <= screen_cursor_row < height - 1 and 
            0 <= screen_cursor_col < width - line_num_width):
            stdscr.move(screen_cursor_row, line_num_width + screen_cursor_col)
        
        # 画面を更新
        stdscr.refresh()
        
        # キー入力を待つ
        key = stdscr.getch()
        
        # キー処理
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            cursor.row = max(0, cursor.row - 1)
        elif key == curses.KEY_DOWN:
            cursor.row = min(len(buffer.lines) - 1, cursor.row + 1)
        elif key == curses.KEY_LEFT:
            cursor.col = max(0, cursor.col - 1)
        elif key == curses.KEY_RIGHT:
            cursor.col = min(len(buffer.lines[cursor.row]), cursor.col + 1)
        elif key == ord('h'):
            # ハイライトを切り替え
            line_display.toggle_current_line_highlight()
        elif key == ord('n'):
            # 行番号を切り替え
            line_display.toggle_line_numbers()

if __name__ == "__main__":
    curses.wrapper(test_highlight) 