import os
import importlib.util
from typing import Dict, Any, Callable, List, Union

class Mode:
    """モード定数"""
    NORMAL = 'normal'
    INSERT = 'insert'
    COMMAND = 'command'
    GLOBAL = 'global'

class KeyMapManager:
    """キーマップ管理クラス - Neovim風のAPIを提供"""
    def __init__(self, screen):
        self.screen = screen
        self.keymaps = []  # フラットなリストで管理
        
        # デフォルトキーマップを読み込み
        self._load_default_keymaps()
        # ユーザー設定を読み込み
        self._load_user_config()
    
    # Neovim風のキーマップメソッド
    def normal(self, key: str, action: Union[str, Callable]):
        """Normal modeのキーマップを設定"""
        self.add_keymap('normal', key, action)
    
    def insert(self, key: str, action: Union[str, Callable]):
        """Insert modeのキーマップを設定"""
        self.add_keymap('insert', key, action)
    
    def command(self, key: str, action: Union[str, Callable]):
        """Command modeのキーマップを設定"""
        self.add_keymap('command', key, action)
    
    def set(self, modes: List[str], key: str, action: Union[str, Callable]):
        """複数モードに同時にキーマップを設定"""
        for mode in modes:
            self.add_keymap(mode, key, action)
    
    def global_(self, key: str, action: Union[str, Callable]):
        """グローバルキーマップを設定"""
        self.add_keymap('global', key, action)
    
    def unbind(self, mode: str, key: str):
        """キーマップを削除"""
        self.remove_keymap(mode, key)
    
    def unbind_all(self, modes: List[str], key: str):
        """複数モードからキーマップを削除"""
        for mode in modes:
            self.remove_keymap(mode, key)
    
    def _load_default_keymaps(self):
        """デフォルトキーマップを読み込み"""
        from .default import DefaultKeyMaps
        
        # グローバルバインド
        for key, action in DefaultKeyMaps.get_global_bindings().items():
            self.add_keymap('global', key, action)
        
        # モード別バインド
        for mode, bindings in [
            ('normal', DefaultKeyMaps.get_normal_mode_bindings()),
            ('insert', DefaultKeyMaps.get_insert_mode_bindings()),
            ('command', DefaultKeyMaps.get_command_mode_bindings()),
        ]:
            for key, action in bindings.items():
                self.add_keymap(mode, key, action)
    
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
        module.Mode = Mode  # モード定数も提供
        
        spec.loader.exec_module(module)
    
    def add_keymap(self, mode: str, key: str, action: Union[str, Callable]):
        """キーマップを追加（文字列または関数を受け取る）"""
        # 既存のキーマップを削除
        self.remove_keymap(mode, key)
        
        self.keymaps.append({
            'mode': mode,
            'key': key,
            'action': action
        })
    
    def remove_keymap(self, mode: str, key: str):
        """キーマップを削除"""
        self.keymaps = [km for km in self.keymaps 
                       if not (km['mode'] == mode and km['key'] == key)]
    
    def get_action(self, mode: str, key: str) -> Callable:
        """キーに対応するアクションを取得"""
        # 現在のモードのキーマップを検索
        for keymap in self.keymaps:
            if keymap['mode'] == mode and keymap['key'] == key:
                action = keymap['action']
                if callable(action):
                    return action
                else:
                    return self._get_action_handler(mode, action)
        
        # グローバルキーマップを検索
        for keymap in self.keymaps:
            if keymap['mode'] == 'global' and keymap['key'] == key:
                action = keymap['action']
                if callable(action):
                    return action
                else:
                    return self._get_action_handler('global', action)
        
        return None
    
    def _get_action_handler(self, mode: str, action_name: str) -> Callable:
        """アクションハンドラーを取得"""
        mode_map = {
            'normal': self.screen.normal_mode,
            'insert': self.screen.insert_mode,
            'command': self.screen.command_mode,
            'global': None,  # グローバルは特別処理
        }
        
        mode_obj = mode_map.get(mode)
        if mode == 'global':
            return self._get_global_handlers().get(action_name)
        elif mode_obj and hasattr(mode_obj, 'get_action_handlers'):
            return mode_obj.get_action_handlers().get(action_name)
        
        return None
    
    def _get_global_handlers(self) -> Dict[str, Callable]:
        """グローバルアクションハンドラーを取得"""
        return {
            'quit': lambda: self.screen.quit(),
            'save': lambda: self.screen.save(),
        } 