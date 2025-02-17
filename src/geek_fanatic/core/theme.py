"""
主题系统实现
"""
from typing import Dict, Optional

from PySide6.QtCore import QObject


class ThemeManager(QObject):
    """主题管理器"""
    
    def __init__(self):
        """初始化主题管理器"""
        super().__init__()
        self._themes: Dict[str, Dict] = {}
        self._current_theme: Optional[str] = None
        
    def register_theme(self, theme_id: str, theme_data: Dict) -> None:
        """注册主题"""
        self._themes[theme_id] = theme_data
        
    def unregister_theme(self, theme_id: str) -> None:
        """注销主题"""
        if theme_id in self._themes:
            del self._themes[theme_id]
        
    def set_theme(self, theme_id: str) -> None:
        """设置当前主题"""
        if theme_id in self._themes:
            self._current_theme = theme_id
        
    def get_theme(self, theme_id: str) -> Optional[Dict]:
        """获取主题数据"""
        return self._themes.get(theme_id)
        
    def get_current_theme(self) -> Optional[Dict]:
        """获取当前主题"""
        if self._current_theme:
            return self._themes.get(self._current_theme)
        return None