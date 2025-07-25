"""
Notification Service

Manages notification system including adding, removing, and rendering
notifications with different levels and durations.
"""

from typing import Optional, Dict, Any, List
from uzuki.interfaces import INotificationService
from uzuki.ui.notification import NotificationManager, NotificationRenderer, NotificationLevel
from uzuki.utils.debug import get_debug_logger

class NotificationService(INotificationService):
    """通知システムのビジネスロジックを実装するサービス"""
    
    def __init__(self, container):
        self.container = container
        self.logger = get_debug_logger()
        
        # 通知管理コンポーネント
        self.notification_manager = NotificationManager()
        self.notification_renderer = NotificationRenderer(self.notification_manager)
        
        # 設定
        self.max_notifications = 5
        self.default_duration = 3.0
    
    def add(self, message: str, level: NotificationLevel = NotificationLevel.INFO, 
            duration: float = None, metadata: Optional[Dict[str, Any]] = None) -> int:
        """通知を追加"""
        try:
            if duration is None:
                duration = self.default_duration
            
            notification_id = self.notification_manager.add(message, level, duration, metadata)
            self.logger.info(f"Notification added: [{level.name}] {message}")
            return notification_id
        except Exception as e:
            self.logger.log_error(e, f"NotificationService.add({message})")
            return -1
    
    def add_info(self, message: str, duration: float = None) -> int:
        """情報通知を追加"""
        return self.add(message, NotificationLevel.INFO, duration)
    
    def add_success(self, message: str, duration: float = None) -> int:
        """成功通知を追加"""
        return self.add(message, NotificationLevel.SUCCESS, duration)
    
    def add_warning(self, message: str, duration: float = None) -> int:
        """警告通知を追加"""
        return self.add(message, NotificationLevel.WARNING, duration)
    
    def add_error(self, message: str, duration: float = None) -> int:
        """エラー通知を追加"""
        return self.add(message, NotificationLevel.ERROR, duration)
    
    def remove(self, notification_id: int) -> bool:
        """通知を削除"""
        try:
            success = self.notification_manager.remove(notification_id)
            if success:
                self.logger.debug(f"Notification removed: {notification_id}")
            return success
        except Exception as e:
            self.logger.log_error(e, f"NotificationService.remove({notification_id})")
            return False
    
    def clear(self):
        """すべての通知をクリア"""
        try:
            self.notification_manager.clear()
            self.logger.debug("All notifications cleared")
        except Exception as e:
            self.logger.log_error(e, "NotificationService.clear")
    
    def get_active_notifications(self) -> List[Dict[str, Any]]:
        """アクティブな通知を取得"""
        try:
            return self.notification_manager.get_active_notifications()
        except Exception as e:
            self.logger.log_error(e, "NotificationService.get_active_notifications")
            return []
    
    def set_colors(self, colors: Dict[NotificationLevel, int]):
        """通知の色を設定"""
        try:
            self.notification_manager.set_colors(colors)
            self.logger.debug("Notification colors updated")
        except Exception as e:
            self.logger.log_error(e, "NotificationService.set_colors")
    
    def set_max_notifications(self, max_count: int):
        """最大通知数を設定"""
        try:
            self.max_notifications = max_count
            self.notification_manager.max_notifications = max_count
            self.logger.debug(f"Max notifications set to: {max_count}")
        except Exception as e:
            self.logger.log_error(e, f"NotificationService.set_max_notifications({max_count})")
    
    def set_notification_duration(self, duration: float):
        """デフォルトの通知表示時間を設定"""
        try:
            self.default_duration = duration
            self.logger.debug(f"Default notification duration set to: {duration}")
        except Exception as e:
            self.logger.log_error(e, f"NotificationService.set_notification_duration({duration})")
    
    def render(self, stdscr, width: int, max_height: int) -> int:
        """通知を描画し、使用した行数を返す"""
        try:
            return self.notification_renderer.render(stdscr, width, max_height)
        except Exception as e:
            self.logger.log_error(e, "NotificationService.render")
            return 0
    
    def update(self):
        """通知を更新（期限切れの通知を削除）"""
        try:
            self.notification_manager.update()
        except Exception as e:
            self.logger.log_error(e, "NotificationService.update")
    
    def get_notification_count(self) -> int:
        """通知数を取得"""
        try:
            return len(self.notification_manager.notifications)
        except Exception as e:
            self.logger.log_error(e, "NotificationService.get_notification_count")
            return 0 