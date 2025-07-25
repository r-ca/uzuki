"""
File Controller

Manages file operations including loading, saving, encoding detection,
and file browser functionality.
"""

import os
from uzuki.core.file_manager import FileManager
from uzuki.core.file_selector import FileSelector
from uzuki.ui.notification import NotificationLevel

class FileController:
    """ファイル操作を制御するコントローラー"""
    
    def __init__(self, screen):
        self.screen = screen
        self.file_manager = FileManager()
        self.file_selector = FileSelector()
    
    def load_file(self, filepath: str) -> bool:
        """ファイルを読み込み"""
        try:
            lines = self.file_manager.load_file(filepath)
            self.screen.editor.buffer.lines = lines
            self.screen.editor.cursor.row = 0
            self.screen.editor.cursor.col = 0
            self.screen.notifications.add(f"Loaded: {filepath}", NotificationLevel.SUCCESS)
            return True
        except Exception as e:
            self.screen.notifications.add(f"Failed to load file: {e}", NotificationLevel.ERROR, duration=5.0)
            return False
    
    def save_file(self, filepath: str = None) -> bool:
        """ファイルを保存"""
        try:
            save_path = filepath or self.file_manager.filename
            if not save_path:
                self.screen.notifications.add("No file to save", NotificationLevel.WARNING)
                return False
            
            self.file_manager.save_file(save_path, self.screen.editor.buffer.lines)
            self.screen.notifications.add(f"Saved: {save_path}", NotificationLevel.SUCCESS)
            return True
        except Exception as e:
            self.screen.notifications.add(f"Failed to save file: {e}", NotificationLevel.ERROR, duration=5.0)
            return False
    
    def set_encoding(self, encoding: str) -> bool:
        """文字エンコーディングを設定"""
        try:
            self.file_manager.set_encoding(encoding)
            self.screen.notifications.add(f"Encoding set to: {encoding}", NotificationLevel.INFO)
            return True
        except ValueError as e:
            self.screen.notifications.add(str(e), NotificationLevel.ERROR)
            return False
    
    def load_initial_file(self, filepath: str):
        """初期ファイルを読み込み"""
        try:
            # パスを解決
            resolved_path = self.file_selector.resolve_path(filepath)
            
            if os.path.isfile(resolved_path):
                self.load_file(resolved_path)
            elif os.path.isdir(resolved_path):
                # ディレクトリの場合はファイルブラウザーを開く
                self.file_selector.change_directory(resolved_path)
                self.screen.editor.file_browser_mode.enter_browser('normal')
            else:
                # ファイルが存在しない場合は新規作成
                self.file_manager.filename = resolved_path
                self.screen.notifications.add(f"New file: {resolved_path}", NotificationLevel.INFO)
        except Exception as e:
            self.screen.notifications.add(f"Failed to load initial file: {e}", NotificationLevel.ERROR)
    
    def open_file_browser(self, directory: str = None):
        """ファイルブラウザーを開く"""
        if directory:
            self.file_selector.change_directory(directory)
        
        current_mode = self.screen.editor.mode.mode_name
        self.screen.editor.file_browser_mode.enter_browser(current_mode)
    
    def get_file_info(self) -> dict:
        """ファイル情報を取得"""
        return self.file_manager.get_file_info()
    
    def is_modified(self) -> bool:
        """ファイルが変更されているかチェック"""
        return self.file_manager.is_modified
    
    def mark_modified(self):
        """ファイルを変更済みとしてマーク"""
        self.file_manager.mark_modified()
    
    def get_current_directory(self) -> str:
        """現在のディレクトリを取得"""
        return self.file_selector.get_current_directory() 