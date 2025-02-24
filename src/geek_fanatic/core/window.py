"""
窗口管理系统实现
"""

from enum import Enum
from typing import Dict, List, Optional

# pylint: disable=no-name-in-module,import-error
from PySide6 import QtWidgets

class WindowState(str, Enum):
    """窗口状态枚举"""
    NORMAL = "normal"
    MAXIMIZED = "maximized"
    MINIMIZED = "minimized"
    FULLSCREEN = "fullscreen"

class WindowManager:
    """窗口管理器"""

    def __init__(self) -> None:
        """初始化窗口管理器"""
        self._windows: Dict[str, "QtWidgets.QMainWindow"] = {}
        self._active_window: Optional["QtWidgets.QMainWindow"] = None
        self._window_state: WindowState = WindowState.NORMAL

    def register_window(self, window_id: str, window: "QtWidgets.QMainWindow") -> bool:
        """注册窗口

        Args:
            window_id: 窗口ID
            window: 窗口实例

        Returns:
            bool: 是否注册成功
        """
        if window_id in self._windows:
            return False
        
        self._windows[window_id] = window
        
        # 如果这是第一个窗口，将其设置为活动窗口
        if len(self._windows) == 1:
            self.set_active_window(window)
            
        return True

    def unregister_window(self, window_id: str) -> bool:
        """注销窗口

        Args:
            window_id: 要注销的窗口ID

        Returns:
            bool: 是否注销成功
        """
        window = self._windows.pop(window_id, None)
        if window is None:
            return False
            
        # 如果注销的是活动窗口，重置活动窗口
        if window is self._active_window:
            next_window = next(iter(self._windows.values())) if self._windows else None
            self._active_window = next_window
            
        return True

    def get_window(self, window_id: str) -> Optional["QtWidgets.QMainWindow"]:
        """获取窗口

        Args:
            window_id: 窗口ID

        Returns:
            Optional[QtWidgets.QMainWindow]: 窗口实例，如果不存在则返回 None
        """
        return self._windows.get(window_id)

    def get_active_window(self) -> Optional["QtWidgets.QMainWindow"]:
        """获取活动窗口

        Returns:
            Optional[QtWidgets.QMainWindow]: 当前活动窗口，如果没有则返回 None
        """
        return self._active_window

    def set_active_window(self, window: "QtWidgets.QMainWindow") -> bool:
        """设置活动窗口

        Args:
            window: 要设置为活动的窗口

        Returns:
            bool: 是否设置成功
        """
        # 检查窗口是否在管理器中
        if not any(w is window for w in self._windows.values()):
            return False
            
        self._active_window = window
        window.activateWindow()
        return True

    def get_window_state(self) -> WindowState:
        """获取窗口状态

        Returns:
            WindowState: 当前窗口状态
        """
        return self._window_state

    def set_window_state(self, state: WindowState) -> None:
        """设置窗口状态

        Args:
            state: 要设置的窗口状态
        """
        self._window_state = state
        window = self.get_active_window()
        if window:
            if state == WindowState.MAXIMIZED:
                window.showMaximized()
            elif state == WindowState.MINIMIZED:
                window.showMinimized()
            elif state == WindowState.FULLSCREEN:
                window.showFullScreen()
            else:
                window.showNormal()

    def get_all_windows(self) -> List["QtWidgets.QMainWindow"]:
        """获取所有窗口

        Returns:
            List[QtWidgets.QMainWindow]: 所有窗口的列表
        """
        return list(self._windows.values())

    def get_window_by_id(self, window_id: str) -> Optional["QtWidgets.QMainWindow"]:
        """根据ID获取窗口

        Args:
            window_id: 窗口ID

        Returns:
            Optional[QtWidgets.QMainWindow]: 对应的窗口实例，如果不存在则返回 None
        """
        return self._windows.get(window_id)

    def get_window_id(self, window: "QtWidgets.QMainWindow") -> Optional[str]:
        """获取窗口的ID

        Args:
            window: 窗口实例

        Returns:
            Optional[str]: 窗口ID，如果不存在则返回 None
        """
        for window_id, win in self._windows.items():
            if win is window:
                return window_id
        return None

    def clear(self) -> None:
        """清除所有窗口"""
        self._windows.clear()
        self._active_window = None
        self._window_state = WindowState.NORMAL
