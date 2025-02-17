"""
窗口管理系统实现
"""

from typing import Dict, List, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow


class WindowManager(QObject):
    """窗口管理器"""

    def __init__(self):
        """初始化窗口管理器"""
        super().__init__()
        self._windows: Dict[str, QMainWindow] = {}
        self._active_window: Optional[QMainWindow] = None
        self._window_state: str = "normal"

    def register_window(self, window_id: str, window: QMainWindow) -> None:
        """注册窗口"""
        self._windows[window_id] = window

    def unregister_window(self, window_id: str) -> None:
        """注销窗口"""
        if window_id in self._windows:
            del self._windows[window_id]

    def get_window(self, window_id: str) -> Optional[QMainWindow]:
        """获取窗口"""
        return self._windows.get(window_id)

    def get_active_window(self) -> Optional[QMainWindow]:
        """获取活动窗口"""
        return self._active_window

    def set_active_window(self, window: QMainWindow) -> None:
        """设置活动窗口"""
        self._active_window = window

    def get_window_state(self) -> str:
        """获取窗口状态"""
        return self._window_state

    def set_window_state(self, state: str) -> None:
        """设置窗口状态"""
        self._window_state = state

    def get_all_windows(self) -> List[QMainWindow]:
        """获取所有窗口"""
        return list(self._windows.values())
