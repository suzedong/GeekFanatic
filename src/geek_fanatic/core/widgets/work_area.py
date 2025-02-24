"""
工作区实现
"""

from typing import Dict, Optional
from PySide6.QtCore import Signal
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
        # 清除当前视图
        self.clear()

        # 添加新视图
        for view_id, view in views.items():
            if isinstance(view, QTabWidget):
                # 如果是标签页组，直接添加
                self._stack.addWidget(view)
                self._current_views[view_id] = view
            else:
                # 否则创建新的标签页组
                tab_widget = QTabWidget()
                tab_widget.setTabsClosable(True)
                tab_widget.setMovable(True)
                tab_widget.addTab(view, view.windowTitle() or "未命名")
                tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

                self._stack.addWidget(tab_widget)
                self._current_views[view_id] = tab_widget

        # 显示第一个视图
        if self._current_views:
            first_view_id = next(iter(self._current_views))
            self.set_current_view(first_view_id)

    def clear(self) -> None:
        """清除所有视图"""
        while self._stack.count():
            self._stack.removeWidget(self._stack.widget(0))
        self._current_views.clear()
        self._current_view_id = None

    def set_current_view(self, view_id: str) -> None:
        """设置当前视图

        Args:
            view_id: 视图ID
        """
        if view_id in self._current_views:
            view = self._current_views[view_id]
            self._stack.setCurrentWidget(view)
            self._current_view_id = view_id
            self.viewChanged.emit(view_id)

    def get_current_view(self) -> Optional[QWidget]:
        """获取当前视图

        Returns:
            Optional[QWidget]: 当前视图，如果没有则返回None
        """
        if self._current_view_id:
            return self._current_views.get(self._current_view_id)
        return None

    def add_tab(self, group_id: str, tab: WorkTab) -> None:
        """添加标签页到指定组

        Args:
            group_id: 标签页组ID
            tab: 标签页
        """
        if group_id in self._current_views:
            tab_widget = self._current_views[group_id]
            if isinstance(tab_widget, QTabWidget):
                tab_widget.addTab(tab, tab.title)
                tab_widget.setCurrentWidget(tab)

    def remove_tab(self, group_id: str, tab: WorkTab) -> None:
        """从指定组移除标签页

        Args:
            group_id: 标签页组ID
            tab: 标签页
        """
        if group_id in self._current_views:
            tab_widget = self._current_views[group_id]
            if isinstance(tab_widget, QTabWidget):
                index = tab_widget.indexOf(tab)
                if index != -1:
                    tab_widget.removeTab(index)

    def _on_tab_close_requested(self, index: int) -> None:
        """处理标签页关闭请求

        Args:
            index: 标签页索引
        """
        tab_widget = self.sender()
        if isinstance(tab_widget, QTabWidget):
            tab_widget.removeTab(index)