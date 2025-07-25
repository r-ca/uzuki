"""
File Service

Handles file operations including loading, saving, encoding detection,
and file browser functionality.
"""

import os
from typing import Optional, Dict, Any, List
from uzuki.interfaces import IFileService
from uzuki.core.file_manager import FileManager
from uzuki.core.file_selector import FileSelector, FileBrowser
from uzuki.utils.debug import get_debug_logger

class FileService(IFileService):
    """ファイル操作のビジネスロジックを実装するサービス"""
    
    def __init__(self, container):
        self.container = container
        self.logger = get_debug_logger()
        
        # ファイル管理コンポーネント
        self.file_manager = FileManager()
        self.file_selector = FileSelector()
        self.file_browser = FileBrowser(self.file_selector)
        
        # 状態
        self.current_file: Optional[str] = None
        self.current_directory: Optional[str] = None
    
    def load_file(self, filepath: str) -> bool:
        """ファイルを読み込み"""
        try:
            success = self.file_manager.load_file(filepath)
            if success:
                self.current_file = filepath
                self.current_directory = os.path.dirname(filepath)
                self.logger.info(f"File loaded: {filepath}")
            else:
                self.logger.error(f"Failed to load file: {filepath}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"FileService.load_file({filepath})")
            return False
    
    def save_file(self, filepath: Optional[str] = None) -> bool:
        """ファイルを保存"""
        try:
            target_path = filepath or self.current_file
            if not target_path:
                self.logger.error("No file path specified for saving")
                return False
            
            success = self.file_manager.save_file(target_path)
            if success:
                self.current_file = target_path
                self.current_directory = os.path.dirname(target_path)
                self.logger.info(f"File saved: {target_path}")
            else:
                self.logger.error(f"Failed to save file: {target_path}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"FileService.save_file({filepath})")
            return False
    
    def set_encoding(self, encoding: str) -> bool:
        """エンコーディングを設定"""
        try:
            self.file_manager.encoding = encoding
            self.logger.info(f"Encoding set to: {encoding}")
            return True
        except Exception as e:
            self.logger.log_error(e, f"FileService.set_encoding({encoding})")
            return False
    
    def get_file_info(self) -> Dict[str, Any]:
        """ファイル情報を取得"""
        info = {
            'filename': self.current_file,
            'directory': self.current_directory,
            'encoding': self.file_manager.encoding,
            'modified': self.file_manager.is_modified(),
            'size': 0,
            'lines': 0
        }
        
        if self.current_file and os.path.exists(self.current_file):
            try:
                stat = os.stat(self.current_file)
                info['size'] = stat.st_size
                info['lines'] = len(self.file_manager.lines)
            except Exception as e:
                self.logger.log_error(e, "FileService.get_file_info")
        
        return info
    
    def is_modified(self) -> bool:
        """ファイルが変更されているかチェック"""
        return self.file_manager.is_modified()
    
    def mark_modified(self):
        """ファイルを変更済みとしてマーク"""
        self.file_manager.mark_modified()
        self.logger.debug("File marked as modified")
    
    def get_buffer_content(self) -> List[str]:
        """バッファの内容を取得"""
        return self.file_manager.lines
    
    def set_buffer_content(self, lines: List[str]):
        """バッファの内容を設定"""
        self.file_manager.lines = lines
        self.mark_modified()
        self.logger.debug("Buffer content updated")
    
    def open_file_browser(self, directory: Optional[str] = None) -> bool:
        """ファイルブラウザーを開く"""
        try:
            target_dir = directory or self.current_directory or os.getcwd()
            self.file_browser.set_directory(target_dir)
            self.logger.info(f"File browser opened in: {target_dir}")
            return True
        except Exception as e:
            self.logger.log_error(e, f"FileService.open_file_browser({directory})")
            return False
    
    def get_file_browser_content(self) -> List[Dict[str, Any]]:
        """ファイルブラウザーの内容を取得"""
        return self.file_browser.get_items()
    
    def get_file_browser_selection(self) -> Optional[str]:
        """ファイルブラウザーの選択項目を取得"""
        return self.file_browser.get_selected_item()
    
    def navigate_file_browser(self, direction: int):
        """ファイルブラウザーでナビゲート"""
        self.file_browser.navigate(direction)
    
    def resolve_path(self, path: str) -> str:
        """パスを解決"""
        return self.file_selector.resolve_path(path)
    
    def list_directory(self, directory: str) -> List[Dict[str, Any]]:
        """ディレクトリの内容をリスト"""
        return self.file_selector.list_directory(directory) 