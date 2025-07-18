import os
import codecs
from typing import List, Optional, Tuple
from pathlib import Path

class FileManager:
    """ファイル操作と文字エンコーディング管理"""
    
    # 一般的な文字エンコーディング
    COMMON_ENCODINGS = [
        'utf-8',
        'utf-8-sig',  # BOM付きUTF-8
        'shift_jis',
        'cp932',
        'euc-jp',
        'iso-2022-jp',
        'ascii',
        'latin-1',
        'cp1252',
    ]
    
    def __init__(self):
        self.filename: Optional[str] = None
        self.encoding: str = 'utf-8'
        self.has_bom: bool = False
        self.line_ending: str = '\n'  # 改行コード
        self.is_modified: bool = False
        
    def detect_encoding(self, filepath: str) -> Tuple[str, bool]:
        """ファイルの文字エンコーディングを検出"""
        try:
            # まずBOMをチェック
            with open(filepath, 'rb') as f:
                raw = f.read(4)
                
            if raw.startswith(codecs.BOM_UTF8):
                return 'utf-8-sig', True
            elif raw.startswith(codecs.BOM_UTF16_LE):
                return 'utf-16-le', True
            elif raw.startswith(codecs.BOM_UTF16_BE):
                return 'utf-16-be', True
            elif raw.startswith(codecs.BOM_UTF32_LE):
                return 'utf-32-le', True
            elif raw.startswith(codecs.BOM_UTF32_BE):
                return 'utf-32-be', True
            
            # BOMがない場合、一般的なエンコーディングを試す
            for encoding in self.COMMON_ENCODINGS:
                try:
                    with codecs.open(filepath, 'r', encoding=encoding) as f:
                        f.read()
                    return encoding, False
                except (UnicodeDecodeError, UnicodeError):
                    continue
                    
            # デフォルトはUTF-8
            return 'utf-8', False
            
        except Exception:
            return 'utf-8', False
    
    def detect_line_ending(self, content: str) -> str:
        """改行コードを検出"""
        if '\r\n' in content:
            return '\r\n'
        elif '\r' in content:
            return '\r'
        else:
            return '\n'
    
    def load_file(self, filepath: str) -> List[str]:
        """ファイルを読み込み"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # エンコーディングを検出
        self.encoding, self.has_bom = self.detect_encoding(filepath)
        
        try:
            with codecs.open(filepath, 'r', encoding=self.encoding) as f:
                content = f.read()
            
            # 改行コードを検出
            self.line_ending = self.detect_line_ending(content)
            
            # 行に分割（改行コードを除去）
            lines = content.splitlines()
            if not lines:
                lines = ['']
            
            self.filename = filepath
            self.is_modified = False
            
            return lines
            
        except UnicodeDecodeError as e:
            raise UnicodeError(f"Failed to decode file with {self.encoding}: {e}")
        except Exception as e:
            raise IOError(f"Failed to read file: {e}")
    
    def save_file(self, filepath: str, lines: List[str], encoding: Optional[str] = None) -> None:
        """ファイルを保存"""
        save_encoding = encoding or self.encoding
        
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with codecs.open(filepath, 'w', encoding=save_encoding) as f:
                for i, line in enumerate(lines):
                    f.write(line)
                    if i < len(lines) - 1:  # 最後の行以外は改行を追加
                        f.write(self.line_ending)
            
            self.filename = filepath
            self.encoding = save_encoding
            self.is_modified = False
            
        except Exception as e:
            raise IOError(f"Failed to save file: {e}")
    
    def get_file_info(self) -> dict:
        """ファイル情報を取得"""
        if not self.filename:
            return {
                'name': 'untitled',
                'path': None,
                'encoding': self.encoding,
                'modified': self.is_modified,
                'size': 0,
                'line_ending': self.line_ending
            }
        
        try:
            stat = os.stat(self.filename)
            return {
                'name': os.path.basename(self.filename),
                'path': self.filename,
                'encoding': self.encoding,
                'modified': self.is_modified,
                'size': stat.st_size,
                'line_ending': self.line_ending
            }
        except OSError:
            return {
                'name': os.path.basename(self.filename),
                'path': self.filename,
                'encoding': self.encoding,
                'modified': self.is_modified,
                'size': 0,
                'line_ending': self.line_ending
            }
    
    def set_encoding(self, encoding: str):
        """文字エンコーディングを設定"""
        if encoding in self.COMMON_ENCODINGS:
            self.encoding = encoding
            self.is_modified = True
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")
    
    def get_available_encodings(self) -> List[str]:
        """利用可能な文字エンコーディングを取得"""
        return self.COMMON_ENCODINGS.copy()
    
    def mark_modified(self):
        """ファイルが変更されたことをマーク"""
        self.is_modified = True
    
    def is_file_loaded(self) -> bool:
        """ファイルが読み込まれているかチェック"""
        return self.filename is not None 