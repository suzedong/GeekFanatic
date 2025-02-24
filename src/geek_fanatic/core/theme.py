"""
主题系统实现
"""

from typing import Dict, List, Optional, Any

# pylint: disable=no-name-in-module,import-error
import PySide6.QtCore
from PySide6.QtCore import QObject

class ThemeManager(QObject):
    """主题管理器"""

    def __init__(self) -> None:
        """初始化主题管理器

        初始化主题管理器实例，设置内部存储结构。
        """
        super().__init__()
        self._themes: Dict[str, Dict[str, Any]] = {}
        self._current_theme: Optional[str] = None

    def register_theme(self, theme_id: str, theme_data: Dict[str, Any]) -> None:
        """注册主题
        
        Args:
            theme_id: 主题ID
            theme_data: 主题数据
        """
        self._themes[theme_id] = theme_data

    def unregister_theme(self, theme_id: str) -> None:
        """注销主题
        
        Args:
            theme_id: 要注销的主题ID
        """
        if theme_id in self._themes:
            del self._themes[theme_id]

    def set_theme(self, theme_id: str) -> bool:
        """设置当前主题
        
        Args:
            theme_id: 要设置的主题ID
            
        Returns:
            bool: 设置是否成功
        """
        if theme_id in self._themes:
            self._current_theme = theme_id
            return True
        return False

    def get_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """获取主题数据
        
        Args:
            theme_id: 主题ID
            
        Returns:
            Optional[Dict[str, Any]]: 主题数据，如果主题不存在则返回None
        """
        return self._themes.get(theme_id)

    def get_current_theme(self) -> Optional[Dict[str, Any]]:
        """获取当前主题
        
        Returns:
            Optional[Dict[str, Any]]: 当前主题数据，如果未设置主题则返回None
        """
        if self._current_theme:
            return self._themes.get(self._current_theme)
        return None

    @property
    def current_theme_id(self) -> Optional[str]:
        """获取当前主题ID
        
        Returns:
            Optional[str]: 当前主题ID，如果未设置主题则返回None
        """
        return self._current_theme

    @property
    def available_themes(self) -> List[str]:
        """获取所有可用的主题ID列表
        
        Returns:
            List[str]: 主题ID列表
        """
        return list(self._themes.keys())
