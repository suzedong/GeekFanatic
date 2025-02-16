"""
GeekFanatic
一个模仿 Visual Studio Code 的现代化集成开发环境
"""

__version__ = "0.1.0"
__author__ = "GeekFanatic Team"
__description__ = "一个模仿 Visual Studio Code 的现代化集成开发环境"

# 导出核心类
from geek_fanatic.core.app import GeekFanatic
from geek_fanatic.core.plugin import Plugin, PluginManager
from geek_fanatic.core.theme import Theme, ThemeManager
from geek_fanatic.core.window import WindowManager

__all__ = [
    "GeekFanatic",
    "Plugin",
    "PluginManager",
    "Theme",
    "ThemeManager",
    "WindowManager",
]