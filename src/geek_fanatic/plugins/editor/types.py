"""
编辑器类型定义
"""
from dataclasses import dataclass

@dataclass
class Position:
    """文本位置"""
    line: int
    column: int

    def __lt__(self, other: 'Position') -> bool:
        if self.line < other.line:
            return True
        if self.line == other.line:
            return self.column < other.column
        return False