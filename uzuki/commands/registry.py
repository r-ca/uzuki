from uzuki.commands import quit as quit_command, save as save_command
from uzuki.ui.notification import NotificationLevel

COMMANDS = {
    'q': quit_command.QuitCommand,
    'w': save_command.SaveCommand,
    'e': 'edit',  # ファイル編集コマンド
    'set': 'set',  # 設定コマンド
}

class CommandRegistry:
    @staticmethod
    def execute(screen, name: str):
        parts = name.split()
        cmd = parts[0]
        
        if cmd in COMMANDS:
            if isinstance(COMMANDS[cmd], str):
                # 組み込みコマンド
                CommandRegistry._execute_builtin(screen, COMMANDS[cmd], parts[1:])
            else:
                # 外部コマンドクラス
                COMMANDS[cmd]().execute(screen, parts[1:])
        else:
            screen.notify_error(f"Unknown command: {cmd}")
    
    @staticmethod
    def _execute_builtin(screen, cmd_type: str, args: list):
        """組み込みコマンドを実行"""
        if cmd_type == 'edit':
            if args:
                screen.load_file(args[0])
            else:
                screen.notify_warning("Usage: e <filename>")
        elif cmd_type == 'set':
            if len(args) >= 2 and args[0] == 'encoding':
                screen.set_encoding(args[1])
            else:
                screen.notify_warning("Usage: set encoding <encoding>")
