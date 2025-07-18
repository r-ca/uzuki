class DefaultKeyMaps:
    @staticmethod
    def get_global_bindings():
        return {
            'ctrl_c': 'quit',
            'ctrl_s': 'save',
            'ctrl_q': 'quit',
        }
    
    @staticmethod
    def get_normal_mode_bindings():
        return {
            # ナビゲーション
            'h': 'move_left',
            'j': 'move_down', 
            'k': 'move_up',
            'l': 'move_right',
            
            # モード切り替え
            'i': 'enter_insert_mode',
            ':': 'enter_command_mode',
            'ctrl_e': 'open_file_browser',  # ファイルブラウザーを開く
            
            # 表示設定
            'ctrl_l': 'toggle_line_numbers',  # 行番号表示切り替え
            'ctrl_h': 'toggle_current_line_highlight',  # カレント行ハイライト切り替え
            'ctrl_r': 'toggle_ruler',  # ルーラー表示切り替え
            
            # 編集操作（単一キー）
            'x': 'delete_char',
            'o': 'new_line_below',
            'O': 'new_line_above',
            'a': 'append',
            'A': 'append_end',
            'p': 'paste',
            'P': 'paste_before',
            
            # 編集操作（複数キー）
            'dd': 'delete_line',
            'yy': 'yank_line',
            
            # その他
            'escape': 'noop',
        }
    
    @staticmethod
    def get_insert_mode_bindings():
        return {
            'escape': 'enter_normal_mode',
            'enter': 'new_line',
            'backspace': 'delete_backward',
            'tab': 'indent',
            'shift_tab': 'unindent',
        }
    
    @staticmethod
    def get_command_mode_bindings():
        return {
            'escape': 'enter_normal_mode',
            'enter': 'execute_command',
            'backspace': 'delete_backward',
        }
    
    @staticmethod
    def get_file_browser_bindings():
        return {
            # ナビゲーション
            'h': 'move_left',      # 親ディレクトリに移動
            'j': 'move_down',      # 下に移動
            'k': 'move_up',        # 上に移動
            'l': 'move_right',     # ディレクトリに入る/ファイルを開く
            'enter': 'open_file',  # ファイルを開く
            
            # フィルタリング
            '/': 'toggle_filter',  # フィルタモード切り替え
            'escape': 'clear_filter',  # フィルタクリア
            
            # 表示設定
            'ctrl_h': 'toggle_hidden',  # 隠しファイル表示切り替え
            
            # ファイル操作
            'n': 'create_file',    # 新規ファイル作成
            'd': 'delete_file',    # ファイル削除
            
            # モード切り替え
            'q': 'enter_normal_mode',  # ブラウザーを終了
            'escape': 'cancel',        # キャンセル
        } 