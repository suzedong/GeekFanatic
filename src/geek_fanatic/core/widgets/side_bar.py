"""
侧边栏实现
"""

from typing import Dict, Optional
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QSizePolicy
)

class SideBar(QWidget):
    """侧边栏，用于显示插件的辅助功能区域"""

    # 视图变更信号
    viewChanged = Signal(str)  # 视图ID

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化侧边栏

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

        # 视图堆栈
        self._stack = QStackedWidget()
        self._stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._layout.addWidget(self._stack)
        
        # 设置样式
        self.setStyleSheet("""
            SideBar {
                background: #252526;
                border-right: 1px solid #1e1e1e;
            }
            QStackedWidget {
                background: #252526;
            }
        """)

    def clear(self) -> None:
        """清除所有视图"""
        # 移除所有视图
        while self._stack.count():
            self._stack.removeWidget(self._stack.widget(0))
        self._current_views.clear()
        self._current_view_id = None

    def add_view(self, view: QWidget, view_id: str) -> None:
        """添加视图

        Args:
            view: 要添加的视图
            view_id: 视图ID
        """
        print(f"添加视图: {view_id}")
        if view_id not in self._current_views:
            index = self._stack.addWidget(view)
            self._current_views[view_id] = view
            print(f"添加视图到索引: {index}")

            # 如果是第一个视图，设置为当前视图
            if not self._current_view_id:
                print(f"设置为当前视图: {view_id}")
                self.set_current_view(view_id)

    def set_current_view(self, view_id: str) -> None:
        """设置当前视图

        Args:
            view_id: 视图ID
        """
        print(f"尝试设置当前视图: {view_id}")
        print(f"可用视图: {list(self._current_views.keys())}")
        
        if view_id in self._current_views:
            view = self._current_views[view_id]
            self._stack.setCurrentWidget(view)
            self._current_view_id = view_id
            self.viewChanged.emit(view_id)
            print(f"当前视图已设置为: {view_id}")
            print(f"堆栈当前索引: {self._stack.currentIndex()}")
            print(f"堆栈总数: {self._stack.count()}")
        else:
            print(f"未找到视图: {view_id}")

    def get_current_view(self) -> Optional[QWidget]:
        """获取当前视图

        Returns:
            Optional[QWidget]: 当前视图，如果没有则返回None
        """
        if self._current_view_id:
            return self._current_views.get(self._current_view_id)
        return None

    def remove_view(self, view_id: str) -> None:
        """移除视图

        Args:
            view_id: 视图ID
        """
        if view_id in self._current_views:
            view = self._current_views[view_id]
            self._stack.removeWidget(view)
            del self._current_views[view_id]

            # 如果移除的是当前视图，切换到其他视图
            if view_id == self._current_view_id:
                self._current_view_id = None
                if self._current_views:
                    next_view_id = next(iter(self._current_views))
                    self.set_current_view(next_view_id)