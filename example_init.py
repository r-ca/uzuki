"""
Uzuki Configuration File - 実用的な設定例
Edit this file to customize your editor settings

This file is loaded automatically when Uzuki starts.
You can use Python's full power including functions, conditionals, and loops.
"""

# ============================================================================
# 基本設定 - 関数を使った設定
# ============================================================================

# エディタ設定
configure_editor(
    tab_size=4,
    expand_tabs=True,
    auto_indent=True,
    show_greeting=True,
    default_encoding='utf-8'
)

# 表示設定
configure_display(
    line_numbers=True,
    current_line_highlight=True,
    ruler=False,
    status_line=True,
    notifications=True,
    notification_duration=3.0
)

# ハイライト設定
configure_highlight(
    current_line_style='dim',
    error_line_style='dim_red',
    warning_line_style='dim_yellow',
    info_line_style='dim_blue',
    success_line_style='dim_green',
    line_number_style='dim',
    separator_style='dim'
)

# ============================================================================
# キーマップ設定 - 実用的なAPI
# ============================================================================

# 基本ナビゲーション
def setup_basic_navigation():
    """基本的なナビゲーション"""
    kmap.normal('h', 'move_left')
    kmap.normal('j', 'move_down')
    kmap.normal('k', 'move_up')
    kmap.normal('l', 'move_right')
    
    # 行移動
    kmap.normal('0', 'move_beginning_of_line')
    kmap.normal('$', 'move_end_of_line')
    kmap.normal('^', 'move_first_non_blank')
    kmap.normal('gg', 'move_beginning_of_file')
    kmap.normal('G', 'move_end_of_file')

# 編集操作
def setup_editing():
    """編集関連の操作"""
    # モード切り替え
    kmap.normal('i', 'enter_insert_mode')
    kmap.normal('a', 'append_after_cursor')
    kmap.normal('A', 'append_end_of_line')
    kmap.normal('o', 'new_line_below')
    kmap.normal('O', 'new_line_above')
    kmap.normal(':', 'enter_command_mode')
    
    # 削除・コピー・ペースト
    kmap.normal('x', 'delete_character')
    kmap.normal('dd', 'delete_line')
    kmap.normal('yy', 'yank_line')
    kmap.normal('p', 'paste_after')
    kmap.normal('P', 'paste_before')
    
    # アンドゥ・リドゥ
    kmap.normal('u', 'undo')
    kmap.normal('Ctrl+r', 'redo')

# ファイル操作
def setup_file_operations():
    """ファイル操作"""
    kmap.normal('Ctrl+s', 'save_file')
    kmap.normal('Ctrl+q', 'quit')
    kmap.normal('Ctrl+e', 'open_file_browser')

# 表示切り替え
def setup_display_toggles():
    """表示の切り替え"""
    kmap.normal('Ctrl+l', 'toggle_line_numbers')
    kmap.normal('Ctrl+h', 'toggle_current_line_highlight')
    kmap.normal('Ctrl+r', 'toggle_ruler')

# Insert mode
def setup_insert_mode():
    """Insert modeの設定"""
    kmap.insert('Escape', 'enter_normal_mode')
    kmap.insert('Ctrl+c', 'enter_normal_mode')
    kmap.insert('Enter', 'new_line')
    kmap.insert('Backspace', 'delete_backward')
    kmap.insert('Tab', 'indent')
    kmap.insert('Shift+Tab', 'unindent')

# Command mode
def setup_command_mode():
    """Command modeの設定"""
    kmap.command('Escape', 'enter_normal_mode')
    kmap.command('Ctrl+c', 'enter_normal_mode')
    kmap.command('Enter', 'execute_command')
    kmap.command('Backspace', 'delete_backward')

# File browser mode
def setup_file_browser():
    """File browser modeの設定"""
    kmap.file_browser('Escape', 'exit_browser')
    kmap.file_browser('Ctrl+c', 'exit_browser')
    kmap.file_browser('Enter', 'select_file')
    kmap.file_browser('h', 'move_up')
    kmap.file_browser('j', 'move_down')
    kmap.file_browser('k', 'move_up')
    kmap.file_browser('l', 'move_down')
    kmap.file_browser('g', 'move_beginning')
    kmap.file_browser('G', 'move_end')
    kmap.file_browser('f', 'enter_filter_mode')
    kmap.file_browser('a', 'toggle_hidden_files')
    kmap.file_browser('s', 'sort_files')

# ============================================================================
# カスタムキーマップ
# ============================================================================

def setup_custom_keymaps():
    """カスタムキーマップ"""
    # 複数モードに同時設定
    kmap.set([Mode.NORMAL, Mode.INSERT], 'Ctrl+b', 'move_backward')
    kmap.set([Mode.NORMAL, Mode.INSERT], 'Ctrl+f', 'move_forward')
    
    # 条件付きキーマップ
    if get_display('line_numbers', True):
        kmap.normal('Ctrl+n', 'toggle_line_numbers')
    
    # カスタム関数を使ったキーマップ
    def show_info():
        screen.notify_info("Custom action executed!")
    
    def toggle_features():
        screen.toggle_line_numbers()
        screen.toggle_current_line_highlight()
        screen.notify_success("Toggled display features")
    
    kmap.normal('Ctrl+t', show_info)
    kmap.normal('Ctrl+u', toggle_features)

def setup_leader_keymaps():
    """Leader keyを使ったキーマップ"""
    # SpaceキーをLeaderとして使用
    kmap.normal('<Space>', 'leader_key')
    
    # Leader + キーの組み合わせ
    kmap.normal('<Space>w', 'save_file')
    kmap.normal('<Space>q', 'quit')
    kmap.normal('<Space>e', 'open_file_browser')
    kmap.normal('<Space>n', 'toggle_line_numbers')
    kmap.normal('<Space>h', 'toggle_current_line_highlight')

# ============================================================================
# 便利な設定関数
# ============================================================================

def setup_workflow_keymaps():
    """ワークフロー用のキーマップ"""
    # 開発ワークフロー用のショートカット
    def save_and_notify():
        screen.save_file()
        screen.notify_success("File saved!")
    
    def quick_quit():
        screen.notify_info("Quitting...")
        screen.quit()
    
    kmap.normal('Ctrl+w', save_and_notify)
    kmap.normal('Ctrl+x', quick_quit)

def setup_file_settings():
    """ファイル設定"""
    configure_file(
        auto_save=False,
        backup_files=True,
        backup_extension='.bak',
        auto_reload=False,
        encoding_detection=True
    )

def setup_search_settings():
    """検索設定"""
    configure_search(
        case_sensitive=False,
        highlight_matches=True,
        incremental_search=True
    )

def setup_notification_settings():
    """通知設定"""
    configure_notification(
        max_notifications=5,
        position='bottom'
    )

def setup_status_line_settings():
    """ステータスライン設定"""
    configure_status_line(
        separator=' | ',
        alignment='left'
    )

def setup_greeting_settings():
    """Greeting設定"""
    set_greeting_content([
        "Welcome to Uzuki",
        "A Vim-like text editor in Python",
        "",
        "Press any key to continue..."
    ])
    set_greeting_bottom_text("")

# ============================================================================
# 設定の実行
# ============================================================================

# 基本キーマップを設定
setup_basic_navigation()
setup_editing()
setup_file_operations()
setup_display_toggles()
setup_insert_mode()
setup_command_mode()
setup_file_browser()

# カスタムキーマップを設定
setup_custom_keymaps()
setup_leader_keymaps()
setup_workflow_keymaps()

# その他の設定
setup_file_settings()
setup_search_settings()
setup_notification_settings()
setup_status_line_settings()
setup_greeting_settings()

# ============================================================================
# 設定の確認とログ
# ============================================================================

# 設定の確認
print("Uzuki configuration loaded!")
print(f"Tab size: {get_editor('tab_size')}")
print(f"Line numbers: {get_display('line_numbers')}")
print(f"Current encoding: {get_editor('default_encoding')}")

# カスタム設定の例
# 便利な関数を使った設定
set_tab_size(2)  # タブサイズを2に変更
disable_line_numbers()  # 行番号を無効化

print("Configuration completed successfully!") 