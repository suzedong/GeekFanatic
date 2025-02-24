#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文本缓冲区实现模块
"""

from typing import List, Optional

from .types import Position, TextOperation, InsertOperation, DeleteOperation

class TextBuffer:
    """文本缓冲区类
    
    提供基础的文本存储和操作功能。
    """

    def __init__(self) -> None:
        """初始化缓冲区"""
        self._content: List[str] = [""]  # 按行存储的内容
        self._undo_stack: List[TextOperation] = []  # 撤销栈
        self._redo_stack: List[TextOperation] = []  # 重做栈

    def get_content(self) -> str:
        """获取完整内容"""
        return "\n".join(self._content)

    def set_content(self, text: str) -> None:
        """设置完整内容"""
        self._content = text.split("\n")
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_line(self, line_number: int) -> str:
        """获取指定行的内容"""
        if 0 <= line_number < len(self._content):
            return self._content[line_number]
        return ""

    def get_line_count(self) -> int:
        """获取总行数"""
        return len(self._content)

    def insert(self, position: Position, text: str) -> None:
        """插入文本
        
        Args:
            position: 插入位置
            text: 要插入的文本
        """
        operation = InsertOperation(position, text)
        self._execute_operation(operation)
        self._undo_stack.append(operation)
        self._redo_stack.clear()

    def delete(self, start: Position, end: Position) -> None:
        """删除文本
        
        Args:
            start: 起始位置
            end: 结束位置
        """
        # 确保起始位置在结束位置之前
        if (start.line > end.line or 
            (start.line == end.line and start.column > end.column)):
            start, end = end, start

        # 获取要删除的文本
        deleted_text = self._get_text(start, end)
        operation = DeleteOperation(start, end, deleted_text)
        self._execute_operation(operation)
        self._undo_stack.append(operation)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """撤销操作
        
        Returns:
            bool: 是否成功撤销
        """
        if not self._undo_stack:
            return False

        operation = self._undo_stack.pop()
        reversed_operation = operation.reverse()
        self._execute_operation(reversed_operation)
        self._redo_stack.append(operation)
        return True

    def redo(self) -> bool:
        """重做操作
        
        Returns:
            bool: 是否成功重做
        """
        if not self._redo_stack:
            return False

        operation = self._redo_stack.pop()
        self._execute_operation(operation)
        self._undo_stack.append(operation)
        return True

    def _execute_operation(self, operation: TextOperation) -> None:
        """执行文本操作
        
        Args:
            operation: 要执行的操作
        """
        if isinstance(operation, InsertOperation):
            self._insert_text(operation.position, operation.text)
        elif isinstance(operation, DeleteOperation):
            self._delete_text(operation.start, operation.end)

    def _insert_text(self, position: Position, text: str) -> None:
        """在指定位置插入文本"""
        if not text:
            return

        # 处理多行插入
        lines = text.split("\n")
        current_line = self._content[position.line]
        
        if len(lines) == 1:
            # 单行插入
            new_line = (current_line[:position.column] + 
                       text + 
                       current_line[position.column:])
            self._content[position.line] = new_line
        else:
            # 多行插入
            first_line = current_line[:position.column] + lines[0]
            last_line = lines[-1] + current_line[position.column:]
            
            # 替换当前行并插入新行
            self._content[position.line] = first_line
            self._content[position.line + 1:position.line + 1] = lines[1:-1]
            self._content.insert(position.line + len(lines) - 1, last_line)

    def _delete_text(self, start: Position, end: Position) -> None:
        """删除指定范围的文本"""
        if start.line == end.line:
            # 单行删除
            line = self._content[start.line]
            new_line = line[:start.column] + line[end.column:]
            self._content[start.line] = new_line
        else:
            # 多行删除
            first_line = self._content[start.line][:start.column]
            last_line = self._content[end.line][end.column:]
            
            # 合并首尾行
            self._content[start.line] = first_line + last_line
            # 删除中间行
            del self._content[start.line + 1:end.line + 1]

    def _get_text(self, start: Position, end: Position) -> str:
        """获取指定范围的文本"""
        if start.line == end.line:
            # 单行文本
            return self._content[start.line][start.column:end.column]
        
        # 多行文本
        result = []
        # 第一行
        result.append(self._content[start.line][start.column:])
        # 中间行
        result.extend(self._content[start.line + 1:end.line])
        # 最后一行
        result.append(self._content[end.line][:end.column])
        
        return "\n".join(result)
