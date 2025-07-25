from typing import Protocol, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class MotionType(Enum):
    CHARACTER = "character"
    WORD = "word"
    LINE = "line"
    PARAGRAPH = "paragraph"
    BLOCK = "block"
    SEARCH = "search"
    CUSTOM = "custom"

@dataclass
class MotionResult:
    """モーションの結果"""
    start_pos: Tuple[int, int]
    end_pos: Tuple[int, int]
    inclusive: bool = True
    motion_type: MotionType = MotionType.CHARACTER

class IMotion(Protocol):
    """モーションのインターフェース"""
    name: str
    motion_type: MotionType
    
    def execute(self, cursor_pos: Tuple[int, int], buffer: 'IBuffer', 
                args: List[str] = None) -> MotionResult: ...

class IMotionRegistry(Protocol):
    """モーションレジストリのインターフェース"""
    
    def register_motion(self, motion: IMotion) -> None: ...
    def get_motion(self, name: str) -> Optional[IMotion]: ...
    def list_motions(self) -> List[str]: ... 