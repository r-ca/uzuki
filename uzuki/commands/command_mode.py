from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode
from uzuki.commands.registry import CommandRegistry

class CommandMode(BaseMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.cmd_buf = ''

    def handle_key(self, key: Key):
        if key == Key.ENTER:
            cmd = self.cmd_buf.strip()
            try:
                CommandRegistry.execute(self.screen, cmd)
            except SystemExit:
                # 終了コマンドハンドリング
                raise
            except Exception as e:
                self.screen.set_message(f"Error executing command: {e}")
            finally:
                self.screen.mode = self.screen.normal_mode
                self.cmd_buf = ''
        elif key == Key.ESC:
            self.screen.mode = self.screen.normal_mode
            self.cmd_buf = ''
        else:
            self.cmd_buf += chr(key.value) if key.value < 256 else ''
