import time
import curses
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class NotificationLevel(Enum):
    """通知レベル"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

@dataclass
class Notification:
    """通知メッセージ"""
    id: int
    message: str
    level: NotificationLevel
    created_at: float
    duration: float
    metadata: Dict[str, Any]

class NotificationManager:
    """通知管理システム"""
    
    def __init__(self):
        self.notifications: List[Notification] = []
        self.next_id = 1
        self.max_notifications = 5
        self.auto_clear = True
        
        # 色設定
        self.colors = {
            NotificationLevel.INFO: curses.A_NORMAL,
            NotificationLevel.SUCCESS: curses.A_BOLD,
            NotificationLevel.WARNING: curses.A_BOLD,
            NotificationLevel.ERROR: curses.A_BOLD,
        }
    
    def _get_next_id(self) -> int:
        """次のIDを取得"""
        current_id = self.next_id
        self.next_id += 1
        return current_id
    
    def add(self, message: str, level: NotificationLevel = NotificationLevel.INFO, 
            duration: float = 3.0, metadata: Optional[Dict[str, Any]] = None) -> int:
        """通知を追加"""
        notification = Notification(
            id=self._get_next_id(),
            message=message,
            level=level,
            created_at=time.time(),
            duration=duration,
            metadata=metadata or {}
        )
        
        self.notifications.append(notification)
        
        # 最大数を超えた場合、古い通知を削除
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)
        
        return notification.id
    
    def remove(self, notification_id: int) -> bool:
        """指定されたIDの通知を削除"""
        initial_count = len(self.notifications)
        self.notifications = [n for n in self.notifications if n.id != notification_id]
        return len(self.notifications) < initial_count
    
    def clear(self):
        """すべての通知を削除"""
        self.notifications.clear()
    
    def get_active(self) -> List[Notification]:
        """有効な通知を取得（期限切れの通知を自動削除）"""
        current_time = time.time()
        active_notifications = []
        
        for notification in self.notifications:
            if current_time - notification.created_at < notification.duration:
                active_notifications.append(notification)
        
        # 期限切れの通知を削除
        self.notifications = active_notifications
        return active_notifications
    
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """IDで通知を取得"""
        for notification in self.notifications:
            if notification.id == notification_id:
                return notification
        return None
    
    def update(self, notification_id: int, **kwargs) -> bool:
        """通知を更新"""
        notification = self.get_by_id(notification_id)
        if notification:
            for key, value in kwargs.items():
                if hasattr(notification, key):
                    setattr(notification, key, value)
            return True
        return False
    
    def set_colors(self, colors: Dict[NotificationLevel, int]):
        """色設定を更新"""
        self.colors.update(colors)
    
    def get_color(self, level: NotificationLevel) -> int:
        """通知レベルに応じた色を取得"""
        return self.colors.get(level, curses.A_NORMAL)
    
    def set_max_notifications(self, max_count: int):
        """最大通知数を設定"""
        self.max_notifications = max_count
        # 現在の通知数が最大数を超えている場合は古い通知を削除
        while len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)

class NotificationRenderer:
    """通知表示クラス"""
    
    def __init__(self, manager: NotificationManager):
        self.manager = manager
        self.prefixes = {
            NotificationLevel.INFO: "[INFO]",
            NotificationLevel.SUCCESS: "[OK]",
            NotificationLevel.WARNING: "[WARN]",
            NotificationLevel.ERROR: "[ERROR]",
        }
    
    def render(self, stdscr, max_width: int, start_y: int) -> int:
        """通知を描画し、使用した行数を返す"""
        active_notifications = self.manager.get_active()
        
        if not active_notifications:
            return 0
        
        used_lines = 0
        
        for notification in active_notifications:
            if start_y - used_lines < 0:
                break
            
            # 通知メッセージを準備
            prefix = self.prefixes.get(notification.level, "[INFO]")
            message = f"{prefix} {notification.message}"
            
            # 画面幅に収まるように切り詰め
            if len(message) > max_width - 1:
                message = message[:max_width-4] + "..."
            
            # 色を設定
            color = self.manager.get_color(notification.level)
            
            # 通知を描画
            stdscr.addstr(start_y - used_lines, 0, message[:max_width-1], color)
            used_lines += 1
        
        return used_lines
    
    def set_prefixes(self, prefixes: Dict[NotificationLevel, str]):
        """プレフィックスを設定"""
        self.prefixes.update(prefixes) 