"""
GeekFanatic 核心应用模块
"""
from pathlib import Path
from typing import Dict, List, Optional, Type

from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtWidgets import QWidget
from PySide6.QtQml import QQmlComponent

from geek_fanatic.core.plugin import Plugin, PluginManager
from geek_fanatic.core.theme import ThemeManager
from geek_fanatic.core.window import WindowManager
from geek_fanatic.core.command import CommandRegistry
from geek_fanatic.core.config import ConfigRegistry
from geek_fanatic.core.view import ViewRegistry, ViewType

class GeekFanatic(QObject):
    """核心类，管理整个应用程序的生命周期和核心功能"""

    # 信号定义
    themeChanged = Signal(str)  # 主题变更信号
    windowStateChanged = Signal(str)  # 窗口状态变更信号
    pluginLoaded = Signal(str)  # 插件加载信号
    viewRegistered = Signal(str)  # 视图注册信号
    
    def __init__(self) -> None:
        """初始化应用程序核心实例"""
        super().__init__()
        
        # 初始化核心管理器
        self._plugin_manager = PluginManager()
        self._theme_manager = ThemeManager()
        self._window_manager = WindowManager()
        self._command_registry = CommandRegistry()
        self._config_registry = ConfigRegistry()
        self._view_registry = ViewRegistry()
        
        # 插件注册表
        self._plugins: Dict[str, Plugin] = {}

        # 注册默认插件目录
        self._register_default_plugin_dirs()
        
    def _register_default_plugin_dirs(self) -> None:
        """注册默认插件目录"""
        # 获取主包所在目录
        package_dir = Path(__file__).parent.parent
        # 内置插件目录
        builtin_plugins_dir = package_dir / "plugins"
        self._plugin_manager.add_plugin_directory(builtin_plugins_dir)

        # TODO: 用户插件目录（未来支持）
        # user_plugins_dir = Path.home() / ".geekfanatic" / "plugins"
        # if user_plugins_dir.exists():
        #     self._plugin_manager.add_plugin_directory(user_plugins_dir)
    
    def initialize_plugins(self) -> None:
        """初始化插件系统"""
        # 扫描并加载插件
        discovered_plugins = self._plugin_manager.discover_plugins()
        for plugin_class in discovered_plugins:
            self._load_plugin(plugin_class)

        # 加载内置插件
        self._ensure_builtin_plugins()
    
    def _ensure_builtin_plugins(self) -> None:
        """确保内置插件被加载"""
        builtin_plugins = [
            "geekfanatic.editor"  # 编辑器插件
        ]
        
        for plugin_id in builtin_plugins:
            if not self.is_plugin_loaded(plugin_id):
                plugin_class = self._plugin_manager.get_plugin_class(plugin_id)
                if plugin_class:
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
    @Slot(str, str, 'QVariant', str, str, int)
    def register_view(self, view_id: str, title: str,
                     component: 'QVariant', view_type: str = "widget",
                     icon: str = "", priority: int = 0) -> None:
        """
        注册视图
        
        Args:
            view_id: 视图唯一标识
            title: 视图标题
            component: 视图组件
                - QWidget: 用于QtWidgets视图
                - str/QUrl: 用于QML视图，QML文件路径
            view_type: 视图类型("widget"/"qml")
            icon: 图标
            priority: 优先级
        """
        view_type_enum = ViewType(view_type)
        self._view_registry.register_view(
            view_id=view_id,
            title=title,
            component=component,
            view_type=view_type_enum,
            icon=icon,
            priority=priority
        )
        self.viewRegistered.emit(view_id)
        self.viewRegistered.emit(view_id)
    
    @Slot(str, result='QVariantMap')
    def get_view(self, view_id: str) -> Dict:
        """获取视图信息"""
        view = self._view_registry.get_view(view_id)
        return view if view else {}
    
    @Slot(result='QVariantList')
    def get_views(self) -> List[Dict]:
        """获取所有视图"""
        return self._view_registry.get_sorted_views()
    
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
        
    @property
    def command_registry(self) -> CommandRegistry:
        """获取命令注册表"""
        return self._command_registry
        
    @property
    def config_registry(self) -> ConfigRegistry:
        """获取配置注册表"""
        return self._config_registry
        
    @property
    def view_registry(self) -> ViewRegistry:
        """获取视图注册表"""
        return self._view_registry