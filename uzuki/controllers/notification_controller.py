"""
Notification Controller

Manages notification system including adding, removing, and rendering
notifications with different levels and durations.
"""

from typing import Optional, Dict, Any
from uzuki.ui.notification import NotificationManager, NotificationRenderer, NotificationLevel

class NotificationController:
    """通知システムを制御するコントローラー"""
    
    def __init__(self, screen):
        self.screen = screen
        self.notifications = NotificationManager()
        self.notification_renderer = NotificationRenderer(self.notifications)
    
    def add(self, message: str, level: NotificationLevel = NotificationLevel.INFO, 
            duration: float = 3.0, metadata: Optional[Dict[str, Any]] = None):
        """通知を追加"""
        self.notifications.add(message, level, duration, metadata)
        self.screen.editor.needs_redraw = True
    
    def add_info(self, message: str, duration: float = 3.0):
        """情報通知を追加"""
        self.add(message, NotificationLevel.INFO, duration)
    
    def add_success(self, message: str, duration: float = 3.0):
        """成功通知を追加"""
        self.add(message, NotificationLevel.SUCCESS, duration)
    
    def add_warning(self, message: str, duration: float = 4.0):
        """警告通知を追加"""
        self.add(message, NotificationLevel.WARNING, duration)
    
    def add_error(self, message: str, duration: float = 5.0):
        """エラー通知を追加"""
        self.add(message, NotificationLevel.ERROR, duration)
    
    def remove(self, notification_id: int):
        """通知を削除"""
        self.notifications.remove(notification_id)
        self.screen.editor.needs_redraw = True
    
    def clear(self):
        """すべての通知をクリア"""
        self.notifications.clear()
        self.screen.editor.needs_redraw = True
    
    def get_active_notifications(self):
        """アクティブな通知を取得"""
        return self.notifications.get_active_notifications()
    
    def set_colors(self, colors: Dict[NotificationLevel, int]):
        """通知の色を設定"""
        self.notifications.set_colors(colors)
    
    def set_max_notifications(self, max_count: int):
        """最大通知数を設定"""
        self.notifications.max_notifications = max_count
    
    def set_notification_duration(self, duration: float):
        """デフォルトの通知表示時間を設定"""
        self._default_duration = duration
    
    def render(self, stdscr, width: int, max_height: int) -> int:
        """通知を描画し、使用した行数を返す"""
        return self.notification_renderer.render(stdscr, width, max_height) 