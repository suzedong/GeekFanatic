"""
主题管理器模块
"""
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtCore import QObject, Property, Signal, Slot

class ThemeType(Enum):
    """主题类型枚举"""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high-contrast"

class Theme:
    """主题配置类"""
    
    def __init__(self, name: str, type: ThemeType, colors: Dict[str, str]) -> None:
        """初始化主题"""
        self.name = name
        self.type = type
        self.colors = colors
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Theme':
        """从字典创建主题实例"""
        return cls(
            name=data['name'],
            type=ThemeType(data['type']),
            colors=data['colors']
        )

class ThemeManager(QObject):
    """主题管理器，负责管理主题和颜色方案"""
    
    # 信号定义
    themeChanged = Signal(str)          # 主题改变信号
    colorSchemeChanged = Signal(dict)   # 颜色方案改变信号
    
    def __init__(self) -> None:
        """初始化主题管理器"""
        super().__init__()
        self._themes: Dict[str, Theme] = {}
        self._current_theme: Optional[Theme] = None
        self._load_builtin_themes()
        
    def _load_builtin_themes(self) -> None:
        """加载内置主题"""
        # 默认深色主题
        dark_theme = Theme(
            name="Dark Modern",
            type=ThemeType.DARK,
            colors={
                "editor.background": "#1e1e1e",
                "editor.foreground": "#d4d4d4",
                "activityBar.background": "#333333",
                "activityBar.foreground": "#ffffff",
                "sideBar.background": "#252526",
                "sideBar.foreground": "#cccccc",
                "statusBar.background": "#007acc",
                "statusBar.foreground": "#ffffff",
                "titleBar.activeBackground": "#3c3c3c",
                "titleBar.activeForeground": "#cccccc",
            }
        )
        self._themes[dark_theme.name] = dark_theme
        
        # 默认浅色主题
        light_theme = Theme(
            name="Light Modern",
            type=ThemeType.LIGHT,
            colors={
                "editor.background": "#ffffff",
                "editor.foreground": "#000000",
                "activityBar.background": "#2c2c2c",
                "activityBar.foreground": "#ffffff",
                "sideBar.background": "#f3f3f3",
                "sideBar.foreground": "#333333",
                "statusBar.background": "#007acc",
                "statusBar.foreground": "#ffffff",
                "titleBar.activeBackground": "#dddddd",
                "titleBar.activeForeground": "#333333",
            }
        )
        self._themes[light_theme.name] = light_theme
        
        # 设置默认主题
        self.set_theme("Dark Modern")
        
    @Property(str)
    def current_theme(self) -> str:
        """获取当前主题名称"""
        return self._current_theme.name if self._current_theme else ""
        
    @Slot(str)
    def set_theme(self, theme_name: str) -> None:
        """设置当前主题"""
        if theme_name in self._themes:
            self._current_theme = self._themes[theme_name]
            self.themeChanged.emit(theme_name)
            self.colorSchemeChanged.emit(self._current_theme.colors)
            
    @Slot(result=list)
    def get_available_themes(self) -> List[str]:
        """获取可用主题列表"""
        return list(self._themes.keys())
        
    @Slot(str, result=dict)
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """获取主题的颜色方案"""
        theme = self._themes.get(theme_name)
        return theme.colors if theme else {}
        
    def register_theme(self, theme: Theme) -> None:
        """注册新主题"""
        self._themes[theme.name] = theme
        
    @Slot(str, result=str)
    def get_color(self, color_id: str) -> str:
        """获取指定颜色值"""
        if self._current_theme and color_id in self._current_theme.colors:
            return self._current_theme.colors[color_id]
        return ""