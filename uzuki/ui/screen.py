import curses
import time
import sys
import os
from typing import Optional, List, Tuple
from uzuki.core.buffer import Buffer
from uzuki.core.cursor import Cursor
from uzuki.core.history import History
from uzuki.core.file_manager import FileManager
from uzuki.core.file_selector import FileSelector
from uzuki.input.handler import InputHandler
from uzuki.input.sequence_manager import KeySequenceManager
from uzuki.modes.normal_mode import NormalMode
from uzuki.modes.insert_mode import InsertMode
from uzuki.commands.command_mode import CommandMode
from uzuki.modes.file_browser_mode import FileBrowserMode
from uzuki.keymaps.manager import KeyMapManager
from uzuki.ui.status_line import StatusLineManager, StatusLineBuilder
from uzuki.ui.notification import NotificationManager, NotificationRenderer, NotificationLevel
from uzuki.ui.line_numbers import LineDisplayManager

class Screen:
    """メインのスクリーン管理クラス"""
    def __init__(self, initial_file: Optional[str] = None):
        # コアコンポーネント
        self.buffer = Buffer()
        self.cursor = Cursor()
        self.history = History()
        self.file_manager = FileManager()
        self.file_selector = FileSelector()
        
        # 変更通知コールバックを設定
        self.buffer.set_change_callback(self._on_buffer_change)
        self.cursor.set_move_callback(self._on_cursor_move)
        
        # モード
        self.normal_mode = NormalMode(self)
        self.insert_mode = InsertMode(self)
        self.command_mode = CommandMode(self)
        self.file_browser_mode = FileBrowserMode(self)
        self.mode = self.normal_mode
        
        # 入力処理
        self.input_handler = InputHandler(self)
        self.keymap = KeyMapManager(self)
        self.sequence_manager = KeySequenceManager()
        
        # UI管理
        self.status_line = StatusLineManager()
        self.status_builder = StatusLineBuilder(self.status_line)
        self.notifications = NotificationManager()
        self.notification_renderer = NotificationRenderer(self.notifications)
        self.line_display = LineDisplayManager()
        
        # 状態
        self.running = True
        self.needs_redraw = True
        
        # 初期ファイルの読み込み
        if initial_file:
            self._load_initial_file(initial_file)

    def _load_initial_file(self, filepath: str):
        """初期ファイルを読み込み"""
        try:
            # パスを解決
            resolved_path = self.file_selector.resolve_path(filepath)
            
            if os.path.isfile(resolved_path):
                self.load_file(resolved_path)
            elif os.path.isdir(resolved_path):
                # ディレクトリの場合はファイルブラウザーを開く
                self.file_selector.change_directory(resolved_path)
                self.file_browser_mode.enter_browser('normal')
            else:
                # ファイルが存在しない場合は新規作成
                self.file_manager.filename = resolved_path
                self.notify_info(f"New file: {resolved_path}")
        except Exception as e:
            self.notify_error(f"Failed to load initial file: {e}")

    def run(self, stdscr):
        """メインループ"""
        self.stdscr = stdscr
        curses.curs_set(1)
        
        # 色の初期化
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            # 色ペアを定義（より控えめな色）
            curses.init_pair(1, curses.COLOR_RED, -1)      # エラー用（赤）
            curses.init_pair(2, curses.COLOR_GREEN, -1)    # 成功用（緑）
            curses.init_pair(3, curses.COLOR_YELLOW, -1)   # 警告用（黄）
            curses.init_pair(4, curses.COLOR_BLUE, -1)     # 情報用（青）
            # 薄い色のペアを追加
            curses.init_pair(5, curses.COLOR_WHITE, -1)    # 薄い白（ハイライト用）
            curses.init_pair(6, curses.COLOR_CYAN, -1)     # 薄いシアン（カレント行用）
            
            # 通知システムの色を設定（より控えめに）
            self.notifications.set_colors({
                NotificationLevel.INFO: curses.A_NORMAL,
                NotificationLevel.SUCCESS: curses.A_DIM | curses.color_pair(2),
                NotificationLevel.WARNING: curses.A_DIM | curses.color_pair(3),
                NotificationLevel.ERROR: curses.A_DIM | curses.color_pair(1),
            })
        
        while self.running:
            # 画面を描画
            self.draw()
            
            # キー入力を待つ
            raw = stdscr.getch()
            self._handle_key(raw)

    def _handle_key(self, raw_code: int):
        """キー入力を処理（シーケンス対応）"""
        key_info = self.input_handler.create_key_info(raw_code)
        
        # キーシーケンスを管理
        sequence = self.sequence_manager.add_key(key_info.key_name)
        
        # アクションを検索
        action = self.keymap.get_action(self.mode.mode_name, sequence)
        
        if action:
            # アクションが見つかったら即座に実行
            action()
            self.sequence_manager.clear()
            # アクション実行後に画面を再描画
            self.draw()
        elif self.keymap.has_potential_mapping(self.mode.mode_name, sequence):
            # 潜在的なマッピングがある場合は待つ（何もしない）
            pass
        else:
            # マッピングがない場合は即座にデフォルト処理
            if len(sequence) == 1:
                self.mode.handle_default(key_info)
                # デフォルト処理後に画面を再描画
                self.draw()
            self.sequence_manager.clear()

    def draw(self):
        """画面を描画"""
        if not self.needs_redraw:
            return
            
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        
        # モードに応じて描画内容を変更
        if isinstance(self.mode, self.file_browser_mode.__class__):
            self._draw_file_browser(h, w)
        else:
            self._draw_editor(h, w)
        
        self.stdscr.refresh()
        self.needs_redraw = False

    def _draw_editor(self, h: int, w: int):
        """エディタ画面を描画"""
        # 通知エリアを描画
        notification_lines = self.notification_renderer.render(self.stdscr, w, h-2)
        
        # エディタコンテンツエリアの計算
        content_start_y = notification_lines
        content_height = h - 2 - notification_lines  # ステータスラインの分を引く
        
        # 行番号とコンテンツを描画
        line_num_width, display_lines = self.line_display.render_editor_content(
            self.stdscr, self.buffer.lines, self.cursor.row, self.cursor.col,
            content_start_y, 0, content_height, w
        )
        
        # カーソル位置を調整（行番号の幅を考慮）
        cursor_x = self.cursor.col + line_num_width
        cursor_y = content_start_y + self.cursor.row
        
        # ステータスラインを構築
        self._build_status_line()
        status_text = self.status_line.render(w)
        
        # ステータスラインを描画
        self.stdscr.addstr(h-1, 0, status_text[:w-1], curses.A_REVERSE)
        
        # カーソルを配置
        self.stdscr.move(cursor_y, cursor_x)

    def _draw_file_browser(self, h: int, w: int):
        """ファイルブラウザー画面を描画"""
        # ヘッダー
        header = f"File Browser - {self.file_selector.get_current_directory()}"
        self.stdscr.addstr(0, 0, header[:w-1], curses.A_BOLD)
        
        # ファイル一覧
        display_files = self.file_browser_mode.browser.get_display_files(h-4)
        
        for i, (name, path, is_dir, is_selected) in enumerate(display_files):
            if i + 2 >= h - 2:  # ステータスラインの分を引く
                break
            
            # アイコンと名前
            icon = "📁 " if is_dir else "📄 "
            display_name = icon + name
            
            # 選択状態のスタイル
            style = curses.A_REVERSE if is_selected else curses.A_NORMAL
            
            # ディレクトリの場合は太字
            if is_dir:
                style |= curses.A_BOLD
            
            self.stdscr.addstr(i + 2, 0, display_name[:w-1], style)
        
        # フィルタ情報
        if self.file_browser_mode.filter_mode:
            filter_info = f"Filter: {self.file_browser_mode.filter_text}"
            self.stdscr.addstr(h-3, 0, filter_info[:w-1], curses.A_BOLD)
        
        # ステータスライン
        status_info = self.file_browser_mode.get_status_info()
        status_text = f"Files: {status_info['total_files']} | Hidden: {'ON' if status_info['show_hidden'] else 'OFF'}"
        if status_info['selected_file']:
            status_text += f" | Selected: {os.path.basename(status_info['selected_file'])}"
        
        self.stdscr.addstr(h-1, 0, status_text[:w-1], curses.A_REVERSE)

    def _build_status_line(self):
        """ステータスラインを構築"""
        self.status_line.clear()
        
        if isinstance(self.mode, self.command_mode.__class__):
            # Command mode
            self.status_builder.command(self.mode.cmd_buf)
        else:
            # Normal/Insert mode
            file_info = self.file_manager.get_file_info()
            display_info = self.line_display.get_display_info()
            
            self.status_builder.mode(self.mode.__class__.__name__.replace('Mode', '').lower())
            self.status_builder.filename(file_info['name'])
            self.status_builder.position(self.cursor.row, self.cursor.col)
            self.status_builder.encoding(file_info['encoding'])
            self.status_builder.line_count(len(self.buffer.lines))
            
            # 行番号表示状態
            if display_info['line_numbers']:
                self.status_builder.custom('line_numbers', 'LN', width=3, align='right', priority=40)
            
            # カレント行ハイライト状態
            if display_info['current_line_highlight']:
                self.status_builder.custom('highlight', 'HL', width=3, align='right', priority=35)
            
            # キーシーケンス
            sequence = self.sequence_manager.get_sequence()
            if sequence:
                self.status_builder.sequence(sequence)
            
            # 変更フラグ
            if self.file_manager.is_modified:
                self.status_builder.custom('modified', '[+]', width=4, align='right', priority=85)

    def force_redraw(self):
        """強制的に画面を再描画"""
        self.needs_redraw = True
        self.draw()

    def set_mode(self, mode_name: str):
        """モードを切り替える"""
        if mode_name == 'normal':
            self.mode = self.normal_mode
        elif mode_name == 'insert':
            self.mode = self.insert_mode
        elif mode_name == 'command':
            self.mode = self.command_mode
        elif mode_name == 'file_browser':
            self.mode = self.file_browser_mode
        
        # モード切り替え時にシーケンスをクリア
        self.sequence_manager.clear()
        # モード切り替え後に画面を再描画
        self.draw()

    def quit(self):
        """エディタを終了"""
        self.running = False

    # ファイル操作
    def load_file(self, filepath: str):
        """ファイルを読み込み"""
        try:
            lines = self.file_manager.load_file(filepath)
            self.buffer.lines = lines
            self.cursor.row = 0
            self.cursor.col = 0
            self.notifications.add(f"Loaded: {filepath}", NotificationLevel.SUCCESS)
            self.needs_redraw = True
        except Exception as e:
            self.notifications.add(f"Failed to load file: {e}", NotificationLevel.ERROR, duration=5.0)

    def save_file(self, filepath: Optional[str] = None):
        """ファイルを保存"""
        try:
            save_path = filepath or self.file_manager.filename
            if not save_path:
                self.notifications.add("No file to save", NotificationLevel.WARNING)
                return
            
            self.file_manager.save_file(save_path, self.buffer.lines)
            self.notifications.add(f"Saved: {save_path}", NotificationLevel.SUCCESS)
            self.needs_redraw = True
        except Exception as e:
            self.notifications.add(f"Failed to save file: {e}", NotificationLevel.ERROR, duration=5.0)

    def set_encoding(self, encoding: str):
        """文字エンコーディングを設定"""
        try:
            self.file_manager.set_encoding(encoding)
            self.notifications.add(f"Encoding set to: {encoding}", NotificationLevel.INFO)
            self.needs_redraw = True
        except ValueError as e:
            self.notifications.add(str(e), NotificationLevel.ERROR)

    # ファイルブラウザー操作
    def open_file_browser(self, directory: Optional[str] = None):
        """ファイルブラウザーを開く"""
        if directory:
            self.file_selector.change_directory(directory)
        
        current_mode = self.mode.mode_name
        self.file_browser_mode.enter_browser(current_mode)

    # 通知システム（ピュアなAPI）
    def notify(self, message: str, level: NotificationLevel = NotificationLevel.INFO, 
               duration: float = 3.0, metadata: Optional[dict] = None):
        """通知を表示"""
        self.notifications.add(message, level, duration, metadata)
        self.needs_redraw = True

    def notify_info(self, message: str, duration: float = 3.0):
        """情報通知"""
        self.notify(message, NotificationLevel.INFO, duration)

    def notify_success(self, message: str, duration: float = 3.0):
        """成功通知"""
        self.notify(message, NotificationLevel.SUCCESS, duration)

    def notify_warning(self, message: str, duration: float = 4.0):
        """警告通知"""
        self.notify(message, NotificationLevel.WARNING, duration)

    def notify_error(self, message: str, duration: float = 5.0):
        """エラー通知"""
        self.notify(message, NotificationLevel.ERROR, duration)

    def clear_notifications(self):
        """すべての通知をクリア"""
        self.notifications.clear()
        self.needs_redraw = True

    # ステータスライン操作
    def add_status_segment(self, name: str, content: str, width: Optional[int] = None, 
                          align: str = 'left', priority: int = 0):
        """ステータスラインにセグメントを追加"""
        self.status_line.add_segment(name, content, width, align, priority)
        self.needs_redraw = True

    def update_status_segment(self, name: str, content: str):
        """ステータスラインのセグメントを更新"""
        self.status_line.update_segment(name, content)
        self.needs_redraw = True

    def remove_status_segment(self, name: str):
        """ステータスラインのセグメントを削除"""
        self.status_line.remove_segment(name)
        self.needs_redraw = True

    # 行表示操作
    def toggle_line_numbers(self):
        """行番号表示を切り替え"""
        self.line_display.toggle_line_numbers()
        self.needs_redraw = True

    def toggle_current_line_highlight(self):
        """カレント行ハイライトを切り替え"""
        self.line_display.toggle_current_line_highlight()
        self.needs_redraw = True

    def toggle_ruler(self):
        """ルーラー表示を切り替え"""
        self.line_display.toggle_ruler()
        self.needs_redraw = True

    def highlight_line(self, line_num: int, style: Optional[int] = None):
        """行をハイライト"""
        self.line_display.highlighter.add_highlight(line_num, style)
        self.needs_redraw = True

    def highlight_error_line(self, line_num: int):
        """エラー行をハイライト"""
        self.line_display.highlighter.highlight_error_line(line_num)
        self.needs_redraw = True

    def highlight_warning_line(self, line_num: int):
        """警告行をハイライト"""
        self.line_display.highlighter.highlight_warning_line(line_num)
        self.needs_redraw = True

    def highlight_info_line(self, line_num: int):
        """情報行をハイライト"""
        self.line_display.highlighter.highlight_info_line(line_num)
        self.needs_redraw = True

    def highlight_success_line(self, line_num: int):
        """成功行をハイライト"""
        self.line_display.highlighter.highlight_success_line(line_num)
        self.needs_redraw = True

    def clear_line_highlights(self):
        """行ハイライトをクリア"""
        self.line_display.highlighter.clear_highlights()
        self.needs_redraw = True

    def set_highlight_style(self, style: int):
        """デフォルトのハイライトスタイルを設定"""
        self.line_display.highlighter.set_highlight_style(style)
        self.needs_redraw = True

    def set_error_highlight_style(self, style: int):
        """エラー行のハイライトスタイルを設定"""
        self.line_display.highlighter.set_error_style(style)
        self.needs_redraw = True

    def set_warning_highlight_style(self, style: int):
        """警告行のハイライトスタイルを設定"""
        self.line_display.highlighter.set_warning_style(style)
        self.needs_redraw = True

    def get_line_display_info(self) -> dict:
        """行表示情報を取得"""
        return self.line_display.get_display_info()

    # コールバック
    def _on_buffer_change(self):
        """バッファ変更時の処理"""
        self.file_manager.mark_modified()
        self.needs_redraw = True

    def _on_cursor_move(self):
        """カーソル移動時の処理"""
        self.needs_redraw = True
