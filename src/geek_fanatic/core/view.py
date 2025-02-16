"""
视图注册表实现
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union

from PySide6.QtCore import QObject, QUrl
from PySide6.QtWidgets import QWidget
from PySide6.QtQml import QQmlComponent

class ViewType(Enum):
    """视图类型"""
    WIDGET = "widget"  # QtWidgets 实现
    QML = "qml"       # QML 实现

class ViewRegistry:
    """视图注册表"""
    
    def __init__(self) -> None:
        """初始化视图注册表"""
        self._views: Dict[str, Dict[str, Any]] = {}
        
    def register_view(self,
                     view_id: str,
                     title: str,
                     component: Union[Type[QWidget], QUrl, str],
                     view_type: ViewType = ViewType.WIDGET,
                     icon: str = "",
                     priority: int = 0) -> None:
        """
        注册视图
        
        Args:
            view_id: 视图唯一标识
            title: 视图标题
            component: 视图组件
                - QWidget类型: 用于QtWidgets视图
                - QUrl/str类型: 用于QML视图，指向QML文件
            view_type: 视图类型(WIDGET/QML)
            icon: 图标
            priority: 优先级
        """
        # 处理QML路径
        if view_type == ViewType.QML and isinstance(component, str):
            component = QUrl(component)
            
        self._views[view_id] = {
            "id": view_id,
            "title": title,
            "component": component,
            "type": view_type,
            "icon": icon,
            "priority": priority
        }
        
    def get_view(self, view_id: str) -> Optional[Dict[str, Any]]:
        """获取视图信息"""
        return self._views.get(view_id)
        
    def get_views(self) -> Dict[str, Dict[str, Any]]:
        """获取所有视图"""
        return self._views
        
    def get_sorted_views(self) -> List[Dict[str, Any]]:
        """获取按优先级排序的视图列表"""
        return sorted(
            self._views.values(),
            key=lambda x: x["priority"],
            reverse=True
        )
        
    def unregister_view(self, view_id: str) -> None:
        """注销视图"""
        if view_id in self._views:
            del self._views[view_id]