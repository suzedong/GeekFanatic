"""
活动栏组件实现
"""

from typing import List, Optional

from PySide6.QtCore import Qt, Signal, QSize, QByteArray
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem
)

from geek_fanatic.resources.icons import (
    EXPLORER_SVG, SEARCH_SVG, GIT_SVG,
    DEBUG_SVG, EXTENSIONS_SVG, SETTINGS_SVG
)

def create_icon_from_svg(svg_content: str, size: int = 24) -> QIcon:
    """从 SVG 内容创建图标"""
    renderer = QSvgRenderer(QByteArray(svg_content.encode()))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

class ActivityBarItem(QPushButton):
    """活动栏项目"""

    def __init__(
        self,
        icon: QIcon,
        tooltip: str,
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化活动栏项目

        Args:
            icon: 图标
            tooltip: 提示文本
            parent: 父组件
        """
        super().__init__(parent)
        
        # 设置图标和提示
        if not icon.isNull():
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))
        self.setToolTip(tooltip)
        
        # 设置按钮属性
        self.setCheckable(True)
        self.setFixedSize(48, 48)
        self.setFlat(True)
        
        # 设置样式
        self.setStyleSheet("""
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
        """)

class ActivityBar(QWidget):
    """活动栏组件"""

    # 信号定义
    itemClicked = Signal(str)  # 项目点击信号，参数为项目ID

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化活动栏"""
        super().__init__(parent)
        self._items: List[ActivityBarItem] = []
        self._bottom_items: List[ActivityBarItem] = []
        self._active_item: Optional[ActivityBarItem] = None
        
        self._setup_ui()
        self._setup_style()
        self._setup_default_items()
    
    def _setup_default_items(self) -> None:
        """设置默认图标项目"""
        
        # 核心功能图标
        self.add_item(
            "explorer",
            create_icon_from_svg(EXPLORER_SVG),
            "文件资源管理器"
        )
        
        # 底部项目
        self.add_item(
            "settings",
            create_icon_from_svg(SETTINGS_SVG),
            "设置",
            bottom=True
        )
    
    def _setup_ui(self) -> None:
        """设置UI"""
        # 创建主布局
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        # 创建顶部和底部容器
        self._top_container = QWidget()
        self._bottom_container = QWidget()
        
        # 顶部布局
        self._top_layout = QVBoxLayout(self._top_container)
        self._top_layout.setContentsMargins(0, 0, 0, 0)
        self._top_layout.setSpacing(0)
        
        # 底部布局
        self._bottom_layout = QVBoxLayout(self._bottom_container)
        self._bottom_layout.setContentsMargins(0, 0, 0, 0)
        self._bottom_layout.setSpacing(0)
        
        # 添加弹性空间
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # 组装布局
        self._layout.addWidget(self._top_container)
        self._layout.addItem(spacer)
        self._layout.addWidget(self._bottom_container)
    
    def _setup_style(self) -> None:
        """设置样式"""
        self.setStyleSheet("""
            ActivityBar {
                background: #333333;
                min-width: 48px;
                max-width: 48px;
                border-right: 1px solid #252525;
            }
        """)
    
    def add_item(
        self,
        item_id: str,
        icon: QIcon,
        tooltip: str,
        bottom: bool = False
    ) -> None:
        """添加活动栏项目"""
        item = ActivityBarItem(icon, tooltip, self)
        item.setProperty("item_id", item_id)
        item.clicked.connect(lambda: self._on_item_clicked(item))
        
        if bottom:
            self._bottom_items.append(item)
            self._bottom_layout.addWidget(item)
        else:
            self._items.append(item)
            self._top_layout.addWidget(item)
            
        # 如果是第一个项目，设置为活动项
        if not self._active_item:
            self.set_active_item(item_id)
    
    def _on_item_clicked(self, item: ActivityBarItem) -> None:
        """处理项目点击事件"""
        if self._active_item and self._active_item != item:
            self._active_item.setChecked(False)
        
        self._active_item = item
        item_id = item.property("item_id")
        self.itemClicked.emit(item_id)
    
    def set_active_item(self, item_id: str) -> None:
        """设置活动项目"""
        for item in self._items + self._bottom_items:
            if item.property("item_id") == item_id:
                item.setChecked(True)
                self._active_item = item
            else:
                item.setChecked(False)
