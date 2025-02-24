"""
编辑器基类实现
"""

from typing import Optional, Tuple

# pylint: disable=no-name-in-module,import-error
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit, QWidget


class Editor(QPlainTextEdit):
    """编辑器控件基类"""

    # 定义信号
    cursorPositionChanged = Signal(int, int)  # 行号，列号

    # 默认字体设置
    DEFAULT_FONT_FAMILIES = ["Monaco", "Consolas", "Courier New"]
    DEFAULT_FONT_SIZE = 14
    DEFAULT_TAB_SIZE = 40

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化编辑器

        Args:
            parent: 父窗口部件
        """
        super().__init__(parent)
        self._setup_editor()

    def _setup_editor(self) -> None:
        """初始化编辑器"""
        # 设置字体
        self._setup_font()

        # 设置其他属性
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.setBackgroundVisible(False)
        self.setTabStopDistance(self.DEFAULT_TAB_SIZE)

        # 连接信号
        self.cursorPositionChanged.connect(self._handle_cursor_position_changed)

    def _setup_font(self) -> None:
        """设置编辑器字体

        尝试按优先顺序设置可用的等宽字体
        """
        font = QFont()
        
        # 尝试设置字体族
        for family in self.DEFAULT_FONT_FAMILIES:
            font.setFamily(family)
            if font.exactMatch():
                break

        # 设置字体大小和等宽属性
        font.setPointSize(self.DEFAULT_FONT_SIZE)
        font.setFixedPitch(True)
        
        self.setFont(font)

    def _handle_cursor_position_changed(self) -> None:
        """处理光标位置变化

        发送当前光标的行号和列号（从1开始计数）
        """
        try:
            cursor = self.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.positionInBlock() + 1
            self.cursorPositionChanged.emit(line, column)
        except Exception as e:
            # 在实际应用中，这里应该使用logger记录错误
            print(f"Error handling cursor position change: {e}")

    def set_font_size(self, size: int) -> None:
        """设置字体大小

        Args:
            size: 字体大小（点数）
        
        该函数会验证字体大小是否在合理范围内（8-72点）。
        如果大小无效，函数会静默返回而不做任何更改。
        """
        if size < 8 or size > 72:  # 添加合理的限制
            return
            
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    def set_tab_size(self, size: int) -> None:
        """设置制表符宽度

        Args:
            size: 制表符宽度（像素）

        该函数会验证宽度是否为正数。
        如果宽度无效，函数会静默返回而不做任何更改。
        """
        if size < 1:  # 确保宽度有效
            return
            
        self.setTabStopDistance(size)

    def get_cursor_position(self) -> Tuple[int, int]:
        """获取当前光标位置

        Returns:
            Tuple[int, int]: (行号, 列号)，均从1开始计数
        """
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        return line, column

    def set_cursor_position(self, line: int, column: int) -> bool:
        """设置光标位置

        Args:
            line: 目标行号（从1开始）
            column: 目标列号（从1开始）

        Returns:
            bool: 是否设置成功

        该函数尝试将光标移动到指定位置。如果位置无效或发生错误，
        将返回False并保持光标在原位置不变。
        """
        try:
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
            
            # 移动到指定行
            for _ in range(line - 1):
                if not cursor.movePosition(QtGui.QTextCursor.MoveOperation.NextBlock):
                    return False
            
            # 移动到指定列
            for _ in range(column - 1):
                if not cursor.movePosition(QtGui.QTextCursor.MoveOperation.Right):
                    return False
                    
            self.setTextCursor(cursor)
            return True
            
        except Exception:
            return False

    def get_line_count(self) -> int:
        """获取总行数

        Returns:
            int: 文档的总行数
        """
        return self.document().blockCount()

    def get_line_text(self, line: int) -> Optional[str]:
        """获取指定行的文本内容

        Args:
            line: 行号（从1开始）

        Returns:
            Optional[str]: 行文本内容，如果行号无效则返回 None
        """
        if line < 1 or line > self.get_line_count():
            return None
            
        block = self.document().findBlockByNumber(line - 1)
        return block.text() if block.isValid() else None
