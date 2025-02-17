"""
视图系统实现
"""

from enum import Enum
from typing import Any, Dict, List, Union

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget


class ViewType(str, Enum):
    """视图类型"""

    WIDGET = "widget"  # Qt Widgets
    QML = "qml"  # QML


class ViewRegistry(QObject):
    """视图注册表"""

    def __init__(self):
        """初始化视图注册表"""
        super().__init__()
        self._views: Dict[str, Dict] = {}

    def register_view(
        self,
        view_id: str,
        title: str,
        component: Union[QWidget, str],
        view_type: ViewType = ViewType.WIDGET,
        icon: str = "",
        priority: int = 0,
    ) -> None:
        """
        注册视图

        Args:
            view_id: 视图唯一标识
            title: 视图标题
            component: 视图组件
                - QWidget: Qt Widgets视图
                - str: QML文件路径
            view_type: 视图类型
            icon: 图标
            priority: 优先级
        """
        self._views[view_id] = {
            "id": view_id,
            "title": title,
            "component": component,
            "type": view_type,
            "icon": icon,
            "priority": priority,
        }

    def unregister_view(self, view_id: str) -> None:
        """注销视图"""
        if view_id in self._views:
            del self._views[view_id]

    def get_view(self, view_id: str) -> Dict[str, Any]:
        """获取视图信息"""
        return self._views.get(view_id, {})

    def get_sorted_views(self) -> List[Dict[str, Any]]:
        """获取所有视图（按优先级排序）"""
        views = list(self._views.values())
        return sorted(views, key=lambda x: x["priority"], reverse=True)
