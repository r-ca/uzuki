#!/usr/bin/env python3
"""
シンプルなGreetingのテストスクリプト
"""

import curses
from uzuki.ui.screen import Screen

def test_greeting():
    """Greetingのテスト"""
    
    def run_test(stdscr):
        # スクリーンを作成（Greeting表示あり）
        screen = Screen(show_greeting=True)
        
        # 基本的なGreeting
        screen.set_greeting_content([
            "Welcome to Uzuki",
            "A Vim-like text editor in Python",
            "",
            "Press any key to continue..."
        ])
        screen.greeting.render_greeting(stdscr)
        stdscr.getch()
        
        # カスタムコンテンツ
        screen.set_greeting_content([
            "Hello World!",
            "This is a custom greeting",
            "",
            "You can add any content you want",
            "Just like this!"
        ])
        screen.set_greeting_bottom_text("Press any key to start...")
        screen.greeting.render_greeting(stdscr)
        stdscr.getch()
        
        # コンテンツを追加
        screen.add_greeting_content_line("")
        screen.add_greeting_content_line("Additional line added!")
        screen.greeting.render_greeting(stdscr)
        stdscr.getch()
        
        # コンテンツをクリア
        screen.clear_greeting_content()
        screen.add_greeting_content_line("Content cleared!")
        screen.greeting.render_greeting(stdscr)
        stdscr.getch()
        
        print("All tests completed!")
    
    try:
        curses.wrapper(run_test)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Simple Greeting Test")
    print("===================")
    
    # インタラクティブテスト
    test_greeting() 