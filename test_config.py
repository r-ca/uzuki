# テスト用設定ファイル
# このファイルを ~/.uzuki/config.py にコピーして使用

# 基本的なナビゲーション
keymap.normal('h', 'move_left')
keymap.normal('j', 'move_down')
keymap.normal('k', 'move_up')
keymap.normal('l', 'move_right')

# 編集操作
keymap.normal('i', 'enter_insert_mode')
keymap.normal('a', 'append')
keymap.normal('o', 'new_line_below')
keymap.normal('O', 'new_line_above')
keymap.normal('x', 'delete_char')
keymap.normal('dd', 'delete_line')

# Insert mode
keymap.insert('escape', 'enter_normal_mode')
keymap.insert('enter', 'new_line')
keymap.insert('backspace', 'delete_backward')

# Command mode
keymap.normal(':', 'enter_command_mode')
keymap.command('escape', 'enter_normal_mode')
keymap.command('enter', 'execute_command')

# グローバルキーマップ
keymap.global_('ctrl_c', 'quit')
keymap.global_('ctrl_s', 'save')

# 複数モードに同時設定
keymap.set([Mode.NORMAL, Mode.INSERT], 'ctrl_q', 'quit')

# カスタム関数
def my_custom_action():
    screen.set_message("Hello from custom action!")

keymap.normal('f1', my_custom_action)

# 複雑なロジック
def smart_indent():
    current_line = screen.buffer.lines[screen.cursor.row]
    if current_line.strip():  # 空行でない場合
        screen.buffer.insert(screen.cursor.row, 0, '    ')
        screen.cursor.move(0, 4, screen.buffer)
    else:
        screen.buffer.insert(screen.cursor.row, 0, '\n')

keymap.insert('tab', smart_indent)

# キーマップを削除
keymap.unbind('normal', 'dd')  # ddを無効化

# 複数モードから削除
keymap.unbind_all([Mode.NORMAL, Mode.INSERT], 'ctrl_q') 