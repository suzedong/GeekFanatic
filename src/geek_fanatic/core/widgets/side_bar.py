"""
侧边栏组件实现
"""

from typing import Dict, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QLabel
)

class SideBarView(QWidget):
    """侧边栏视图基类"""

    def __init__(self, view_id: str, title: str, parent: Optional[QWidget] = None) -> None:
        """初始化侧边栏视图

        Args:
            view_id: 视图唯一标识
            title: 视图标题
            parent: 父组件
        """
        super().__init__(parent)
        self.view_id = view_id
        self.title = title
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                padding: 5px 10px;
                background: #252526;
                border-bottom: 1px solid #1E1E1E;
            }
        """)
        layout.addWidget(title_label)
        
        # 内容区域
        self._content = QWidget()
        layout.addWidget(self._content)

    @property
    def content_widget(self) -> QWidget:
        """获取内容区域组件"""
        return self._content

class SideBar(QWidget):
    """侧边栏组件
    
    提供类似 VSCode 侧边栏的功能，包括：
    - 多视图切换
    - 视图标题显示
    - 视图内容区域
    """

    # 信号定义
    viewChanged = Signal(str)  # 视图切换信号，参数为视图ID

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化侧边栏"""
        super().__init__(parent)
        self._views: Dict[str, SideBarView] = {}
        self._current_view: Optional[str] = None
        
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self) -> None:
        """设置UI"""
        # 创建主布局
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # 创建视图容器
        self._stack = QStackedWidget()
        self._layout.addWidget(self._stack)

    def _setup_style(self) -> None:
        """设置样式"""
        self.setStyleSheet("""
            SideBar {
                background: #252526;
                border-right: 1px solid #1E1E1E;
            }
        """)

    def add_view(self, view: SideBarView) -> None:
        """添加视图

        Args:
            view: 要添加的视图
        """
        if view.view_id in self._views:
            return

        self._views[view.view_id] = view
        self._stack.addWidget(view)

        # 如果是第一个视图，设置为当前视图
        if len(self._views) == 1:
            self.set_current_view(view.view_id)

    def remove_view(self, view_id: str) -> None:
        """移除视图

        Args:
            view_id: 要移除的视图ID
        """
        if view_id not in self._views:
            return

        view = self._views.pop(view_id)
        self._stack.removeWidget(view)

        # 如果移除的是当前视图，切换到其他视图
        if self._current_view == view_id:
            next_view = next(iter(self._views)) if self._views else None
            if next_view:
                self.set_current_view(next_view)
            self._current_view = None

    def set_current_view(self, view_id: str) -> None:
        """设置当前视图

        Args:
            view_id: 视图ID
        """
        if view_id not in self._views:
            return

        view = self._views[view_id]
        self._stack.setCurrentWidget(view)
        self._current_view = view_id
        self.viewChanged.emit(view_id)

    def get_current_view(self) -> Optional[str]:
        """获取当前视图ID"""
        return self._current_view

    def get_view(self, view_id: str) -> Optional[SideBarView]:
        """获取指定视图

        Args:
            view_id: 视图ID

        Returns:
            Optional[SideBarView]: 视图实例，如果不存在则返回None
        """
        return self._views.get(view_id)