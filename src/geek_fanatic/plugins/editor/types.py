#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编辑器类型定义模块
"""

from dataclasses import dataclass
from typing import Protocol

@dataclass
class Position:
    """文本位置
    
    表示文本中的一个位置，使用行号和列号表示。
    行号和列号都从0开始计数。
    
    Attributes:
        line: 行号
        column: 列号
    """
    line: int
    column: int

class TextOperation(Protocol):
    """文本操作协议类
    
    定义文本操作的接口。
    """
    def reverse(self) -> 'TextOperation':
        """返回此操作的逆操作"""
        ...

@dataclass
class InsertOperation:
    """插入操作
    
    表示在指定位置插入文本的操作。
    
    Attributes:
        position: 插入位置
        text: 要插入的文本
    """
    position: Position
    text: str

    def reverse(self) -> 'DeleteOperation':
        """返回对应的删除操作"""
        end_position = Position(
            self.position.line,
            self.position.column + len(self.text)
        )
        return DeleteOperation(self.position, end_position, self.text)

@dataclass
class DeleteOperation:
    """删除操作
    
    表示删除指定范围文本的操作。
    
    Attributes:
        start: 起始位置
        end: 结束位置
        deleted_text: 被删除的文本
    """
    start: Position
    end: Position
    deleted_text: str

    def reverse(self) -> 'InsertOperation':
        """返回对应的插入操作"""
        return InsertOperation(self.start, self.deleted_text)
