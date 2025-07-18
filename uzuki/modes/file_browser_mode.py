import curses
from uzuki.modes.base_mode import BaseMode
from uzuki.core.file_selector import FileBrowser
from uzuki.ui.notification import NotificationLevel

class FileBrowserMode(BaseMode):
    """File Browser mode - ファイル選択モード"""
    
    def __init__(self, screen):
        super().__init__(screen, 'file_browser')
        self.browser = FileBrowser(screen.file_selector)
        self.filter_mode = False
        self.filter_text = ""
        self.original_mode = None
    
    def get_action_handlers(self):
        """File Browser modeのアクションハンドラー"""
        return {
            # ナビゲーション
            'move_up': self.browser.move_up,
            'move_down': self.browser.move_down,
            'move_left': self._go_parent_directory,
            'move_right': self._enter_directory,
            
            # ファイル操作
            'open_file': self._open_selected_file,
            'create_file': self._create_file,
            'delete_file': self._delete_file,
            
            # フィルタリング
            'toggle_filter': self._toggle_filter_mode,
            'clear_filter': self._clear_filter,
            'toggle_hidden': self.browser.toggle_hidden_files,
            
            # モード切り替え
            'enter_normal_mode': self._exit_browser,
            'cancel': self._exit_browser,
        }
    
    def handle_default(self, key_info):
        """デフォルト処理"""
        if self.filter_mode and key_info.is_printable and key_info.char:
            self.filter_text += key_info.char
            self.browser.set_filter(self.filter_text)
        elif key_info.key_name == 'backspace' and self.filter_mode:
            self.filter_text = self.filter_text[:-1]
            self.browser.set_filter(self.filter_text)
    
    def enter_browser(self, original_mode):
        """ブラウザーモードに入る"""
        self.original_mode = original_mode
        self.screen.set_mode('file_browser')
    
    def _exit_browser(self):
        """ブラウザーモードを終了"""
        if self.original_mode:
            self.screen.set_mode(self.original_mode)
        else:
            self.screen.set_mode('normal')
    
    def _go_parent_directory(self):
        """親ディレクトリに移動"""
        parent_dir = self.screen.file_selector.get_parent_directory()
        if self.screen.file_selector.change_directory(parent_dir):
            self.browser.current_index = 0
            self.browser.scroll_offset = 0
            self.screen.notify_info(f"Changed to: {parent_dir}")
        else:
            self.screen.notify_warning("Cannot access parent directory")
    
    def _enter_directory(self):
        """選択されたディレクトリに入る"""
        selected_file = self.browser.get_selected_file()
        if selected_file and self.screen.file_selector.is_valid_directory(selected_file):
            if self.screen.file_selector.change_directory(selected_file):
                self.browser.current_index = 0
                self.browser.scroll_offset = 0
                self.screen.notify_info(f"Entered: {selected_file}")
            else:
                self.screen.notify_warning("Cannot access directory")
    
    def _open_selected_file(self):
        """選択されたファイルを開く"""
        selected_file = self.browser.get_selected_file()
        if selected_file and self.screen.file_selector.is_valid_file(selected_file):
            try:
                self.screen.load_file(selected_file)
                self._exit_browser()
            except Exception as e:
                self.screen.notify_error(f"Failed to open file: {e}")
        else:
            self.screen.notify_warning("Please select a valid file")
    
    def _create_file(self):
        """新しいファイルを作成"""
        # TODO: ファイル作成ダイアログの実装
        self.screen.notify_info("File creation not implemented yet")
    
    def _delete_file(self):
        """選択されたファイルを削除"""
        # TODO: ファイル削除確認ダイアログの実装
        self.screen.notify_info("File deletion not implemented yet")
    
    def _toggle_filter_mode(self):
        """フィルタモードを切り替え"""
        self.filter_mode = not self.filter_mode
        if self.filter_mode:
            self.screen.notify_info("Filter mode: Type to filter files")
        else:
            self.screen.notify_info("Filter mode disabled")
    
    def _clear_filter(self):
        """フィルタをクリア"""
        self.filter_text = ""
        self.browser.set_filter("")
        self.screen.notify_info("Filter cleared")
    
    def get_status_info(self) -> dict:
        """ステータス情報を取得"""
        current_dir = self.screen.file_selector.get_current_directory()
        selected_file = self.browser.get_selected_file()
        
        return {
            'current_directory': current_dir,
            'selected_file': selected_file,
            'filter_mode': self.filter_mode,
            'filter_text': self.filter_text,
            'show_hidden': self.browser.show_hidden,
            'total_files': len(self.screen.file_selector.get_files_in_directory()),
        } 