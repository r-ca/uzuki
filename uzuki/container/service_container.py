"""
Service Container

Lightweight dependency injection container for managing service registrations
and resolutions with support for services, plugins, and hooks.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Type, Callable, List
from uzuki.interfaces import (
    IEditorService, IFileService, INotificationService, IConfigService
)
from uzuki.services import (
    EditorService, FileService, NotificationService, ConfigService
)
from uzuki.utils.debug import get_debug_logger

@dataclass
class ServiceRegistration:
    """サービス登録情報"""
    service_type: Type
    implementation: Type
    singleton: bool = True
    instance: Optional[Any] = None

class ServiceContainer:
    """サービスコンテナ"""
    
    def __init__(self):
        self.services: Dict[str, ServiceRegistration] = {}
        self.plugins: Dict[str, Any] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        self.logger = get_debug_logger()
        
        # デフォルトサービスを登録
        self._register_default_services()
    
    def _register_default_services(self):
        """デフォルトサービスを登録"""
        self.register_service(IEditorService, EditorService)
        self.register_service(IFileService, FileService)
        self.register_service(INotificationService, NotificationService)
        self.register_service(IConfigService, ConfigService)
        
        self.logger.info("Default services registered")
    
    def register_service(self, service_type: Type, implementation: Type, singleton: bool = True):
        """サービスを登録"""
        service_name = service_type.__name__
        self.services[service_name] = ServiceRegistration(
            service_type=service_type,
            implementation=implementation,
            singleton=singleton
        )
        self.logger.debug(f"Service registered: {service_name}")
    
    def resolve(self, service_type: Type) -> Any:
        """サービスを解決"""
        service_name = service_type.__name__
        
        if service_name not in self.services:
            raise ValueError(f"Service not registered: {service_name}")
        
        registration = self.services[service_name]
        
        # シングルトンの場合、インスタンスが存在すれば返す
        if registration.singleton and registration.instance is not None:
            return registration.instance
        
        # 新しいインスタンスを作成
        try:
            instance = registration.implementation(self)
            if registration.singleton:
                registration.instance = instance
            self.logger.debug(f"Service resolved: {service_name}")
            return instance
        except Exception as e:
            self.logger.log_error(e, f"ServiceContainer.resolve({service_name})")
            raise
    
    def get_editor_service(self) -> IEditorService:
        """エディタサービスを取得"""
        return self.resolve(IEditorService)
    
    def get_file_service(self) -> IFileService:
        """ファイルサービスを取得"""
        return self.resolve(IFileService)
    
    def get_notification_service(self) -> INotificationService:
        """通知サービスを取得"""
        return self.resolve(INotificationService)
    
    def get_config_service(self) -> IConfigService:
        """設定サービスを取得"""
        return self.resolve(IConfigService)
    
    def register_plugin(self, name: str, plugin: Any):
        """プラグインを登録"""
        self.plugins[name] = plugin
        self.logger.info(f"Plugin registered: {name}")
    
    def get_plugin(self, name: str) -> Optional[Any]:
        """プラグインを取得"""
        return self.plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, Any]:
        """すべてのプラグインを取得"""
        return self.plugins.copy()
    
    def register_hook(self, hook_name: str, callback: Callable):
        """フックを登録"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
        self.logger.debug(f"Hook registered: {hook_name}")
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """フックを実行"""
        results = []
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    self.logger.log_error(e, f"Hook execution failed: {hook_name}")
        return results
    
    def get_hook_manager(self):
        """フックマネージャーを取得"""
        return self
    
    def initialize_services(self):
        """すべてのサービスを初期化"""
        try:
            # サービスを順次初期化
            editor_service = self.get_editor_service()
            file_service = self.get_file_service()
            notification_service = self.get_notification_service()
            config_service = self.get_config_service()
            
            self.logger.info("All services initialized successfully")
            return True
        except Exception as e:
            self.logger.log_error(e, "ServiceContainer.initialize_services")
            return False
    
    def shutdown(self):
        """コンテナをシャットダウン"""
        try:
            # プラグインのクリーンアップ
            for name, plugin in self.plugins.items():
                if hasattr(plugin, 'cleanup'):
                    try:
                        plugin.cleanup()
                    except Exception as e:
                        self.logger.log_error(e, f"Plugin cleanup failed: {name}")
            
            # サービスインスタンスのクリア
            for registration in self.services.values():
                registration.instance = None
            
            self.logger.info("Service container shutdown completed")
        except Exception as e:
            self.logger.log_error(e, "ServiceContainer.shutdown") 