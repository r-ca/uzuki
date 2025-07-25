from uzuki.modes.base_mode import BaseMode
from uzuki.commands.registry import CommandRegistry
from uzuki.ui.notification import NotificationLevel

class CommandMode(BaseMode):
    """Command mode - コマンド実行モード"""
    def __init__(self, screen):
        super().__init__(screen, 'command')
        self.cmd_buf = ''
    
    def get_action_handlers(self):
        """Command modeのアクションハンドラー"""
        return {
            # モード切り替え
            'enter_normal_mode': lambda: self.screen.set_mode('normal'),
            
            # コマンド実行
            'execute_command': self._execute_command,
            'delete_backward': self._delete_backward,
        }
    
    def handle_default(self, key_info):
        """デフォルト処理：文字入力・バックスペース"""
        if key_info.key_name == 'backspace':
            self._delete_backward()
            return
        if key_info.is_printable and key_info.char:
            self.cmd_buf += key_info.char
            # 画面更新フラグを設定
            self.screen.editor.needs_redraw = True
    
    def _execute_command(self):
        """コマンドを実行"""
        cmd = self.cmd_buf.strip()
        try:
            self.screen.notify_info(f"Executing: {cmd}")
            CommandRegistry.execute(self.screen, cmd)
        except SystemExit:
            # 終了コマンドハンドリング
            raise
        except Exception as e:
            self.screen.notify_error(f"Command error: {e}")
        finally:
            self.screen.set_mode('normal')
            self.cmd_buf = ''
    
    def _delete_backward(self):
        """バックスペース処理"""
        if self.cmd_buf:
            self.cmd_buf = self.cmd_buf[:-1]
            # 画面更新フラグを設定
            self.screen.editor.needs_redraw = True
