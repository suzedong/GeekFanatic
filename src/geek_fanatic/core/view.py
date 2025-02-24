"""
视图系统实现
"""

from enum import Enum
from typing import Dict, List, Union, TypedDict, Optional

# pylint: disable=no-name-in-module
from PySide6 import QtWidgets

ViewComponent = Union["QtWidgets.QWidget", str]

class ViewType(str, Enum):
    """视图类型"""
    WIDGET = "widget"  # Qt Widgets
    QML = "qml"  # QML

class ViewInfo(TypedDict):
    """视图信息类型"""
    id: str
    title: str
    component: ViewComponent
    type: ViewType
    icon: str
    priority: int

class ViewRegistry:
    """视图注册表"""

    def __init__(self) -> None:
        """初始化视图注册表"""
        self._views: Dict[str, ViewInfo] = {}

    def register_view(
        self,
        view_id: str,
        title: str,
        component: ViewComponent,
        view_type: ViewType = ViewType.WIDGET,
        icon: str = "",
        priority: int = 0,
    ) -> bool:
        """注册视图

        Args:
            view_id: 视图唯一标识
            title: 视图标题
            component: 视图组件
                - QWidget: Qt Widgets视图
                - str: QML文件路径
            view_type: 视图类型
            icon: 图标路径
            priority: 优先级

        Returns:
            bool: 注册是否成功
        """
        if view_id in self._views:
            return False

        # 验证参数
        if not isinstance(view_id, str) or not view_id.strip():
            return False

        if not isinstance(title, str) or not title.strip():
            return False

        # 验证组件类型
        try:
            if view_type == ViewType.WIDGET:
                if not isinstance(component, QtWidgets.QWidget):
                    return False
            elif view_type == ViewType.QML:
                if not isinstance(component, str):
                    return False
            else:
                return False

            self._views[view_id] = ViewInfo(
                id=view_id,
                title=title,
                component=component,
                type=view_type,
                icon=icon,
                priority=priority
            )
            return True
        except Exception:
            return False

    def unregister_view(self, view_id: str) -> bool:
        """注销视图

        Args:
            view_id: 视图ID

        Returns:
            bool: 注销是否成功
        """
        return bool(self._views.pop(view_id, None))

    def get_view(self, view_id: str) -> Optional[ViewInfo]:
        """获取视图信息

        Args:
            view_id: 视图ID

        Returns:
            Optional[ViewInfo]: 视图信息，如果不存在则返回 None
        """
        return self._views.get(view_id)

    def get_sorted_views(self) -> List[ViewInfo]:
        """获取所有视图（按优先级排序）

        Returns:
            List[ViewInfo]: 按优先级降序排列的视图列表
        """
        return sorted(
            self._views.values(),
            key=lambda x: x["priority"],
            reverse=True
        )

    def get_widget_views(self) -> List[ViewInfo]:
        """获取所有 Widget 类型的视图

        Returns:
            List[ViewInfo]: Widget 类型的视图列表
        """
        return [
            view for view in self._views.values()
            if view["type"] == ViewType.WIDGET
        ]

    def get_qml_views(self) -> List[ViewInfo]:
        """获取所有 QML 类型的视图

        Returns:
            List[ViewInfo]: QML 类型的视图列表
        """
        return [
            view for view in self._views.values()
            if view["type"] == ViewType.QML
        ]

    def update_view_priority(self, view_id: str, priority: int) -> bool:
        """更新视图优先级

        Args:
            view_id: 视图ID
            priority: 新的优先级

        Returns:
            bool: 更新是否成功
        """
        view = self._views.get(view_id)
        if view is None:
            return False

        try:
            view["priority"] = priority
            return True
        except Exception:
            return False

    def clear(self) -> None:
        """清空所有视图"""
        self._views.clear()

    def get_view_component(self, view_id: str) -> Optional[ViewComponent]:
        """获取视图组件

        Args:
            view_id: 视图ID

        Returns:
            Optional[ViewComponent]: 视图组件，如果不存在则返回 None
        """
        view = self.get_view(view_id)
        return view["component"] if view else None
