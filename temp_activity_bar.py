from typing import List, Optional

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem
)

class ActivityBarItem(QPushButton):
    """活动栏项目"""

    def __init__(
        self,
        icon: QIcon,
        tooltip: str,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        # 创建 SVG 渲染器
        self._svg_renderer = QSvgRenderer()
        svg_data = QByteArray('''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24">
    <path fill="#CCCCCC" d="M3 3h18v18H3V3m2 2v14h14V5H5z"/>
    <path fill="#CCCCCC" d="M7 7h10v10H7V7m2 2v6h6V9H9z"/>
</svg>

'''.encode('utf-8'))
        self._svg_renderer.load(svg_data)

        # 设置按钮属性
        self.setCheckable(True)
        self.setFixedSize(48, 48)
        self.setToolTip(tooltip)
        
        # 设置样式
        self.setStyleSheet('''
            QPushButton {
                border: none;
                background: transparent;
                padding: 10px;
                border-left: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-left: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.2);
                border-left: 2px solid white;
            }
        ''')

    def paintEvent(self, event):
        """重写绘制事件以自定义图标渲染"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        size = QSize(24, 24)
        x = (self.width() - size.width()) // 2
        y = (self.height() - size.height()) // 2
        self._svg_renderer.render(painter, QRect(x, y, size.width(), size.height()))
        painter.end()

class ActivityBar(QWidget):
    # ... Rest of your code
