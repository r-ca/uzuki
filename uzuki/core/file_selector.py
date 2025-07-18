import os
import glob
from typing import List, Optional, Tuple
from pathlib import Path

class FileSelector:
    """ファイル選択機能"""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.file_patterns = ['*', '*.txt', '*.py', '*.js', '*.html', '*.css', '*.md']
        self.hidden_files = False
        self.sort_by = 'name'  # 'name', 'modified', 'size'
        self.sort_reverse = False
    
    def get_files_in_directory(self, directory: Optional[str] = None, 
                              pattern: Optional[str] = None) -> List[Tuple[str, str, bool]]:
        """ディレクトリ内のファイル一覧を取得
        
        Returns:
            List of (name, full_path, is_directory) tuples
        """
        target_dir = directory or self.current_dir
        
        if not os.path.exists(target_dir):
            return []
        
        files = []
        
        try:
            for item in os.listdir(target_dir):
                if not self.hidden_files and item.startswith('.'):
                    continue
                
                full_path = os.path.join(target_dir, item)
                is_dir = os.path.isdir(full_path)
                
                # パターンフィルタリング
                if pattern and not is_dir:
                    if not glob.fnmatch.fnmatch(item, pattern):
                        continue
                
                files.append((item, full_path, is_dir))
        except PermissionError:
            return []
        
        # ソート
        if self.sort_by == 'name':
            files.sort(key=lambda x: x[0].lower(), reverse=self.sort_reverse)
        elif self.sort_by == 'modified':
            files.sort(key=lambda x: os.path.getmtime(x[1]), reverse=self.sort_reverse)
        elif self.sort_by == 'size':
            files.sort(key=lambda x: os.path.getsize(x[1]) if not x[2] else 0, reverse=self.sort_reverse)
        
        # ディレクトリを先に表示
        dirs = [f for f in files if f[2]]
        regular_files = [f for f in files if not f[2]]
        
        return dirs + regular_files
    
    def find_files_by_pattern(self, pattern: str, directory: Optional[str] = None) -> List[str]:
        """パターンにマッチするファイルを検索"""
        target_dir = directory or self.current_dir
        
        if not os.path.exists(target_dir):
            return []
        
        matches = []
        for root, dirs, files in os.walk(target_dir):
            # 隠しディレクトリをスキップ
            dirs[:] = [d for d in dirs if not d.startswith('.') or self.hidden_files]
            
            for file in files:
                if glob.fnmatch.fnmatch(file, pattern):
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        
        return matches
    
    def get_file_info(self, filepath: str) -> Optional[dict]:
        """ファイル情報を取得"""
        if not os.path.exists(filepath):
            return None
        
        try:
            stat = os.stat(filepath)
            return {
                'name': os.path.basename(filepath),
                'path': filepath,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'is_directory': os.path.isdir(filepath),
                'is_file': os.path.isfile(filepath),
                'readable': os.access(filepath, os.R_OK),
                'writable': os.access(filepath, os.W_OK),
            }
        except OSError:
            return None
    
    def change_directory(self, directory: str) -> bool:
        """ディレクトリを変更"""
        if os.path.exists(directory) and os.path.isdir(directory):
            self.current_dir = os.path.abspath(directory)
            return True
        return False
    
    def get_current_directory(self) -> str:
        """現在のディレクトリを取得"""
        return self.current_dir
    
    def get_parent_directory(self) -> str:
        """親ディレクトリを取得"""
        return os.path.dirname(self.current_dir)
    
    def is_valid_file(self, filepath: str) -> bool:
        """ファイルが有効かチェック"""
        return os.path.isfile(filepath) and os.access(filepath, os.R_OK)
    
    def is_valid_directory(self, directory: str) -> bool:
        """ディレクトリが有効かチェック"""
        return os.path.isdir(directory) and os.access(directory, os.R_OK)
    
    def resolve_path(self, path: str) -> str:
        """パスを解決（相対パスを絶対パスに変換）"""
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(self.current_dir, path))
    
    def get_common_file_extensions(self) -> List[str]:
        """一般的なファイル拡張子を取得"""
        return [
            '.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml',
            '.c', '.cpp', '.h', '.java', '.rb', '.php', '.go', '.rs',
            '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd',
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.mp3', '.mp4', '.avi', '.mkv', '.mov',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.zip', '.tar', '.gz', '.rar', '.7z'
        ]

class FileBrowser:
    """ファイルブラウザー（TUI用）"""
    
    def __init__(self, selector: FileSelector):
        self.selector = selector
        self.current_index = 0
        self.scroll_offset = 0
        self.filter_text = ""
        self.show_hidden = False
    
    def get_display_files(self, max_height: int) -> List[Tuple[str, str, bool, bool]]:
        """表示用ファイル一覧を取得
        
        Returns:
            List of (name, path, is_directory, is_selected) tuples
        """
        files = self.selector.get_files_in_directory()
        
        # フィルタリング
        if self.filter_text:
            files = [f for f in files if self.filter_text.lower() in f[0].lower()]
        
        # 隠しファイルフィルタリング
        if not self.show_hidden:
            files = [f for f in files if not f[0].startswith('.')]
        
        # スクロール範囲を調整
        if self.current_index >= len(files):
            self.current_index = max(0, len(files) - 1)
        
        if self.current_index < self.scroll_offset:
            self.scroll_offset = self.current_index
        elif self.current_index >= self.scroll_offset + max_height:
            self.scroll_offset = self.current_index - max_height + 1
        
        # 表示範囲のファイルを取得
        display_files = files[self.scroll_offset:self.scroll_offset + max_height]
        
        # 選択状態を追加
        result = []
        for i, (name, path, is_dir) in enumerate(display_files):
            is_selected = (self.scroll_offset + i) == self.current_index
            result.append((name, path, is_dir, is_selected))
        
        return result
    
    def move_up(self):
        """上に移動"""
        if self.current_index > 0:
            self.current_index -= 1
    
    def move_down(self):
        """下に移動"""
        files = self.selector.get_files_in_directory()
        if self.filter_text:
            files = [f for f in files if self.filter_text.lower() in f[0].lower()]
        if not self.show_hidden:
            files = [f for f in files if not f[0].startswith('.')]
        
        if self.current_index < len(files) - 1:
            self.current_index += 1
    
    def get_selected_file(self) -> Optional[str]:
        """選択されたファイルのパスを取得"""
        files = self.selector.get_files_in_directory()
        if self.filter_text:
            files = [f for f in files if self.filter_text.lower() in f[0].lower()]
        if not self.show_hidden:
            files = [f for f in files if not f[0].startswith('.')]
        
        if 0 <= self.current_index < len(files):
            return files[self.current_index][1]
        return None
    
    def set_filter(self, filter_text: str):
        """フィルタを設定"""
        self.filter_text = filter_text
        self.current_index = 0
        self.scroll_offset = 0
    
    def toggle_hidden_files(self):
        """隠しファイルの表示を切り替え"""
        self.show_hidden = not self.show_hidden
        self.current_index = 0
        self.scroll_offset = 0 