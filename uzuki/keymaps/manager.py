import os
import importlib.util
from typing import Dict, Any, Callable

class KeyMapManager:
    def __init__(self, screen):
        self.screen = screen
        self.global_bindings = {}
        self.mode_bindings = {
            'normal': {},
            'insert': {},
            'command': {}
        }
        
        # デフォルトキーマップを読み込み
        self._load_default_bindings()
        # ユーザー設定を読み込み
        self._load_user_config()
    
    def _load_default_bindings(self):
        """デフォルトキーマップを読み込み"""
        from .default import DefaultKeyMaps
        
        # グローバルバインド
        for key, action in DefaultKeyMaps.get_global_bindings().items():
            self.bind_global(key, action)
        
        # モード別バインド
        for mode, bindings in [
            ('normal', DefaultKeyMaps.get_normal_mode_bindings()),
            ('insert', DefaultKeyMaps.get_insert_mode_bindings()),
            ('command', DefaultKeyMaps.get_command_mode_bindings()),
        ]:
            for key, action in bindings.items():
                self.bind_mode(mode, key, action)
    
    def _load_user_config(self):
        """ユーザー設定ファイルを読み込み"""
        config_paths = [
            os.path.expanduser('~/.uzuki/config.py'),
            os.path.expanduser('~/.uzuki/init.py'),
            './.uzuki.py',
            './uzuki_config.py'
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                self._load_config_file(path)
                break
    
    def _load_config_file(self, path: str):
        """設定ファイルを動的に読み込み"""
        spec = importlib.util.spec_from_file_location("user_config", path)
        module = importlib.util.module_from_spec(spec)
        
        # 設定ファイル内でkeymapを使えるようにする
        module.keymap = self
        module.screen = self.screen
        
        spec.loader.exec_module(module)
    
    def bind_global(self, key: str, action: str):
        """グローバルキーバインド"""
        self.global_bindings[key] = action
    
    def bind_mode(self, mode: str, key: str, action: str):
        """モード別キーバインド"""
        if mode in self.mode_bindings:
            self.mode_bindings[mode][key] = action
    
    def unbind_global(self, key: str):
        """グローバルキーバインドを削除"""
        if key in self.global_bindings:
            del self.global_bindings[key]
    
    def unbind_mode(self, mode: str, key: str):
        """モード別キーバインドを削除"""
        if mode in self.mode_bindings and key in self.mode_bindings[mode]:
            del self.mode_bindings[mode][key]
    
    def get_action(self, mode: str, key: str) -> Callable:
        """キーに対応するアクションを取得"""
        # モード別バインドを優先
        if mode in self.mode_bindings and key in self.mode_bindings[mode]:
            action_name = self.mode_bindings[mode][key]
            # 現在のモードからアクションハンドラーを取得
            mode_handlers = self._get_mode_handlers(mode)
            return mode_handlers.get(action_name)
        
        # グローバルバインド
        if key in self.global_bindings:
            action_name = self.global_bindings[key]
            return self._get_global_handlers().get(action_name)
        
        return None
    
    def _get_mode_handlers(self, mode: str) -> Dict[str, Callable]:
        """モード別のアクションハンドラーを取得"""
        mode_map = {
            'normal': self.screen.normal_mode,
            'insert': self.screen.insert_mode,
            'command': self.screen.command_mode,
        }
        
        mode_obj = mode_map.get(mode)
        if mode_obj and hasattr(mode_obj, 'get_action_handlers'):
            return mode_obj.get_action_handlers()
        return {}
    
    def _get_global_handlers(self) -> Dict[str, Callable]:
        """グローバルアクションハンドラーを取得"""
        return {
            'quit': lambda: self.screen.quit(),
            'save': lambda: self.screen.save(),
        } 