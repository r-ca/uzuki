import curses
import sys
import argparse
from uzuki.ui.screen import Screen

def parse_arguments():
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        description='Uzuki - A Vim-like text editor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uzuki                    # 新規ファイルで起動
  uzuki file.txt          # ファイルを開く
  uzuki /path/to/file.py  # 絶対パスでファイルを開く
  uzuki .                 # カレントディレクトリのファイルブラウザーを開く
  uzuki /path/to/dir      # 指定ディレクトリのファイルブラウザーを開く
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='File to open or directory to browse'
    )
    
    parser.add_argument(
        '--encoding',
        '-e',
        default='utf-8',
        help='Default encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--version',
        '-v',
        action='version',
        version='Uzuki 0.1.0'
    )
    
    return parser.parse_args()

def main():
    """メイン関数"""
    args = parse_arguments()
    
    # 初期ファイル/ディレクトリを設定
    initial_path = args.file
    
    def run_editor(stdscr):
        screen = Screen(initial_path)
        screen.run(stdscr)
    
    try:
        curses.wrapper(run_editor)
    except KeyboardInterrupt:
        print("\nUzuki terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
