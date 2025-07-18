import curses
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.input.handler import InputHandler
from uzuki.modes.normal_mode import NormalMode
from uzuki.modes.insert_mode import InsertMode
from uzuki.commands.command_mode import CommandMode
from uzuki.keymaps.manager import KeyMapManager

class Screen:
    def __init__(self):
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        self.normal_mode = NormalMode(self)
        self.insert_mode = InsertMode(self)
        self.command_mode = CommandMode(self)
        self.mode = self.normal_mode
        self.input_handler = InputHandler(self)
        self.keymap = KeyMapManager(self)
        self.filename = 'untitled.txt'
        self.running = True

    def run(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1)
        while self.running:
            self.draw()
            raw = stdscr.getch()
            self.input_handler.handle(raw)

    def draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        for idx, line in enumerate(self.buffer.lines[:h-1]):
            self.stdscr.addstr(idx, 0, line)
        
        # Status line
        if isinstance(self.mode, self.command_mode.__class__):
            # Command mode: show command buffer
            status = f":{self.mode.cmd_buf}"
        else:
            # Normal/Insert mode: show status
            status = f"--{self.mode.__class__.__name__.upper()}-- {self.filename} {self.cursor.row+1}:{self.cursor.col+1}"
        
        self.stdscr.addstr(h-1, 0, status[:w-1], curses.A_REVERSE)
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()

    def set_message(self, message: str):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(h-1, 0, message[:w-1], curses.A_BOLD)
        self.stdscr.refresh()
        self.stdscr.getch()

    def set_mode(self, mode_name: str):
        """モードを切り替える"""
        if mode_name == 'normal':
            self.mode = self.normal_mode
        elif mode_name == 'insert':
            self.mode = self.insert_mode
        elif mode_name == 'command':
            self.mode = self.command_mode

    def quit(self):
        """エディタを終了"""
        self.running = False

    def save(self):
        """ファイルを保存"""
        try:
            with open(self.filename, 'w') as f:
                for line in self.buffer.lines:
                    f.write(line + '\n')
            self.set_message(f"Saved: {self.filename}")
        except Exception as e:
            self.set_message(f"Error saving: {e}")
