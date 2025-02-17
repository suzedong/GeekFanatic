"""
文本缓冲区实现
"""

from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtCore import QObject, Signal

from geek_fanatic.plugins.editor.types import Position


@dataclass
class TextOperation:
    """文本操作基类"""

    start: Position
    text: str

    def apply(self, buffer: "TextBuffer") -> None:
        """应用操作"""
        raise NotImplementedError

    def revert(self, buffer: "TextBuffer") -> None:
        """撤销操作"""
        raise NotImplementedError


@dataclass
class InsertOperation(TextOperation):
    """插入操作"""

    def apply(self, buffer: "TextBuffer") -> None:
        """应用插入操作"""
        lines = self.text.split("\n")
        if len(lines) == 1:
            # 单行插入
            line = buffer._content[self.start.line]
            new_line = line[: self.start.column] + self.text + line[self.start.column :]
            buffer._content[self.start.line] = new_line
        else:
            # 多行插入
            current_line = buffer._content[self.start.line]
            first_line = current_line[: self.start.column] + lines[0]
            last_line = lines[-1] + current_line[self.start.column :]

            # 更新第一行和添加中间行
            buffer._content[self.start.line] = first_line
            for i, line in enumerate(lines[1:-1], 1):
                buffer._content.insert(self.start.line + i, line)
            buffer._content.insert(self.start.line + len(lines) - 1, last_line)

    def revert(self, buffer: "TextBuffer") -> None:
        """撤销插入操作"""
        lines = self.text.split("\n")
        if len(lines) == 1:
            # 单行删除
            line = buffer._content[self.start.line]
            new_line = (
                line[: self.start.column] + line[self.start.column + len(self.text) :]
            )
            buffer._content[self.start.line] = new_line
        else:
            # 多行删除
            current_line = buffer._content[self.start.line]
            last_line = buffer._content[self.start.line + len(lines) - 1]
            new_line = current_line[: self.start.column] + last_line[len(lines[-1]) :]

            # 删除中间行并更新第一行
            for _ in range(len(lines) - 1):
                buffer._content.pop(self.start.line + 1)
            buffer._content[self.start.line] = new_line


@dataclass
class DeleteOperation:
    """删除操作"""

    start: Position
    end: Position
    deleted_text: str  # 存储被删除的文本，用于撤销操作

    def apply(self, buffer: "TextBuffer") -> None:
        """应用删除操作"""
        if self.start.line == self.end.line:
            # 单行删除
            line = buffer._content[self.start.line]
            new_line = line[: self.start.column] + line[self.end.column :]
            buffer._content[self.start.line] = new_line
        else:
            # 多行删除，合并起始行和结束行
            first_line = buffer._content[self.start.line]
            last_line = buffer._content[self.end.line]

            # 只保留起始行前半部分和结束行后半部分，直接拼接
            # 不添加换行符，因为这是多行删除
            new_line = first_line[: self.start.column] + last_line[self.end.column :]
            buffer._content[self.start.line] = new_line

            # 删除中间所有行（包括末行）
            for _ in range(self.end.line - self.start.line):
                buffer._content.pop(self.start.line + 1)

    def revert(self, buffer: "TextBuffer") -> None:
        """撤销删除操作"""
        InsertOperation(self.start, self.deleted_text).apply(buffer)


class TextBuffer(QObject):
    """文本缓冲区实现"""

    # 信号
    contentChanged = Signal()

    def __init__(self) -> None:
        """初始化缓冲区"""
        super().__init__()
        self._content: List[str] = [""]
        self._undo_stack: List[TextOperation] = []
        self._redo_stack: List[TextOperation] = []

    def get_content(self) -> str:
        """获取缓冲区内容"""
        return "\n".join(self._content)

    def set_content(self, content: str) -> None:
        """设置缓冲区内容"""
        self._content = content.split("\n")
        self._undo_stack.clear()
        self._redo_stack.clear()
        self.contentChanged.emit()

    def get_line(self, line: int) -> str:
        """获取指定行内容"""
        if 0 <= line < len(self._content):
            return self._content[line]
        return ""

    def get_line_count(self) -> int:
        """获取总行数"""
        return len(self._content)

    def insert(self, position: Position, text: str) -> None:
        """插入文本"""
        operation = InsertOperation(position, text)
        self._execute_operation(operation)

    def delete(self, start: Position, end: Position) -> None:
        """删除文本"""
        # 获取要删除的文本
        deleted_text = self._get_text(start, end)
        operation = DeleteOperation(start, end, deleted_text)
        self._execute_operation(operation)

    def _get_text(self, start: Position, end: Position) -> str:
        """获取指定范围的文本"""
        if start.line == end.line:
            # 单行
            line = self._content[start.line]
            return line[start.column : end.column]
        else:
            # 多行
            lines = []
            # 第一行
            first_line = self._content[start.line][start.column :]
            lines.append(first_line)

            # 中间行
            for line in range(start.line + 1, end.line):
                lines.append(self._content[line])

            # 最后一行
            last_line = self._content[end.line][: end.column]
            if last_line:
                lines.append(last_line)

            return "\n".join(lines)

    def _execute_operation(self, operation: TextOperation) -> None:
        """执行操作"""
        operation.apply(self)
        self._undo_stack.append(operation)
        self._redo_stack.clear()
        self.contentChanged.emit()

    def undo(self) -> None:
        """撤销操作"""
        if not self._undo_stack:
            return

        operation = self._undo_stack.pop()
        operation.revert(self)
        self._redo_stack.append(operation)
        self.contentChanged.emit()

    def redo(self) -> None:
        """重做操作"""
        if not self._redo_stack:
            return

        operation = self._redo_stack.pop()
        operation.apply(self)
        self._undo_stack.append(operation)
        self.contentChanged.emit()
