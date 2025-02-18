"""
编辑器小部件实现
"""

from typing import List, Optional, Type, Any

# pylint: disable=no-name-in-module,import-error
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QKeyEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QResizeEvent,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

class Editor(QPlainTextEdit):
    """编辑器控件"""

    # 自定义信号
    cursorPositionChanged = Signal(int, int)  # 行号，列号

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化编辑器

        Args:
            parent: 父窗口部件
        """
        super().__init__(parent)
        # 获取 extraSelectionClass
        self._extra_selection_class = getattr(QPlainTextEdit, "ExtraSelection")
        self._setup_editor()

    def _setup_editor(self) -> None:
        """初始化编辑器"""
        # 设置字体
        font = QFont("Consolas", 14)
        font.setFixedPitch(True)
        self.setFont(font)

        # 设置制表符宽度（以像素为单位）
        metrics = self.fontMetrics()
        self.setTabStopDistance(4 * metrics.horizontalAdvance(" "))

        # 显示行号
        self._show_line_numbers: bool = True
        self._line_number_area_width: int = 50

        # 设置内边距，为行号区域留出空间
        self.setViewportMargins(self._line_number_area_width, 0, 0, 0)

        # 连接信号
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def line_number_area_width(self) -> int:
        """获取行号区域宽度

        Returns:
            行号区域的像素宽度
        """
        return self._line_number_area_width

    def paintEvent(self, event: QPaintEvent) -> None:
        """重写绘制事件，添加行号

        Args:
            event: 绘制事件对象
        """
        # 先调用父类的绘制
        super().paintEvent(event)

        if not self._show_line_numbers:
            return

        painter = QPainter(self.viewport())
        try:
            # 设置画笔
            no_pen = QPen()
            no_pen.setStyle(Qt.PenStyle.NoPen)
            painter.setPen(no_pen)

            # 绘制行号区域背景
            painter.fillRect(
                0,
                0,
                self._line_number_area_width,
                self.viewport().height(),
                QColor("#1e1e1e")
            )

            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            top = int(
                self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            )
            bottom = top + int(self.blockBoundingRect(block).height())

            # 设置行号颜色
            painter.setPen(QPen(QColor("#858585")))

            # 绘制所有可见行号
            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.drawText(
                        0,
                        top,
                        self._line_number_area_width - 5,
                        self.fontMetrics().height(),
                        int(Qt.AlignmentFlag.AlignRight),
                        number,
                    )

                block = block.next()
                top = bottom
                bottom = top + int(self.blockBoundingRect(block).height())
                block_number += 1

        finally:
            painter.end()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """重写调整大小事件

        Args:
            event: 调整大小事件对象
        """
        super().resizeEvent(event)
        # 调整滚动区域大小
        self.setViewportMargins(self._line_number_area_width, 0, 0, 0)

    def _on_cursor_position_changed(self) -> None:
        """处理光标位置变化"""
        cursor = self.textCursor()
        block = cursor.block()
        line = block.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        self.cursorPositionChanged.emit(line, column)

        # 高亮当前行
        self._highlight_current_line()

    def _highlight_current_line(self) -> None:
        """高亮当前行"""
        selections = []

        if not self.isReadOnly():
            extra_sel = self._extra_selection_class()
            text_format = QTextCharFormat()
            text_format.setBackground(QColor("#282828"))
            text_format.setProperty(
                QTextFormat.Property.FullWidthSelection,
                True
            )
            extra_sel.format = text_format
            extra_sel.cursor = self.textCursor()
            extra_sel.cursor.clearSelection()
            selections.append(extra_sel)

        self.setExtraSelections(selections)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """处理按键事件

        Args:
            event: 键盘事件对象
        """
        if event.key() == int(Qt.Key.Key_Tab):
            # 插入4个空格
            self.insertPlainText("    ")
            event.accept()
        else:
            super().keyPressEvent(event)
