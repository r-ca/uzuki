"""
Interfaces Package

Core interfaces for the Uzuki editor.
"""

from .editor_interface import IEditorService
from .file_interface import IFileService
from .config_interface import IConfigService
from .notification_interface import INotificationService
from .command_interface import ICommandRegistry, ICommand
from .motion_interface import IMotionRegistry, IMotion
from .operator_interface import IOperatorRegistry, IOperator

__all__ = [
    'IEditorService',
    'IFileService', 
    'IConfigService',
    'INotificationService',
    'ICommandRegistry',
    'ICommand',
    'IMotionRegistry',
    'IMotion',
    'IOperatorRegistry',
    'IOperator',
] 