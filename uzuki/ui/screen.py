"""
Screen - Main screen management class

A clean, modular implementation using services and DI container to manage
different aspects of the editor functionality.
"""

import curses
import time
import sys
import os
from typing import Optional
from uzuki.container import ServiceContainer
from uzuki.controllers import (
    EditorController,
    FileController,
    ConfigController,
    NotificationController
)
from .ui_controller import UIController
from uzuki.ui.notification import NotificationLevel
from uzuki.ui.color_manager import color_manager
from uzuki.utils.debug import init_debug_logger, get_debug_logger

class Screen:
    """メインのスクリーン管理クラス"""
    
    def __init__(self, initial_file: Optional[str] = None, show_greeting: bool = True, config_file: Optional[str] = None):
        # デバッグロガーを初期化
        self.debug_logger = init_debug_logger()
        self.debug_logger.info("Screen initialized")
        
        # サービスコンテナを初期化
        self.container = ServiceContainer()
        
        # コントローラーの初期化（依存関係の順序で）
        self.editor = EditorController(self)
        self.notifications = NotificationController(self)
        self.file = FileController(self)
        self.ui = UIController(self)
        self.config = ConfigController(self, config_file)
        
        # 状態
        self.running = True
        self.show_greeting = show_greeting
        
        # 設定を適用
        self.config.apply_config()
        
        # 初期ファイルの読み込み
        if initial_file:
            self.file.load_initial_file(initial_file)
        
        self.debug_logger.info("Screen initialization completed")

    def run(self, stdscr):
        """メインループを実行"""
        try:
            self.stdscr = stdscr
            
            # curses初期設定
            curses.noecho()  # キー入力を表示しない
            curses.cbreak()  # 入力バッファを使用しない
            
            # カラーマネージャーを初期化
            color_manager.initialize()
            
            # システムカーソルを有効化
            curses.curs_set(1)
            
            # 通知システムの色を設定
            self.notifications.set_colors({
                NotificationLevel.INFO: curses.A_NORMAL,
                NotificationLevel.SUCCESS: color_manager.get_success_style(),
                NotificationLevel.WARNING: color_manager.get_warning_style(),
                NotificationLevel.ERROR: color_manager.get_error_style(),
            })
            
            # Greeting表示
            if self.show_greeting:
                self._show_greeting()
            
            self.debug_logger.info("Main loop started")
            
            while self.running:
                # 画面を描画（常に描画）
                self.ui.draw(self.stdscr)
                
                # カーソル位置を設定
                self._set_cursor_position()
                
                # キー入力を待つ
                raw = self.stdscr.getch()
                self._handle_key(raw)
                
        except Exception as e:
            self.debug_logger.log_error(e, "Screen.run")
            raise
        finally:
            # クリーンアップ
            color_manager.cleanup()
            self.container.shutdown()

    def _handle_key(self, raw_code: int):
        """キー入力を処理"""
        try:
            self.editor.handle_key(raw_code)
            
            # エディタの状態に応じて画面を更新
            if self.editor.needs_redraw:
                self.ui.draw(self.stdscr)
                self.editor.needs_redraw = False
        except Exception as e:
            self.debug_logger.log_error(e, "Screen._handle_key")

    def _show_greeting(self):
        """Greetingを表示"""
        # デフォルトのコンテンツを設定
        self.ui.set_greeting_content([
            "Welcome to Uzuki",
            "A Vim-like text editor in Python",
            "",
            "Press any key to continue..."
        ])
        
        # Greetingを表示
        self.ui.display_greeting(self.stdscr)
        
        # キー入力を待つ
        self.stdscr.getch()
        
        # Greeting表示を無効化
        self.ui.set_show_greeting(False)
        
        self.debug_logger.info("Greeting displayed and disabled")
    
    def _set_cursor_position(self):
        """カーソル位置を設定"""
        try:
            # 現在のモードに応じてカーソル位置を設定
            if self.editor.mode.mode_name == 'command':
                # コマンドモードの場合はステータスラインのコマンド入力位置に
                height, width = self.stdscr.getmaxyx()
                y = height - 1  # ステータスラインの行
                
                # ステータスラインの構築ロジックを直接使用してコマンド位置を計算
                # モード、ファイル情報、位置情報、行数情報の長さを計算
                mode_text = f"--{self.editor.mode.mode_name.upper()}--"
                mode_width = 15
                
                # ファイル情報
                file_info = self.screen.file.get_file_info()
                filename_width = 0
                encoding_width = 0
                if file_info.get('filename'):
                    filename_width = 30
                if file_info.get('encoding'):
                    encoding_width = 12
                
                # 位置情報
                cursor_row = self.editor.cursor.row
                cursor_col = self.editor.cursor.col
                position_text = f"{cursor_row+1}:{cursor_col+1}"
                position_width = 10
                
                # 行数情報
                total_lines = len(self.editor.buffer.lines)
                line_count_text = f"L{total_lines}"
                line_count_width = 8
                
                # セパレータ
                separator = " | "
                separator_width = len(separator)
                
                # コマンドセグメントの開始位置を計算
                # 左から: モード + セパレータ + ファイル名 + セパレータ + エンコーディング + セパレータ + 位置 + セパレータ + 行数 + セパレータ
                cmd_start = mode_width + separator_width
                if filename_width > 0:
                    cmd_start += filename_width + separator_width
                if encoding_width > 0:
                    cmd_start += encoding_width + separator_width
                cmd_start += position_width + separator_width + line_count_width + separator_width
                
                # コマンドテキストの長さ
                cmd_text = f":{self.editor.mode.cmd_buf}"
                x = cmd_start + len(cmd_text)
                
                # 画面幅を超えないように調整
                if x >= width:
                    x = width - 1
                
                self.stdscr.move(y, x)
            else:
                # 通常のエディタモードの場合はカーソル位置に
                cursor_row = self.editor.cursor.row
                cursor_col = self.editor.cursor.col
                height, width = self.stdscr.getmaxyx()
                
                # エディタ表示からカーソルの画面座標を取得
                screen_row, screen_col = self.ui.editor_display.get_cursor_screen_pos(
                    cursor_row, cursor_col, 0, 0)
                
                # カーソルが画面内にある場合のみ設定
                if 0 <= screen_row < height - 1 and 0 <= screen_col < width:
                    self.stdscr.move(screen_row, screen_col)
                else:
                    # カーソルが画面外の場合は安全な位置に移動
                    safe_row = min(max(0, screen_row), height - 2)
                    safe_col = min(max(0, screen_col), width - 1)
                    self.stdscr.move(safe_row, safe_col)
        except Exception as e:
            self.debug_logger.log_error(e, "Screen._set_cursor_position")
    
    # サービスアクセサー
    def get_editor_service(self):
        """エディタサービスを取得"""
        return self.container.get_editor_service()
    
    def get_file_service(self):
        """ファイルサービスを取得"""
        return self.container.get_file_service()
    
    def get_notification_service(self):
        """通知サービスを取得"""
        return self.container.get_notification_service()
    
    def get_config_service(self):
        """設定サービスを取得"""
        return self.container.get_config_service()
    
    # エディタ操作
    def set_mode(self, mode_name: str):
        """モードを切り替える"""
        self.editor.set_mode(mode_name)
    
    def quit(self):
        """エディタを終了"""
        self.editor.quit()
        self.running = False
    
    # ファイル操作
    def load_file(self, filepath: str):
        """ファイルを読み込み"""
        return self.file.load_file(filepath)
    
    def save_file(self, filepath: Optional[str] = None):
        """ファイルを保存"""
        return self.file.save_file(filepath)
    
    def set_encoding(self, encoding: str):
        """エンコーディングを設定"""
        return self.file.set_encoding(encoding)
    
    def open_file_browser(self, directory: Optional[str] = None):
        """ファイルブラウザーを開く"""
        return self.file.open_file_browser(directory)
    
    # 通知操作
    def notify(self, message: str, level=None, duration: float = 3.0, metadata=None):
        """通知を追加"""
        if level is None:
            level = NotificationLevel.INFO
        return self.notifications.add(message, level, duration, metadata)
    
    def notify_info(self, message: str, duration: float = 3.0):
        """情報通知を追加"""
        return self.notifications.add_info(message, duration)
    
    def notify_success(self, message: str, duration: float = 3.0):
        """成功通知を追加"""
        return self.notifications.add_success(message, duration)
    
    def notify_warning(self, message: str, duration: float = 4.0):
        """警告通知を追加"""
        return self.notifications.add_warning(message, duration)
    
    def notify_error(self, message: str, duration: float = 5.0):
        """エラー通知を追加"""
        return self.notifications.add_error(message, duration)
    
    def clear_notifications(self):
        """すべての通知をクリア"""
        self.notifications.clear()
    
    # 設定操作
    def get_config(self, section: str = None, key: str = None):
        """設定値を取得"""
        return self.config.get_config(section, key)
    
    def set_config(self, section: str, key: str, value):
        """設定値を設定"""
        return self.config.set_config(section, key, value)
    
    def reset_config(self, section: str = None):
        """設定をリセット"""
        return self.config.reset_config(section)
    
    def import_config(self, filepath: str):
        """設定ファイルをインポート"""
        return self.config.import_config(filepath)
    
    def print_config(self, section: str = None):
        """設定を出力"""
        return self.config.print_config(section)
