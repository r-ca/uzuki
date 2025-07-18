import curses
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.input.handler import InputHandler
from uzuki.input.sequence_manager import KeySequenceManager
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
        
        # 変更通知コールバックを設定
        self.buffer.set_change_callback(self._on_buffer_change)
        self.cursor.set_move_callback(self._on_cursor_move)
        
        # モード
        self.normal_mode = NormalMode(self)
        self.insert_mode = InsertMode(self)
        self.command_mode = CommandMode(self)
        self.mode = self.normal_mode
        
        # 入力処理
        self.input_handler = InputHandler(self)
        self.keymap = KeyMapManager(self)
        self.sequence_manager = KeySequenceManager()
        
        # 状態
        self.filename = 'untitled.txt'
        self.running = True
        self.needs_redraw = True  # 再描画が必要かどうかのフラグ

    def run(self, stdscr):
        """メインループ"""
        self.stdscr = stdscr
        curses.curs_set(1)
        
        while self.running:
            # 画面を描画
            self.draw()
            
            # キー入力を待つ
            raw = stdscr.getch()
            self._handle_key(raw)

    def _handle_key(self, raw_code: int):
        """キー入力を処理（シーケンス対応）"""
        key_info = self.input_handler.create_key_info(raw_code)
        
        # キーシーケンスを管理
        sequence = self.sequence_manager.add_key(key_info.key_name)
        
        # アクションを検索
        action = self.keymap.get_action(self.mode.mode_name, sequence)
        
        if action:
            # アクションが見つかったら即座に実行
            action()
            self.sequence_manager.clear()
            # アクション実行後に画面を再描画
            self.draw()
        elif self.keymap.has_potential_mapping(self.mode.mode_name, sequence):
            # 潜在的なマッピングがある場合は待つ（何もしない）
            # デバッグ用: 待機中であることを表示
            pass
        else:
            # マッピングがない場合は即座にデフォルト処理
            if len(sequence) == 1:
                self.mode.handle_default(key_info)
                # デフォルト処理後に画面を再描画
                self.draw()
            self.sequence_manager.clear()

    def draw(self):
        """画面を描画"""
        if not self.needs_redraw:
            return
            
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
            sequence = self.sequence_manager.get_sequence()
            sequence_display = f" [{sequence}]" if sequence else ""
            status = f"--{self.mode.__class__.__name__.upper()}-- {self.filename} {self.cursor.row+1}:{self.cursor.col+1}{sequence_display}"
        
        self.stdscr.addstr(h-1, 0, status[:w-1], curses.A_REVERSE)
        self.stdscr.move(self.cursor.row, self.cursor.col)
        self.stdscr.refresh()
        self.needs_redraw = False

    def force_redraw(self):
        """強制的に画面を再描画"""
        self.needs_redraw = True
        self.draw()

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
        
        # モード切り替え時にシーケンスをクリア
        self.sequence_manager.clear()
        # モード切り替え後に画面を再描画
        self.draw()

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

    def _on_buffer_change(self):
        """バッファ変更時の処理"""
        self.needs_redraw = True

    def _on_cursor_move(self):
        """カーソル移動時の処理"""
        self.needs_redraw = True
