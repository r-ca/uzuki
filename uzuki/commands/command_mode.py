from uzuki.input.keycodes import Key
from uzuki.modes.base_mode import BaseMode

class CommandMode(BaseMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.cmd_buf = ''

    def handle_key(self, key: Key):
        if key == Key.ENTER:
            if self.cmd_buf == 'q':
                raise SystemExit
            elif self.cmd_buf == 'w':
                self.screen.save_file()
            self.screen.mode = self.screen.normal_mode
        else:
            self.cmd_buf += chr(key.value)
