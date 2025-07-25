"""
Editor Service

Core editor business logic including modes, key handling, and buffer operations.
"""

from typing import Optional, Callable
from uzuki.interfaces import IEditorService
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.core.viewport import ViewportManager
from uzuki.modes.normal_mode import NormalMode
from uzuki.modes.insert_mode import InsertMode
from uzuki.commands.command_mode import CommandMode
from uzuki.modes.file_browser_mode import FileBrowserMode
from uzuki.input.handler import InputHandler
from uzuki.input.sequence_manager import KeySequenceManager
from uzuki.keymaps.manager import KeyMapManager
from uzuki.utils.debug import get_debug_logger
from uzuki.ui import cursor_display

class EditorService(IEditorService):
    """エディタのビジネスロジックを実装するサービス"""
    
    def __init__(self, container):
        self.container = container
        self.logger = get_debug_logger()
        
        # コアコンポーネント
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        self.viewport = ViewportManager()
        
        # 変更通知コールバックを設定
        self.buffer.set_change_callback(self._on_buffer_change)
        self.cursor.set_move_callback(self._on_cursor_move)
        
        # モード（FileBrowserModeは遅延初期化）
        self._normal_mode = None
        self._insert_mode = None
        self._command_mode = None
        self._file_browser_mode = None
        self._current_mode = None
        
        # 入力処理
        self.input_handler = InputHandler(self)
        self.keymap = KeyMapManager(self)
        self.sequence_manager = KeySequenceManager()
        
        # 状態
        self.running = True
        self.needs_redraw = True
    
    @property
    def normal_mode(self):
        """NormalModeを遅延初期化"""
        if self._normal_mode is None:
            self._normal_mode = NormalMode(self)
        return self._normal_mode
    
    @property
    def insert_mode(self):
        """InsertModeを遅延初期化"""
        if self._insert_mode is None:
            self._insert_mode = InsertMode(self)
        return self._insert_mode
    
    @property
    def command_mode(self):
        """CommandModeを遅延初期化"""
        if self._command_mode is None:
            self._command_mode = CommandMode(self)
        return self._command_mode
    
    @property
    def file_browser_mode(self):
        """FileBrowserModeを遅延初期化"""
        if self._file_browser_mode is None:
            self._file_browser_mode = FileBrowserMode(self)
        return self._file_browser_mode
    
    @property
    def current_mode(self):
        """現在のモードを取得"""
        if self._current_mode is None:
            self._current_mode = self.normal_mode
        return self._current_mode
    
    def handle_key(self, raw_code: int):
        """キー入力を処理"""
        key_info = self.input_handler.create_key_info(raw_code)
        
        # デバッグログ
        self.logger.log_key_event(raw_code, key_info.key_name, self.current_mode.mode_name)
        
        # キーシーケンスを管理
        sequence = self.sequence_manager.add_key(key_info.key_name)
        
        # アクションを検索
        action = self.keymap.get_action(self.current_mode.mode_name, sequence)
        
        if action:
            # アクションが見つかったら即座に実行
            action()
            self.sequence_manager.clear()
            self.needs_redraw = True
        elif self.keymap.has_potential_mapping(self.current_mode.mode_name, sequence):
            # 潜在的なマッピングがある場合は待つ
            pass
        else:
            # マッピングがない場合は即座にデフォルト処理
            if len(sequence) == 1:
                self.current_mode.handle_default(key_info)
                self.needs_redraw = True
            self.sequence_manager.clear()
    
    def set_mode(self, mode: str):
        """モードを設定"""
        if mode == 'normal':
            self._current_mode = self.normal_mode
        elif mode == 'insert':
            self._current_mode = self.insert_mode
        elif mode == 'command':
            self._current_mode = self.command_mode
        elif mode == 'file_browser':
            self._current_mode = self.file_browser_mode
        
        # モード切り替え時にシーケンスをクリア
        self.sequence_manager.clear()
        self.needs_redraw = True
        
        # カーソル表示も更新
        cursor_display.set_mode(mode)
        self.logger.debug(f"Mode changed to: {mode}")
    
    def get_current_mode(self) -> str:
        """現在のモード名を取得"""
        return self.current_mode.mode_name
    
    def quit(self):
        """エディタを終了"""
        self.running = False
        self.logger.info("Editor quit requested")
    
    def _on_buffer_change(self):
        """バッファ変更時のコールバック"""
        self.needs_redraw = True
        self.logger.debug("Buffer changed")
    
    def _on_cursor_move(self):
        """カーソル移動時のコールバック"""
        # ビューポートをカーソルに追従
        self.viewport.scroll_to_cursor(self.cursor.col, self.cursor.row)
        self.needs_redraw = True
        self.logger.debug(f"Cursor moved to ({self.cursor.row}, {self.cursor.col})")
    
    def get_buffer_content(self) -> list:
        """バッファの内容を取得"""
        return self.buffer.lines
    
    def get_cursor_position(self) -> tuple:
        """カーソル位置を取得"""
        return (self.cursor.row, self.cursor.col)
    
    def get_viewport_info(self) -> dict:
        """ビューポート情報を取得"""
        return self.viewport.get_scroll_info() 