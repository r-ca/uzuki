from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode
from uzuki.commands.registry import CommandRegistry

class CommandMode(BaseMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.cmd_buf = ''

    def handle_key(self, key: Key, raw_code=None):
        if key == Key.ENTER:
            cmd = self.cmd_buf.strip()
            try:
                self.screen.set_message(f"Executing command: {cmd}")
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
        elif key == Key.BACKSP:
            if self.cmd_buf:
                self.cmd_buf = self.cmd_buf[:-1]
        elif key == Key.RAW and raw_code is not None:
            if raw_code < 256:  # 印字可能文字のみ
                char = chr(raw_code)
                self.cmd_buf += char
