"""
Debug utilities for CLI application

Provides logging and debugging capabilities for the terminal-based editor.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

class DebugLogger:
    """CLIアプリケーション用のデバッグロガー"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or f"uzuki_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # ロガーの設定
        self.logger = logging.getLogger('uzuki')
        self.logger.setLevel(logging.DEBUG)
        
        # ファイルハンドラー
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """デバッグメッセージを記録"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報メッセージを記録"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告メッセージを記録"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """エラーメッセージを記録"""
        self.logger.error(message)
    
    def log_key_event(self, raw_code: int, key_name: str, mode: str, action: Optional[str] = None):
        """キーイベントを記録"""
        self.debug(f"KEY: raw={raw_code}, name='{key_name}', mode='{mode}', action='{action}'")
    
    def log_screen_event(self, event: str, details: str = ""):
        """画面イベントを記録"""
        self.debug(f"SCREEN: {event} - {details}")
    
    def log_error(self, error: Exception, context: str = ""):
        """エラーを記録"""
        self.error(f"ERROR in {context}: {type(error).__name__}: {error}")
        import traceback
        self.error(f"Traceback: {traceback.format_exc()}")

# グローバルインスタンス
debug_logger = None

def init_debug_logger(log_file: Optional[str] = None):
    """デバッグロガーを初期化"""
    global debug_logger
    debug_logger = DebugLogger(log_file)
    return debug_logger

def get_debug_logger() -> DebugLogger:
    """デバッグロガーを取得"""
    global debug_logger
    if debug_logger is None:
        debug_logger = DebugLogger()
    return debug_logger 