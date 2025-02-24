"""
工作区实现
"""

from typing import Dict, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QTabWidget
)

class WorkTab(QWidget):
    """工作区标签页"""

    def __init__(
        self, 
        id: str, 
        title: str, 
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化标签页

        Args:
            id: 标签页ID
            title: 标签页标题
            parent: 父widget
        """
        super().__init__(parent)
        self.id = id
        self.title = title
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置UI"""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

    @property
    def content_widget(self) -> QWidget:
        """获取内容区域widget"""
        return self

class WorkArea(QWidget):
    """工作区，用于显示插件的主要功能区域"""

    # 视图变更信号
    viewChanged = Signal(str)  # 视图ID

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化工作区

        Args:
            parent: 父widget
        """
        super().__init__(parent)
        self._current_views: Dict[str, QWidget] = {}  # 当前加载的视图
        self._current_view_id: Optional[str] = None   # 当前显示的视图ID
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置UI"""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # 主视图堆栈
        self._stack = QStackedWidget()
        self._layout.addWidget(self._stack)

    def switch_to_plugin_views(self, views: Dict[str, QWidget]) -> None:
        """切换到插件视图

        Args:
            views: 插件视图字典
        """
        # 如果已经显示了这些视图，不需要重新创建
        if all(view_id in self._current_views for view_id in views):
            return

        # 清除当前视图
        self.clear()

        # 创建新的标签页组
        tab_widget = QTabWidget()
        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

        # 添加视图到标签页
        for view_id, view in views.items():
            # 保存视图引用
            self._current_views[view_id] = view
            # 添加到标签页
            tab_widget.addTab(view, view.windowTitle() or "未命名")

        # 添加标签页组到堆栈
        self._stack.addWidget(tab_widget)
        self._stack.setCurrentWidget(tab_widget)

    def clear(self) -> None:
        """清除所有视图"""
        # 移除所有视图但不删除它们
        while self._stack.count():
            widget = self._stack.widget(0)
            self._stack.removeWidget(widget)
            widget.setParent(None)  # 取消父子关系但不删除

    def _on_tab_close_requested(self, index: int) -> None:
        """处理标签页关闭请求

        Args:
            index: 标签页索引
        """
        tab_widget = self._stack.currentWidget()
        if isinstance(tab_widget, QTabWidget):
            # 移除标签页但不删除视图
            widget = tab_widget.widget(index)
            tab_widget.removeTab(index)
            if widget:
                widget.setParent(None)  # 取消父子关系但不删除