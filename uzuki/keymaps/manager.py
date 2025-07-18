import os
import importlib.util
from typing import Dict, Any, Callable, List, Union

class Mode:
    """モード定数 - Neovim風のAPI"""
    NORMAL = 'normal'
    INSERT = 'insert'
    COMMAND = 'command'
    FILE_BROWSER = 'file_browser'
    GLOBAL = 'global'
    
    # 便利なエイリアス
    VISUAL = 'visual'  # 将来的な拡張用
    TERMINAL = 'terminal'  # 将来的な拡張用

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
    
    def file_browser(self, key: str, action: Union[str, Callable]):
        """File Browser modeのキーマップを設定"""
        self.add_keymap('file_browser', key, action)
    
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
    
    def load_from_config(self, config: Dict[str, Any]):
        """設定からキーマップを読み込み"""
        # 既存のキーマップをクリア
        self.keymaps.clear()
        
        # デフォルトキーマップを再読み込み
        self._load_default_keymaps()
        
        # 設定からキーマップを読み込み
        for mode, bindings in config.items():
            if isinstance(bindings, dict):
                for key, action in bindings.items():
                    self.add_keymap(mode, key, action)
    
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
            ('file_browser', DefaultKeyMaps.get_file_browser_bindings()),
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
    
    def has_potential_mapping(self, mode: str, sequence: str) -> bool:
        """指定されたシーケンスで始まるマッピングが存在するかチェック"""
        from uzuki.input.keycodes import Key
        
        # モード固有のマッピングをチェック
        for keymap in self.keymaps:
            if keymap['mode'] == mode:
                key = keymap['key']
                
                # コンボキーの場合、プレフィックスが一致するかチェック
                if Key.is_combo_key(key):
                    prefix = Key.get_combo_prefix(key)
                    if sequence.startswith(prefix):
                        return True
                # 通常のキーの場合
                elif key.startswith(sequence):
                    return True
        
        # グローバルマッピングもチェック
        for keymap in self.keymaps:
            if keymap['mode'] == 'global':
                key = keymap['key']
                
                # コンボキーの場合、プレフィックスが一致するかチェック
                if Key.is_combo_key(key):
                    prefix = Key.get_combo_prefix(key)
                    if sequence.startswith(prefix):
                        return True
                # 通常のキーの場合
                elif key.startswith(sequence):
                    return True
        
        return False
    
    def get_action(self, mode: str, key_sequence: str) -> Callable:
        """キーシーケンスに対応するアクションを取得（最長一致）"""
        # 最長一致で検索（キーの長さで降順ソート）
        for keymap in sorted(self.keymaps, key=lambda x: len(x['key']), reverse=True):
            if (keymap['mode'] == mode and 
                key_sequence.endswith(keymap['key'])):
                action = keymap['action']
                if callable(action):
                    return action
                else:
                    return self._get_action_handler(mode, action)
        
        # グローバルキーマップを検索
        for keymap in sorted(self.keymaps, key=lambda x: len(x['key']), reverse=True):
            if (keymap['mode'] == 'global' and 
                key_sequence.endswith(keymap['key'])):
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
            'file_browser': self.screen.file_browser_mode,
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
            'save': lambda: self.screen.save_file(),
        } 