"""
設定管理クラス - Pythonらしい柔軟な設定システム
"""

import os
import importlib.util
from typing import Dict, Any, Optional
from .default_config import DefaultConfig

class ConfigManager:
    """設定管理クラス - Neovim風のPythonオブジェクト操作"""
    
    def __init__(self, config_file: Optional[str] = None, keymap_manager=None):
        self.config_file = config_file or self._get_default_config_path()
        self.config = {}
        self.keymap_manager = keymap_manager  # キーマップマネージャーへの参照
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """デフォルト設定ファイルパスを取得"""
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".config", "uzuki")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "init.py")
    
    def load_config(self):
        """設定を読み込み"""
        # デフォルト設定を読み込み
        self.config = DefaultConfig.get_all_config()
        
        # ユーザー設定ファイルが存在する場合は読み込み
        if os.path.exists(self.config_file):
            try:
                self._load_python_config()
            except Exception as e:
                print(f"Warning: Failed to load config file: {e}")
    
    def _load_python_config(self):
        """Python設定ファイルを読み込み"""
        spec = importlib.util.spec_from_file_location("user_config", self.config_file)
        module = importlib.util.module_from_spec(spec)
        
        # 設定ファイル内でconfigオブジェクトを使えるようにする
        module.config = self
        
        # 各セクションを辞書として提供（Neovim風のAPI）
        # getメソッドを持つ辞書オブジェクトを作成
        class ConfigDict(dict):
            def get(self, key, default=None):
                return super().get(key, default)
        
        module.editor = ConfigDict(self.config.get('editor', {}))
        module.display = ConfigDict(self.config.get('display', {}))
        module.highlight = ConfigDict(self.config.get('highlight', {}))
        module.keymap = ConfigDict(self.config.get('keymap', {}))
        module.file = ConfigDict(self.config.get('file', {}))
        module.search = ConfigDict(self.config.get('search', {}))
        module.notification = ConfigDict(self.config.get('notification', {}))
        module.status_line = ConfigDict(self.config.get('status_line', {}))
        module.greeting = ConfigDict(self.config.get('greeting', {}))
        
        # キーマップマネージャーを提供（Neovim風のAPI）
        if self.keymap_manager:
            module.keymap_manager = self.keymap_manager
            # 便利なエイリアス
            module.kmap = self.keymap_manager
            module.Mode = self.keymap_manager.Mode if hasattr(self.keymap_manager, 'Mode') else None
            
            # screenオブジェクトへのアクセス（キーマップマネージャー経由）
            if hasattr(self.keymap_manager, 'screen'):
                module.screen = self.keymap_manager.screen
        
        # 便利な関数も提供
        module.set = self.set_value
        module.get = self.get_value
        
        # 設定項目別の便利な関数
        module.set_editor = lambda key, value: self.set_value('editor', key, value)
        module.get_editor = lambda key, default=None: self.get_value('editor', key, default)
        
        module.set_display = lambda key, value: self.set_value('display', key, value)
        module.get_display = lambda key, default=None: self.get_value('display', key, default)
        
        module.set_highlight = lambda key, value: self.set_value('highlight', key, value)
        module.get_highlight = lambda key, default=None: self.get_value('highlight', key, default)
        
        module.set_file = lambda key, value: self.set_value('file', key, value)
        module.get_file = lambda key, default=None: self.get_value('file', key, default)
        
        module.set_search = lambda key, value: self.set_value('search', key, value)
        module.get_search = lambda key, default=None: self.get_value('search', key, default)
        
        module.set_notification = lambda key, value: self.set_value('notification', key, value)
        module.get_notification = lambda key, default=None: self.get_value('notification', key, default)
        
        module.set_status_line = lambda key, value: self.set_value('status_line', key, value)
        module.get_status_line = lambda key, default=None: self.get_value('status_line', key, default)
        
        module.set_greeting = lambda key, value: self.set_value('greeting', key, value)
        module.get_greeting = lambda key, default=None: self.get_value('greeting', key, default)
        
        # 設定の一括操作関数
        module.configure_editor = lambda **kwargs: [self.set_value('editor', k, v) for k, v in kwargs.items()]
        module.configure_display = lambda **kwargs: [self.set_value('display', k, v) for k, v in kwargs.items()]
        module.configure_highlight = lambda **kwargs: [self.set_value('highlight', k, v) for k, v in kwargs.items()]
        module.configure_file = lambda **kwargs: [self.set_value('file', k, v) for k, v in kwargs.items()]
        module.configure_search = lambda **kwargs: [self.set_value('search', k, v) for k, v in kwargs.items()]
        module.configure_notification = lambda **kwargs: [self.set_value('notification', k, v) for k, v in kwargs.items()]
        module.configure_status_line = lambda **kwargs: [self.set_value('status_line', k, v) for k, v in kwargs.items()]
        module.configure_greeting = lambda **kwargs: [self.set_value('greeting', k, v) for k, v in kwargs.items()]
        
        # 通知設定の便利関数
        module.set_notification_duration = lambda duration: self.set_value('notification', 'duration', duration)
        module.set_max_notifications = lambda max_count: self.set_value('notification', 'max_notifications', max_count)
        
        # 表示設定の便利関数
        module.enable_line_numbers = lambda: self.set_value('display', 'line_numbers', True)
        module.disable_line_numbers = lambda: self.set_value('display', 'line_numbers', False)
        module.enable_current_line_highlight = lambda: self.set_value('display', 'current_line_highlight', True)
        module.disable_current_line_highlight = lambda: self.set_value('display', 'current_line_highlight', False)
        module.enable_ruler = lambda: self.set_value('display', 'ruler', True)
        module.disable_ruler = lambda: self.set_value('display', 'ruler', False)
        
        # エディタ設定の便利関数
        module.set_tab_size = lambda size: self.set_value('editor', 'tab_size', size)
        module.enable_expand_tabs = lambda: self.set_value('editor', 'expand_tabs', True)
        module.disable_expand_tabs = lambda: self.set_value('editor', 'expand_tabs', False)
        module.enable_auto_indent = lambda: self.set_value('editor', 'auto_indent', True)
        module.disable_auto_indent = lambda: self.set_value('editor', 'auto_indent', False)
        module.set_encoding = lambda encoding: self.set_value('editor', 'default_encoding', encoding)
        
        # ファイル設定の便利関数
        module.enable_auto_save = lambda: self.set_value('file', 'auto_save', True)
        module.disable_auto_save = lambda: self.set_value('file', 'auto_save', False)
        module.enable_backup_files = lambda: self.set_value('file', 'backup_files', True)
        module.disable_backup_files = lambda: self.set_value('file', 'backup_files', False)
        module.set_backup_extension = lambda ext: self.set_value('file', 'backup_extension', ext)
        
        # Greeting設定の便利関数
        module.set_greeting_content = lambda content: self.set_value('greeting', 'content', content)
        module.set_greeting_bottom_text = lambda text: self.set_value('greeting', 'bottom_text', text)
        module.enable_greeting = lambda: self.set_value('editor', 'show_greeting', True)
        module.disable_greeting = lambda: self.set_value('editor', 'show_greeting', False)
        
        spec.loader.exec_module(module)
    
    def get_section(self, section_name: str) -> Dict[str, Any]:
        """指定されたセクションの設定を取得"""
        return self.config.get(section_name, {})
    
    def get_value(self, section_name: str, key: str, default=None):
        """指定された設定値を取得"""
        section = self.get_section(section_name)
        return section.get(key, default)
    
    def set_value(self, section_name: str, key: str, value: Any):
        """設定値を設定"""
        if section_name not in self.config:
            self.config[section_name] = {}
        self.config[section_name][key] = value
    
    def set_section(self, section_name: str, values: Dict[str, Any]):
        """セクション全体を設定"""
        self.config[section_name] = values.copy()
    
    def reset_section(self, section_name: str):
        """セクションをデフォルトにリセット"""
        default_config = DefaultConfig.get_all_config()
        if section_name in default_config:
            self.config[section_name] = default_config[section_name].copy()
    
    def reset_all(self):
        """すべての設定をデフォルトにリセット"""
        self.config = DefaultConfig.get_all_config()
    
    def get_all_config(self) -> Dict[str, Any]:
        """すべての設定を取得"""
        return self.config.copy()
    
    def import_config(self, filepath: str):
        """設定をインポート"""
        try:
            # 一時的に設定ファイルを変更して読み込み
            original_file = self.config_file
            self.config_file = filepath
            self._load_python_config()
            self.config_file = original_file
        except Exception as e:
            print(f"Error: Failed to import config: {e}")
    
    # 便利なメソッド
    def get_editor_config(self) -> Dict[str, Any]:
        """エディタ設定を取得"""
        return self.get_section('editor')
    
    def get_display_config(self) -> Dict[str, Any]:
        """表示設定を取得"""
        return self.get_section('display')
    
    def get_highlight_config(self) -> Dict[str, Any]:
        """ハイライト設定を取得"""
        return self.get_section('highlight')
    
    def get_keymap_config(self) -> Dict[str, Any]:
        """キーマップ設定を取得"""
        return self.get_section('keymap')
    
    def get_file_config(self) -> Dict[str, Any]:
        """ファイル設定を取得"""
        return self.get_section('file')
    
    def get_search_config(self) -> Dict[str, Any]:
        """検索設定を取得"""
        return self.get_section('search')
    
    def get_notification_config(self) -> Dict[str, Any]:
        """通知設定を取得"""
        return self.get_section('notification')
    
    def get_status_line_config(self) -> Dict[str, Any]:
        """ステータスライン設定を取得"""
        return self.get_section('status_line')
    
    def get_greeting_config(self) -> Dict[str, Any]:
        """Greeting設定を取得"""
        return self.get_section('greeting')
    
    # 設定の検証
    def validate_config(self) -> bool:
        """設定の妥当性を検証"""
        try:
            # 必須セクションの存在確認
            required_sections = ['editor', 'display', 'highlight', 'keymap']
            for section in required_sections:
                if section not in self.config:
                    print(f"Warning: Missing required section: {section}")
                    return False
            
            # キーマップの妥当性確認
            keymap = self.get_keymap_config()
            required_modes = ['normal', 'insert', 'command']
            for mode in required_modes:
                if mode not in keymap:
                    print(f"Warning: Missing required mode in keymap: {mode}")
                    return False
            
            return True
        except Exception as e:
            print(f"Error validating config: {e}")
            return False
    
    def print_config(self, section_name: Optional[str] = None):
        """設定を表示"""
        if section_name:
            config = self.get_section(section_name)
            print(f"\n=== {section_name.upper()} ===")
            for key, value in config.items():
                print(f"  {key}: {value}")
        else:
            for section, values in self.config.items():
                print(f"\n=== {section.upper()} ===")
                for key, value in values.items():
                    print(f"  {key}: {value}") 