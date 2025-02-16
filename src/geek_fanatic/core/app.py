"""
GeekFanatic 核心应用模块
"""
from typing import Dict, List, Optional, Type

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QQmlEngine, qmlRegisterType

from geek_fanatic.core.plugin import Plugin, PluginManager
from geek_fanatic.core.theme import ThemeManager
from geek_fanatic.core.window import WindowManager


class GeekFanatic(QObject):
    """核心类，管理整个应用程序的生命周期和核心功能"""

    # 信号定义
    themeChanged = Signal(str)  # 主题变更信号
    windowStateChanged = Signal(str)  # 窗口状态变更信号
    pluginLoaded = Signal(str)  # 插件加载信号
    
    def __init__(self) -> None:
        """初始化应用程序核心实例"""
        super().__init__()
        
        # 初始化核心管理器
        self._plugin_manager = PluginManager()
        self._theme_manager = ThemeManager()
        self._window_manager = WindowManager()
        
        # 插件注册表
        self._plugins: Dict[str, Plugin] = {}
        
    def register_types(self) -> None:
        """注册Python类型到QML"""
        # 注册核心类型
        qmlRegisterType(GeekFanatic, 'GeekFanatic.Core', 1, 0, 'IDE')
        qmlRegisterType(WindowManager, 'GeekFanatic.Core', 1, 0, 'WindowManager')
        qmlRegisterType(ThemeManager, 'GeekFanatic.Core', 1, 0, 'ThemeManager')
        
        # 注册插件提供的类型
        for plugin in self._plugins.values():
            plugin.register_types()
    
    def initialize_plugins(self) -> None:
        """初始化插件系统"""
        # 扫描并加载插件
        discovered_plugins = self._plugin_manager.discover_plugins()
        for plugin_class in discovered_plugins:
            self._load_plugin(plugin_class)
    
    def _load_plugin(self, plugin_class: Type[Plugin]) -> None:
        """加载单个插件"""
        plugin = plugin_class(self)
        plugin_id = plugin.id
        
        if plugin_id in self._plugins:
            return
            
        self._plugins[plugin_id] = plugin
        plugin.initialize()
        self.pluginLoaded.emit(plugin_id)
    
    @Slot(str)
    def set_theme(self, theme_name: str) -> None:
        """设置主题"""
        self._theme_manager.set_theme(theme_name)
        self.themeChanged.emit(theme_name)
    
    @Slot(str)
    def set_window_state(self, state: str) -> None:
        """设置窗口状态"""
        self._window_manager.set_window_state(state)
        self.windowStateChanged.emit(state)
    
    @Slot(str, result=bool)
    def is_plugin_loaded(self, plugin_id: str) -> bool:
        """检查插件是否已加载"""
        return plugin_id in self._plugins
    
    @Slot(str, result=str)
    def get_plugin_info(self, plugin_id: str) -> str:
        """获取插件信息"""
        if plugin_id in self._plugins:
            plugin = self._plugins[plugin_id]
            return f"{plugin.name} (v{plugin.version})"
        return ""
    
    @property
    def plugin_manager(self) -> PluginManager:
        """获取插件管理器"""
        return self._plugin_manager
    
    @property
    def theme_manager(self) -> ThemeManager:
        """获取主题管理器"""
        return self._theme_manager
    
    @property
    def window_manager(self) -> WindowManager:
        """获取窗口管理器"""
        return self._window_manager