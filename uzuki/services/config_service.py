"""
Config Service

Manages configuration system including loading, saving, and applying
user settings and keymaps.
"""

import os
import importlib.util
from typing import Optional, Dict, Any
from uzuki.interfaces import IConfigService
from uzuki.config.config_manager import ConfigManager
from uzuki.config.default_config import DEFAULT_CONFIG
from uzuki.utils.debug import get_debug_logger

class ConfigService(IConfigService):
    """設定システムのビジネスロジックを実装するサービス"""
    
    def __init__(self, container):
        self.container = container
        self.logger = get_debug_logger()
        
        # 設定管理コンポーネント
        self.config_manager = ConfigManager()
        
        # 設定ファイルパス
        self.config_file: Optional[str] = None
        self.config_loaded = False
    
    def load_config(self, config_file: Optional[str] = None) -> bool:
        """設定を読み込み"""
        try:
            self.config_file = config_file
            success = self.config_manager.load_config(config_file)
            
            if success:
                self.config_loaded = True
                self.logger.info(f"Config loaded: {config_file or 'default'}")
            else:
                self.logger.warning(f"Failed to load config: {config_file}")
            
            return success
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.load_config({config_file})")
            return False
    
    def get_config(self, section: str = None, key: str = None) -> Any:
        """設定値を取得"""
        try:
            return self.config_manager.get_config(section, key)
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.get_config({section}, {key})")
            return None
    
    def set_config(self, section: str, key: str, value: Any) -> bool:
        """設定値を設定"""
        try:
            success = self.config_manager.set_config(section, key, value)
            if success:
                self.logger.debug(f"Config set: {section}.{key} = {value}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.set_config({section}, {key}, {value})")
            return False
    
    def apply_config(self) -> bool:
        """設定を適用"""
        try:
            success = self.config_manager.apply_config()
            if success:
                self.logger.info("Config applied successfully")
            else:
                self.logger.warning("Failed to apply config")
            return success
        except Exception as e:
            self.logger.log_error(e, "ConfigService.apply_config")
            return False
    
    def reset_config(self, section: str = None) -> bool:
        """設定をリセット"""
        try:
            success = self.config_manager.reset_config(section)
            if success:
                self.logger.info(f"Config reset: {section or 'all'}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.reset_config({section})")
            return False
    
    def import_config(self, filepath: str) -> bool:
        """設定ファイルをインポート"""
        try:
            success = self.config_manager.import_config(filepath)
            if success:
                self.logger.info(f"Config imported: {filepath}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.import_config({filepath})")
            return False
    
    def export_config(self, filepath: str) -> bool:
        """設定をエクスポート"""
        try:
            success = self.config_manager.export_config(filepath)
            if success:
                self.logger.info(f"Config exported: {filepath}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.export_config({filepath})")
            return False
    
    def print_config(self, section: str = None) -> str:
        """設定を文字列として出力"""
        try:
            return self.config_manager.print_config(section)
        except Exception as e:
            self.logger.log_error(e, f"ConfigService.print_config({section})")
            return ""
    
    def get_keymap_manager(self):
        """キーマップマネージャーを取得"""
        return self.config_manager.keymap_manager
    
    def get_default_config(self) -> Dict[str, Any]:
        """デフォルト設定を取得"""
        return DEFAULT_CONFIG.copy()
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """設定の妥当性を検証"""
        try:
            # 基本的な検証
            required_sections = ['editor', 'display', 'keymaps']
            for section in required_sections:
                if section not in config:
                    self.logger.error(f"Missing required config section: {section}")
                    return False
            
            # エディタ設定の検証
            editor_config = config.get('editor', {})
            if 'tab_size' in editor_config:
                tab_size = editor_config['tab_size']
                if not isinstance(tab_size, int) or tab_size <= 0:
                    self.logger.error(f"Invalid tab_size: {tab_size}")
                    return False
            
            self.logger.debug("Config validation passed")
            return True
        except Exception as e:
            self.logger.log_error(e, "ConfigService.validate_config")
            return False
    
    def get_config_file_path(self) -> Optional[str]:
        """設定ファイルパスを取得"""
        return self.config_file
    
    def is_config_loaded(self) -> bool:
        """設定が読み込まれているかチェック"""
        return self.config_loaded 