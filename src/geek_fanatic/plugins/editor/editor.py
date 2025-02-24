#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编辑器核心实现模块
"""

from typing import Dict, Optional, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

from .buffer import TextBuffer
from .types import Position

class Editor(QWidget):
    """编辑器核心类
    
    提供基础的文本编辑功能。
    """

    # 信号定义
    contentChanged = Signal()  # 内容变更信号
    selectionChanged = Signal()  # 选择变更信号
    cursorPositionChanged = Signal(int, int)  # 光标位置变更信号

    def __init__(self) -> None:
        """初始化编辑器"""
        super().__init__()
        self._buffer = TextBuffer()  # 文本缓冲区
        self._cursor_position = Position(0, 0)  # 当前光标位置
        self._selection_start: Optional[Position] = None  # 选择起始位置
        self._selection_end: Optional[Position] = None  # 选择结束位置
        
        # 创建UI
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self._text_edit = QPlainTextEdit()
        self._text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        layout.addWidget(self._text_edit)

        # 设置样式
        self._text_edit.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                selection-background-color: #264f78;
                selection-color: #ffffff;
                font-family: 'Consolas';
                font-size: 14px;
                border: none;
            }
        """)

    def _connect_signals(self) -> None:
        """连接信号"""
        self._text_edit.textChanged.connect(self._on_text_changed)
        self._text_edit.selectionChanged.connect(self._on_selection_changed)
        self._text_edit.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def _on_text_changed(self) -> None:
        """处理文本变更"""
        self._buffer.set_content(self._text_edit.toPlainText())
        self.contentChanged.emit()

    def _on_selection_changed(self) -> None:
        """处理选择变更"""
        cursor = self._text_edit.textCursor()
        if cursor.hasSelection():
            start_pos = self._get_position(cursor.selectionStart())
            end_pos = self._get_position(cursor.selectionEnd())
            if start_pos and end_pos:
                self._selection_start = start_pos
                self._selection_end = end_pos
        else:
            self._selection_start = None
            self._selection_end = None
        self.selectionChanged.emit()

    def _on_cursor_position_changed(self) -> None:
        """处理光标位置变更"""
        cursor = self._text_edit.textCursor()
        block = cursor.block()
        line = block.blockNumber()
        column = cursor.positionInBlock()
        self._cursor_position = Position(line, column)
        self.cursorPositionChanged.emit(line, column)

    def _get_position(self, index: int) -> Optional[Position]:
        """从文本索引获取位置"""
        if index < 0:
            return None
            
        text = self._text_edit.toPlainText()
        if index > len(text):
            return None
            
        # 计算行号和列号
        text_before = text[:index]
        line = text_before.count('\n')
        if line == 0:
            return Position(0, index)
            
        last_newline = text_before.rindex('\n')
        column = index - last_newline - 1
        return Position(line, column)

    # 公共接口
    def setPlainText(self, text: str) -> None:
        """设置文本内容"""
        self._text_edit.setPlainText(text)

    def clear(self) -> None:
        """清空内容"""
        self._text_edit.clear()

    @property
    def content(self) -> str:
        """获取编辑器内容"""
        return self._buffer.get_content()

    @content.setter
    def content(self, text: str) -> None:
        """设置编辑器内容"""
        self._text_edit.setPlainText(text)

    def get_cursor_position(self) -> Position:
        """获取光标位置"""
        return self._cursor_position

    def set_cursor_position(self, position: Position) -> None:
        """设置光标位置"""
        cursor = self._text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        for _ in range(position.line):
            cursor.movePosition(QTextCursor.NextBlock)
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, position.column)
        self._text_edit.setTextCursor(cursor)

    def has_selection(self) -> bool:
        """是否有选中内容"""
        return self._text_edit.textCursor().hasSelection()

    def get_selection(self) -> Optional[Tuple[Position, Position]]:
        """获取选中区域"""
        if not self.has_selection():
            return None
        if self._selection_start is None or self._selection_end is None:
            return None
        return (self._selection_start, self._selection_end)

    def clear_selection(self) -> None:
        """清除选中区域"""
        cursor = self._text_edit.textCursor()
        cursor.clearSelection()
        self._text_edit.setTextCursor(cursor)

    def insert_text(self, text: str) -> None:
        """插入文本"""
        self._text_edit.insertPlainText(text)

    def delete_at_cursor(self) -> None:
        """在光标位置删除字符"""
        cursor = self._text_edit.textCursor()
        cursor.deletePreviousChar()

    def delete_selection(self) -> None:
        """删除选中内容"""
        if not self.has_selection():
            return
        selection = self.get_selection()
        if selection is None:
            return
        start, end = selection
        self._buffer.delete(start, end)
        cursor = self._text_edit.textCursor()
        cursor.removeSelectedText()

    def undo(self) -> None:
        """撤销操作"""
        self._text_edit.undo()

    def redo(self) -> None:
        """重做操作"""
        self._text_edit.redo()
