"""
编辑器功能模块
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..editor import Editor


class EditorFeature(ABC):
    """编辑器功能基类"""

    def __init__(self, editor: "Editor") -> None:
        """初始化功能"""
        self._editor = editor

    @abstractmethod
    def initialize(self) -> None:
        """初始化功能"""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """清理功能"""
        pass
