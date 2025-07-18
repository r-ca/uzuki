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
    """メインのスクリーン管理クラス"""
    def __init__(self):
        # コアコンポーネント
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        
        # モード
        self.normal_mode = NormalMode(self)
        self.insert_mode = InsertMode(self)
        self.command_mode = CommandMode(self)
        self.mode = self.normal_mode
        
        # 入力処理
        self.input_handler = InputHandler(self)
        self.keymap = KeyMapManager(self)
        
        # 状態
        self.filename = 'untitled.txt'
        self.running = True

    def run(self, stdscr):
        """メインループ"""
        self.stdscr = stdscr
        curses.curs_set(1)
        
        while self.running:
            self.draw()
            raw = stdscr.getch()
            self.input_handler.handle(raw)

    def draw(self):
        """画面を描画"""
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        
        # バッファ内容を描画
        for idx, line in enumerate(self.buffer.lines[:h-1]):
            self.stdscr.addstr(idx, 0, line)
        
        # ステータスライン
        if isinstance(self.mode, self.command_mode.__class__):
            # Command mode: コマンドバッファを表示
            status = f":{self.mode.cmd_buf}"
        else:
            # Normal/Insert mode: ステータスを表示
            status = f"--{self.mode.__class__.__name__.upper()}-- {self.filename} {self.cursor.row+1}:{self.cursor.col+1}"
        
        self.stdscr.addstr(h-1, 0, status[:w-1], curses.A_REVERSE)
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()

    def set_message(self, message: str):
        """メッセージを表示"""
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
