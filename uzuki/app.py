#!/usr/bin/env python3
"""
Uzuki - A Vim-like text editor in Python
"""

import argparse
import sys
import curses
from typing import Optional
from uzuki.ui.screen import Screen

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Uzuki - A Vim-like text editor in Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uzuki                    # Start editor
  uzuki file.txt          # Open file.txt
  uzuki /path/to/dir      # Open file browser in directory
  uzuki --no-greeting     # Start without greeting screen
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='File or directory to open'
    )
    
    parser.add_argument(
        '--encoding',
        '-e',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--version',
        '-v',
        action='version',
        version='Uzuki v0.1.0'
    )
    
    parser.add_argument(
        '--no-greeting',
        action='store_true',
        help='Start without greeting screen'
    )
    
    args = parser.parse_args()
    
    # エディタを開始
    try:
        # スクリーンを作成
        screen = Screen(
            initial_file=args.file,
            show_greeting=not args.no_greeting
        )
        
        # エンコーディングを設定
        if args.encoding:
            screen.file.file_manager.encoding = args.encoding
        
        # cursesでエディタを実行
        curses.wrapper(screen.run)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
