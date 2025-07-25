"""
Editor Controller

Manages editor-specific functionality including modes, key handling,
and core editor operations.
"""

from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.modes.normal_mode import NormalMode
from uzuki.modes.insert_mode import InsertMode
from uzuki.commands.command_mode import CommandMode
from uzuki.modes.file_browser_mode import FileBrowserMode
from uzuki.input.handler import InputHandler
from uzuki.input.sequence_manager import KeySequenceManager
from uzuki.keymaps.manager import KeyMapManager

class EditorController:
    """エディタのコア機能を制御するコントローラー"""
    
    def __init__(self, screen):
        self.screen = screen
        
        # コアコンポーネント
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        
        # 変更通知コールバックを設定
        self.buffer.set_change_callback(self._on_buffer_change)
        self.cursor.set_move_callback(self._on_cursor_move)
        
        # モード（FileBrowserModeは遅延初期化）
        self.normal_mode = NormalMode(screen)
        self.insert_mode = InsertMode(screen)
        self.command_mode = CommandMode(screen)
        self._file_browser_mode = None  # 遅延初期化
        self.mode = self.normal_mode
        
        # 入力処理
        self.input_handler = InputHandler(screen)
        self.keymap = KeyMapManager(screen)
        self.sequence_manager = KeySequenceManager()
        
        # 状態
        self.running = True
        self.needs_redraw = True
    
    @property
    def file_browser_mode(self):
        """FileBrowserModeを遅延初期化"""
        if self._file_browser_mode is None:
            self._file_browser_mode = FileBrowserMode(self.screen)
        return self._file_browser_mode
    
    def handle_key(self, raw_code: int):
        """キー入力を処理"""
        key_info = self.input_handler.create_key_info(raw_code)
        
        # キーシーケンスを管理
        sequence = self.sequence_manager.add_key(key_info.key_name)
        
        # アクションを検索
        action = self.keymap.get_action(self.mode.mode_name, sequence)
        
        if action:
            # アクションが見つかったら即座に実行
            action()
            self.sequence_manager.clear()
            self.needs_redraw = True
        elif self.keymap.has_potential_mapping(self.mode.mode_name, sequence):
            # 潜在的なマッピングがある場合は待つ
            pass
        else:
            # マッピングがない場合は即座にデフォルト処理
            if len(sequence) == 1:
                self.mode.handle_default(key_info)
                self.needs_redraw = True
            self.sequence_manager.clear()
    
    def set_mode(self, mode_name: str):
        """モードを切り替える"""
        if mode_name == 'normal':
            self.mode = self.normal_mode
        elif mode_name == 'insert':
            self.mode = self.insert_mode
        elif mode_name == 'command':
            self.mode = self.command_mode
        elif mode_name == 'file_browser':
            self.mode = self.file_browser_mode
        
        # モード切り替え時にシーケンスをクリア
        self.sequence_manager.clear()
        self.needs_redraw = True
    
    def quit(self):
        """エディタを終了"""
        self.running = False
    
    def load_keymap_config(self, config: dict):
        """キーマップ設定を読み込み"""
        self.keymap.load_from_config(config)
    
    # コールバック
    def _on_buffer_change(self):
        """バッファ変更時の処理"""
        self.screen.file.mark_modified()
        self.needs_redraw = True
    
    def _on_cursor_move(self):
        """カーソル移動時の処理"""
        # 描画フラグを設定
        self.needs_redraw = True 