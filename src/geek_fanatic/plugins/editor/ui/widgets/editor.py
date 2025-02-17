"""
编辑器小部件实现
"""

from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QKeyEvent,
    QPainter,
    QPen,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextFormat,
)
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget


class Editor(QPlainTextEdit):
    """编辑器控件"""

    # 自定义信号
    cursorPositionChanged = Signal(int, int)  # 行号，列号

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_editor()

    def _setup_editor(self):
        """初始化编辑器"""
        # 设置字体
        font = QFont("Consolas", 14)
        font.setFixedPitch(True)
        self.setFont(font)

        # 设置制表符宽度（以像素为单位）
        metrics = self.fontMetrics()
        self.setTabStopDistance(4 * metrics.horizontalAdvance(" "))

        # 显示行号
        self._show_line_numbers = True
        self._line_number_area_width = 50

        # 设置内边距，为行号区域留出空间
        self.setViewportMargins(self._line_number_area_width, 0, 0, 0)

        # 连接信号
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def line_number_area_width(self) -> int:
        """获取行号区域宽度"""
        return self._line_number_area_width

    def paintEvent(self, event):
        """重写绘制事件，添加行号"""
        # 先调用父类的绘制
        super().paintEvent(event)

        if self._show_line_numbers:
            painter = QPainter(self.viewport())
            painter.setPen(Qt.NoPen)

            # 绘制行号区域背景
            area_rect = QRect(
                0, 0, self._line_number_area_width, self.viewport().height()
            )
            painter.fillRect(area_rect, QColor("#1e1e1e"))

            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            top = (
                self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            )
            bottom = top + self.blockBoundingRect(block).height()

            painter.setPen(QColor("#858585"))

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.drawText(
                        0,
                        int(top),
                        self._line_number_area_width - 5,
                        self.fontMetrics().height(),
                        Qt.AlignRight,
                        number,
                    )

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1

            painter.end()

    def resizeEvent(self, event):
        """重写调整大小事件"""
        super().resizeEvent(event)
        # 调整滚动区域大小
        cr = self.contentsRect()
        self.setViewportMargins(self._line_number_area_width, 0, 0, 0)

    def _on_cursor_position_changed(self):
        """处理光标位置变化"""
        cursor = self.textCursor()
        block = cursor.block()
        line = block.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        self.cursorPositionChanged.emit(line, column)

        # 高亮当前行
        self._highlight_current_line()

    def _highlight_current_line(self):
        """高亮当前行"""
        extra_selections = []

        if not self.isReadOnly():
            selection = QPlainTextEdit.ExtraSelection()
            line_color = QColor("#282828")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """处理按键事件"""
        if event.key() == Qt.Key_Tab:
            # 插入4个空格
            self.insertPlainText("    ")
        else:
            super().keyPressEvent(event)
