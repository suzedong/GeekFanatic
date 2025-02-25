"""
GeekFanatic 核心应用模块
"""

from pathlib import Path
from typing import Dict, Type
import logging

from PySide6.QtCore import QObject, Signal, Slot

from .command import CommandRegistry
from .config import ConfigRegistry
from .plugin import Plugin, PluginManager
from .theme import ThemeManager
from .view import ViewRegistry
from .window import WindowManager, WindowState
from .layout import Layout

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
        self._logger = logging.getLogger(__name__)

        # 初始化核心管理器
        self._plugin_manager = PluginManager()
        self._plugin_manager.set_GF(self)
        
        self._theme_manager = ThemeManager()
        self._window_manager = WindowManager()
        self._command_registry = CommandRegistry()
        self._config_registry = ConfigRegistry()
        self._view_registry = ViewRegistry()
        self._layout: Layout = None

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

    def initialize_plugins(self) -> None:
        """初始化插件系统"""
        if not self._layout:
            raise RuntimeError("Layout must be set before initializing plugins")
            
        self._logger.info("开始初始化插件系统...")
            
        # 扫描并加载插件
        discovered_plugins = self._plugin_manager.discover_plugins()
        self._logger.info(f"发现 {len(discovered_plugins)} 个插件")
        
        for plugin_class in discovered_plugins:
            self._load_plugin(plugin_class)

        # 加载内置插件
        self._ensure_builtin_plugins()
        
        self._logger.info("插件系统初始化完成")

    def _load_plugin(self, plugin_class: Type[Plugin]) -> None:
        """加载单个插件"""
        try:
            self._logger.info(f"正在加载插件: {plugin_class.__name__}")
            plugin = plugin_class(self)
            plugin_id = plugin.id

            if plugin_id in self._plugins:
                self._logger.debug(f"插件已加载，跳过: {plugin_id}")
                return

            # 获取并注册插件视图
            views = plugin.get_views()
            self._logger.debug(f"获取插件视图: {plugin_id}")
            
            if views.activity_icons:
                self._logger.debug(f"插件 {plugin_id} 包含活动栏图标列表: {[icon.id for icon in views.activity_icons]}")
            
            if views.side_views:
                self._logger.debug(f"插件 {plugin_id} 包含侧边栏视图: {list(views.side_views.keys())}")
            
            if views.work_views:
                self._logger.debug(f"插件 {plugin_id} 包含工作区视图: {list(views.work_views.keys())}")

            # 注册视图
            self._layout.register_plugin_views(plugin_id, views)
            self._logger.info(f"插件视图注册成功: {plugin_id}")

            # 初始化插件
            self._plugins[plugin_id] = plugin
            plugin.initialize()
            self.pluginLoaded.emit(plugin_id)
            self._logger.info(f"插件加载完成: {plugin_id}")
            
        except Exception as e:
            self._logger.error(f"加载插件失败: {plugin_class.__name__} - {str(e)}")
            import traceback
            self._logger.error(traceback.format_exc())

    def _ensure_builtin_plugins(self) -> None:
        """确保内置插件被加载"""
        builtin_plugins = [
            "geekfanatic.editor"  # 编辑器插件（含文件浏览器）
        ]

        for plugin_id in builtin_plugins:
            if not self.is_plugin_loaded(plugin_id):
                self._logger.info(f"加载内置插件: {plugin_id}")
                plugin_class = self._plugin_manager.get_plugin_class(plugin_id)
                if plugin_class:
                    self._load_plugin(plugin_class)
                else:
                    self._logger.warning(f"未找到内置插件: {plugin_id}")

    @Slot(str)
    def set_theme(self, theme_name: str) -> None:
        """设置主题"""
        self._theme_manager.set_theme(theme_name)
        self.themeChanged.emit(theme_name)

    @Slot(str)
    def set_window_state(self, state: str) -> None:
        """设置窗口状态
        
        Args:
            state: 窗口状态，可选值：'normal', 'maximized', 'minimized', 'fullscreen'
            
        Raises:
            ValueError: 当提供的状态值无效时抛出
        """
        try:
            window_state = WindowState(state.lower())
            self._window_manager.set_window_state(window_state)
            self.windowStateChanged.emit(window_state.value)
        except ValueError as e:
            raise ValueError(
                f"无效的窗口状态: {state}。有效值为: {', '.join(s.value for s in WindowState)}"
            ) from e

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

    @property
    def layout(self) -> Layout:
        """获取布局管理器"""
        return self._layout

    def set_layout(self, layout: Layout) -> None:
        """设置布局管理器"""
        self._layout = layout
