#!/usr/bin/env python3
"""
True Color対応テスト

新しいColorManagerの動作をテストする
"""

import curses
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uzuki.ui.color_manager import color_manager

def test_colors(stdscr):
    """色のテスト"""
    # カラーマネージャーを初期化
    color_manager.initialize()
    
    # 画面サイズを取得
    height, width = stdscr.getmaxyx()
    
    # テスト用のテキスト
    test_lines = [
        "True Color Test - Uzuki Editor",
        "",
        "Error line (should be bright red)",
        "Warning line (should be bright yellow)", 
        "Success line (should be bright green)",
        "Info line (should be bright blue)",
        "Highlight line (should be bright magenta)",
        "Current line (should have white background)",
        "",
        "Press any key to exit..."
    ]
    
    # 行を描画
    for i, line in enumerate(test_lines):
        if i >= height - 2:  # 画面端を避ける
            break
            
        # 行のスタイルを決定
        if "Error" in line:
            style = color_manager.get_error_style()
        elif "Warning" in line:
            style = color_manager.get_warning_style()
        elif "Success" in line:
            style = color_manager.get_success_style()
        elif "Info" in line:
            style = color_manager.get_info_style()
        elif "Highlight" in line:
            style = color_manager.get_highlight_style()
        elif "Current" in line:
            style = color_manager.get_current_line_style()
        else:
            style = curses.A_NORMAL
            
        try:
            stdscr.addstr(i, 0, line, style)
        except curses.error:
            pass
    
    # 画面を更新
    stdscr.refresh()
    
    # キー入力を待つ
    stdscr.getch()

def main():
    """メイン関数"""
    try:
        curses.wrapper(test_colors)
    except KeyboardInterrupt:
        print("Test interrupted")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 