"""
编辑器基类实现
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit


class Editor(QPlainTextEdit):
    """编辑器控件基类"""

    # 定义信号
    cursorPositionChanged = Signal(int, int)  # 行号，列号

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_editor()

    def _setup_editor(self):
        """初始化编辑器"""
        # 设置字体
        font = QFont()
        font.setFamilies(["Monaco"])
        font.setPointSize(14)
        font.setFixedPitch(True)
        self.setFont(font)

        # 设置其他属性
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setBackgroundVisible(False)
        self.setTabStopDistance(40)

        # 连接信号
        self.cursorPositionChanged.connect(self._handle_cursor_position_changed)

    def _handle_cursor_position_changed(self):
        """处理光标位置变化"""
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        self.cursorPositionChanged.emit(line, column)