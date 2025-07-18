import os
from typing import Optional
from uzuki.ui.notification import NotificationLevel

class CommandRegistry:
    """コマンドレジストリ"""
    
    @staticmethod
    def execute(screen, cmd: str):
        """コマンドを実行"""
        if not cmd:
            return
        
        parts = cmd.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # ファイル操作コマンド
        if command == 'e' or command == 'edit':
            if args:
                screen.load_file(args[0])
            else:
                screen.notify_error("Usage: :e <filename>")
        
        elif command == 'w' or command == 'write':
            if args:
                screen.save_file(args[0])
            else:
                screen.save_file()
        
        elif command == 'q' or command == 'quit':
            screen.quit()
        
        elif command == 'wq':
            screen.save_file()
            screen.quit()
        
        elif command == 'q!':
            screen.quit()
        
        # エンコーディング設定
        elif command == 'set' and len(args) >= 2 and args[0] == 'encoding':
            screen.set_encoding(args[1])
        
        # ファイルブラウザー
        elif command == 'Explore' or command == 'E':
            directory = args[0] if args else None
            screen.open_file_browser(directory)
        
        # 行番号表示
        elif command == 'set' and len(args) >= 2 and args[0] == 'number':
            if args[1] in ['on', 'true', '1']:
                if not screen.line_display.line_numbers.show_line_numbers:
                    screen.toggle_line_numbers()
            elif args[1] in ['off', 'false', '0']:
                if screen.line_display.line_numbers.show_line_numbers:
                    screen.toggle_line_numbers()
        
        elif command == 'set' and len(args) >= 2 and args[0] == 'nonumber':
            if screen.line_display.line_numbers.show_line_numbers:
                screen.toggle_line_numbers()
        
        # カレント行ハイライト
        elif command == 'set' and len(args) >= 2 and args[0] == 'cursorline':
            if args[1] in ['on', 'true', '1']:
                if not screen.line_display.line_numbers.current_line_highlight:
                    screen.toggle_current_line_highlight()
            elif args[1] in ['off', 'false', '0']:
                if screen.line_display.line_numbers.current_line_highlight:
                    screen.toggle_current_line_highlight()
        
        elif command == 'set' and len(args) >= 2 and args[0] == 'nocursorline':
            if screen.line_display.line_numbers.current_line_highlight:
                screen.toggle_current_line_highlight()
        
        # ルーラー表示
        elif command == 'set' and len(args) >= 2 and args[0] == 'ruler':
            if args[1] in ['on', 'true', '1']:
                if not screen.line_display.show_ruler:
                    screen.toggle_ruler()
            elif args[1] in ['off', 'false', '0']:
                if screen.line_display.show_ruler:
                    screen.toggle_ruler()
        
        elif command == 'set' and len(args) >= 2 and args[0] == 'noruler':
            if screen.line_display.show_ruler:
                screen.toggle_ruler()
        
        # 設定関連コマンド
        elif command == 'config':
            if not args:
                screen.print_config()
            elif len(args) == 1:
                screen.print_config(args[0])
            elif len(args) >= 3 and args[0] == 'set':
                section = args[1]
                key = args[2]
                value = ' '.join(args[3:]) if len(args) > 3 else ''
                # 値の型を推測
                if value.lower() in ['true', 'on', '1']:
                    value = True
                elif value.lower() in ['false', 'off', '0']:
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                screen.set_config(section, key, value)
                screen.notify_success(f"Config set: {section}.{key} = {value}")
            elif len(args) >= 2 and args[0] == 'get':
                section = args[1]
                key = args[2] if len(args) > 2 else None
                value = screen.get_config(section, key)
                screen.notify_info(f"Config: {section}.{key if key else 'all'} = {value}")
            elif len(args) >= 2 and args[0] == 'reset':
                section = args[1] if len(args) > 1 else None
                screen.reset_config(section)
                screen.notify_success(f"Config reset: {section if section else 'all'}")
            elif len(args) >= 2 and args[0] == 'import':
                filepath = args[1]
                screen.import_config(filepath)
                screen.notify_success(f"Config imported from: {filepath}")
            else:
                screen.notify_error("Usage: :config [get|set|reset|import] [args...]")
        
        # ヘルプ
        elif command == 'help' or command == 'h':
            help_text = """
Available commands:
  :e[dit] <file>     - Edit file
  :w[rite] [file]    - Save file
  :q[uit]            - Quit
  :wq                - Save and quit
  :q!                - Quit without saving
  :Explore [dir]     - Open file browser
  :set encoding <enc> - Set file encoding
  :set number        - Show line numbers
  :set nonumber      - Hide line numbers
  :set cursorline    - Highlight current line
  :set nocursorline  - Don't highlight current line
  :set ruler         - Show ruler
  :set noruler       - Hide ruler
  :config            - Show all config
  :config <section>  - Show section config
  :config set <section> <key> <value> - Set config
  :config get <section> [key] - Get config
  :config reset [section] - Reset config
  :config import <file> - Import config
            """
            for line in help_text.strip().split('\n'):
                screen.notify_info(line)
        
        else:
            screen.notify_error(f"Unknown command: {command}")
