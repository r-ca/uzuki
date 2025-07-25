from typing import Protocol, List, Optional, Any
from dataclasses import dataclass

@dataclass
class CommandContext:
    """コマンド実行時のコンテキスト"""
    container: 'ServiceContainer'
    args: List[str]
    kwargs: dict

class ICommand(Protocol):
    """コマンドのインターフェース"""
    name: str
    description: str
    
    def execute(self, context: CommandContext) -> Any: ...

class ICommandRegistry(Protocol):
    """コマンドレジストリのインターフェース"""
    
    def register_command(self, command: ICommand) -> None: ...
    def get_command(self, name: str) -> Optional[ICommand]: ...
    def list_commands(self) -> List[str]: ... 