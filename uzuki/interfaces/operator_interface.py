from typing import Protocol, List, Optional, Any
from dataclasses import dataclass

@dataclass
class OperatorContext:
    """オペレーター実行時のコンテキスト"""
    motion_result: 'MotionResult'
    buffer: 'IBuffer'
    cursor: 'ICursor'
    args: List[str]
    kwargs: dict

class IOperator(Protocol):
    """オペレーターのインターフェース"""
    name: str
    description: str
    
    def execute(self, context: OperatorContext) -> Any: ...

class IOperatorRegistry(Protocol):
    """オペレーターレジストリのインターフェース"""
    
    def register_operator(self, operator: IOperator) -> None: ...
    def get_operator(self, name: str) -> Optional[IOperator]: ...
    def list_operators(self) -> List[str]: ... 