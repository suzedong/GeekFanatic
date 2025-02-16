"""
窗口管理器模块
"""
from enum import Enum
from typing import Dict, Optional

from PySide6.QtCore import QObject, Property, Signal, Slot

class WindowState(Enum):
    """窗口状态枚举"""
    NORMAL = "normal"
    MAXIMIZED = "maximized"
    MINIMIZED = "minimized"
    FULLSCREEN = "fullscreen"

class WindowManager(QObject):
    """窗口管理器，负责管理窗口状态和布局"""
    
    # 信号定义
    stateChanged = Signal(str)  # 窗口状态改变信号
    layoutChanged = Signal()    # 布局改变信号
    
    def __init__(self) -> None:
        """初始化窗口管理器"""
        super().__init__()
        self._window_state = WindowState.NORMAL
        self._layout_config: Dict[str, float] = {
            "sidebar_width": 300,
            "panel_height": 200,
            "editor_tabs_height": 35,
        }
        
    @Property(str)
    def window_state(self) -> str:
        """获取当前窗口状态"""
        return self._window_state.value
        
    @window_state.setter
    def window_state(self, state: str) -> None:
        """设置窗口状态"""
        try:
            new_state = WindowState(state)
            if new_state != self._window_state:
                self._window_state = new_state
                self.stateChanged.emit(state)
        except ValueError:
            pass
            
    @Slot(str, float)
    def set_layout_size(self, component: str, size: float) -> None:
        """设置布局组件大小"""
        if component in self._layout_config and self._layout_config[component] != size:
            self._layout_config[component] = size
            self.layoutChanged.emit()
            
    @Slot(str, result=float)
    def get_layout_size(self, component: str) -> float:
        """获取布局组件大小"""
        return self._layout_config.get(component, 0.0)
        
    @Slot()
    def maximize(self) -> None:
        """最大化窗口"""
        self.window_state = WindowState.MAXIMIZED.value
        
    @Slot()
    def minimize(self) -> None:
        """最小化窗口"""
        self.window_state = WindowState.MINIMIZED.value
        
    @Slot()
    def restore(self) -> None:
        """还原窗口"""
        self.window_state = WindowState.NORMAL.value
        
    @Slot()
    def toggle_fullscreen(self) -> None:
        """切换全屏状态"""
        if self._window_state == WindowState.FULLSCREEN:
            self.window_state = WindowState.NORMAL.value
        else:
            self.window_state = WindowState.FULLSCREEN.value