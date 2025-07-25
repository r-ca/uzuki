"""
デフォルト設定
"""

class DefaultConfig:
    """デフォルト設定クラス"""
    
    # エディタ設定
    EDITOR = {
        'tab_size': 4,
        'expand_tabs': True,
        'auto_indent': True,
        'show_greeting': True,
        'default_encoding': 'utf-8',
    }
    
    # 表示設定
    DISPLAY = {
        'line_numbers': True,
        'current_line_highlight': True,
        'ruler': False,
        'status_line': True,
        'notifications': True,
        'notification_duration': 3.0,
    }
    
    # ハイライト設定
    HIGHLIGHT = {
        'current_line_style': 'dim',
        'error_line_style': 'dim_red',
        'warning_line_style': 'dim_yellow',
        'info_line_style': 'dim_blue',
        'success_line_style': 'dim_green',
        'line_number_style': 'dim',
        'separator_style': 'dim',
    }
    
    # キーマップ設定
    KEYMAP = {
        'normal': {
            'i': 'enter_insert_mode',
            'a': 'append_after_cursor',
            'A': 'append_end_of_line',
            'o': 'new_line_below',
            'O': 'new_line_above',
            'x': 'delete_character',
            'dd': 'delete_line',
            'yy': 'yank_line',
            'p': 'paste_after',
            'P': 'paste_before',
            'u': 'undo',
            'Ctrl+r': 'redo',
            'h': 'move_left',
            'j': 'move_down',
            'k': 'move_up',
            'l': 'move_right',
            '0': 'move_beginning_of_line',
            '$': 'move_end_of_line',
            '^': 'move_first_non_blank',
            'gg': 'move_beginning_of_file',
            'G': 'move_end_of_file',
            ':': 'enter_command_mode',
            'Ctrl+e': 'open_file_browser',
            'Ctrl+l': 'toggle_line_numbers',
            'Ctrl+h': 'toggle_current_line_highlight',
            'Ctrl+r': 'toggle_ruler',
            'Ctrl+s': 'save_file',
            'Ctrl+q': 'quit',
        },
        'insert': {
            'Escape': 'enter_normal_mode',
            'Ctrl+c': 'enter_normal_mode',
            'Enter': 'new_line',
            'Backspace': 'delete_backward',
            'Tab': 'indent',
            'Shift+Tab': 'unindent',
        },
        'command': {
            'Escape': 'enter_normal_mode',
            'Ctrl+c': 'enter_normal_mode',
            'Enter': 'execute_command',
            'Backspace': 'delete_backward',
        },
        'file_browser': {
            'Escape': 'exit_browser',
            'Ctrl+c': 'exit_browser',
            'Enter': 'select_file',
            'h': 'move_up',
            'j': 'move_down',
            'k': 'move_up',
            'l': 'move_down',
            'g': 'move_beginning',
            'G': 'move_end',
            'f': 'enter_filter_mode',
            'a': 'toggle_hidden_files',
            's': 'sort_files',
        }
    }
    
    # ファイル設定
    FILE = {
        'auto_save': False,
        'backup_files': True,
        'backup_extension': '.bak',
        'auto_reload': False,
        'encoding_detection': True,
    }
    
    # 検索設定
    SEARCH = {
        'case_sensitive': False,
        'highlight_matches': True,
        'incremental_search': True,
    }
    
    # 通知設定
    NOTIFICATION = {
        'levels': ['info', 'success', 'warning', 'error'],
        'max_notifications': 5,
        'position': 'bottom',
    }
    
    # ステータスライン設定
    STATUS_LINE = {
        'segments': ['mode', 'filename', 'position', 'encoding', 'line_count'],
        'separator': ' | ',
        'alignment': 'left',
    }
    
    # Greeting設定
    GREETING = {
        'content': [
            "Welcome to Uzuki",
            "A Vim-like text editor in Python",
            "",
            "Press any key to continue..."
        ],
        'bottom_text': "",
    }
    
    @classmethod
    def get_all_config(cls):
        """すべての設定を取得"""
        return {
            'editor': cls.EDITOR,
            'display': cls.DISPLAY,
            'highlight': cls.HIGHLIGHT,
            'keymap': cls.KEYMAP,
            'file': cls.FILE,
            'search': cls.SEARCH,
            'notification': cls.NOTIFICATION,
            'status_line': cls.STATUS_LINE,
            'greeting': cls.GREETING,
        }
    
    @classmethod
    def get_section(cls, section_name: str):
        """指定されたセクションの設定を取得"""
        config = cls.get_all_config()
        return config.get(section_name, {})
    
    @classmethod
    def get_value(cls, section_name: str, key: str, default=None):
        """設定値を取得"""
        section = cls.get_section(section_name)
        return section.get(key, default)

# デフォルト設定の辞書
DEFAULT_CONFIG = DefaultConfig.get_all_config() 