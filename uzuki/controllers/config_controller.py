"""
Config Controller

Manages configuration system including loading, saving, and applying
configuration settings to various components.
"""

from typing import Optional, Any
from uzuki.config import ConfigManager

class ConfigController:
    """設定システムを制御するコントローラー"""
    
    def __init__(self, screen, config_file: Optional[str] = None):
        self.screen = screen
        self.config_manager = ConfigManager(config_file, keymap_manager=screen.editor.keymap)
    
    def apply_config(self):
        """設定を適用"""
        # エディタ設定
        editor_config = self.config_manager.get_editor_config()
        self.screen.file.file_manager.encoding = editor_config.get('default_encoding', 'utf-8')
        
        # 表示設定
        display_config = self.config_manager.get_display_config()
        if not display_config.get('line_numbers', True):
            self.screen.ui.toggle_line_numbers()
        if not display_config.get('current_line_highlight', True):
            self.screen.ui.toggle_current_line_highlight()
        
        # 通知設定
        notification_config = self.config_manager.get_notification_config()
        self.screen.notifications.set_max_notifications(notification_config.get('max_notifications', 5))
        
        # Greeting設定
        greeting_config = self.config_manager.get_greeting_config()
        if greeting_config.get('content'):
            self.screen.ui.set_greeting_content(greeting_config['content'])
        if greeting_config.get('bottom_text'):
            self.screen.ui.set_greeting_bottom_text(greeting_config['bottom_text'])
        
        # キーマップ設定
        keymap_config = self.config_manager.get_keymap_config()
        self.screen.editor.load_keymap_config(keymap_config)
    
    def get_config(self, section: str = None, key: str = None):
        """設定値を取得"""
        if section is None:
            return self.config_manager.get_all_config()
        elif key is None:
            return self.config_manager.get_section(section)
        else:
            return self.config_manager.get_value(section, key)
    
    def set_config(self, section: str, key: str, value):
        """設定値を設定"""
        self.config_manager.set_value(section, key, value)
        self.apply_config()
    
    def reset_config(self, section: str = None):
        """設定をリセット"""
        if section:
            self.config_manager.reset_section(section)
        else:
            self.config_manager.reset_all()
        self.apply_config()
    
    def import_config(self, filepath: str):
        """設定をインポート"""
        self.config_manager.import_config(filepath)
        self.apply_config()
    
    def print_config(self, section: str = None):
        """設定を表示"""
        self.config_manager.print_config(section)
    
    def get_editor_config(self):
        """エディタ設定を取得"""
        return self.config_manager.get_editor_config()
    
    def get_display_config(self):
        """表示設定を取得"""
        return self.config_manager.get_display_config()
    
    def get_highlight_config(self):
        """ハイライト設定を取得"""
        return self.config_manager.get_highlight_config()
    
    def get_file_config(self):
        """ファイル設定を取得"""
        return self.config_manager.get_file_config()
    
    def get_search_config(self):
        """検索設定を取得"""
        return self.config_manager.get_search_config()
    
    def get_notification_config(self):
        """通知設定を取得"""
        return self.config_manager.get_notification_config()
    
    def get_status_line_config(self):
        """ステータスライン設定を取得"""
        return self.config_manager.get_status_line_config()
    
    def get_greeting_config(self):
        """Greeting設定を取得"""
        return self.config_manager.get_greeting_config()
    
    def get_keymap_config(self):
        """キーマップ設定を取得"""
        return self.config_manager.get_keymap_config() 