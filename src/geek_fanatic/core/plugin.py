"""
插件系统核心实现
"""

import importlib.util
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type, Any, cast, Protocol, runtime_checkable

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

# 配置日志
logging.basicConfig(level=logging.DEBUG)

@runtime_checkable
class IDEProtocol(Protocol):
    """IDE 接口协议"""
    pass

class ActivityIcon:
    """活动栏图标配置"""
    def __init__(self, icon: QIcon, tooltip: str):
        """初始化活动栏图标

        Args:
            icon: 图标
            tooltip: 提示文本
        """
        self.icon = icon
        self.tooltip = tooltip

class PluginViews:
    """插件视图集合"""
    def __init__(self):
        """初始化插件视图集合"""
        self.activity_icon: Optional[ActivityIcon] = None  # 活动栏图标
        self.side_views: Dict[str, QWidget] = {}          # 侧边栏视图
        self.work_views: Dict[str, QWidget] = {}          # 工作区视图

class Plugin(ABC):
    """插件基类"""

    def __init__(self, ide: Optional[IDEProtocol]) -> None:
        """初始化插件

        Args:
            ide: IDE 实例，提供插件运行所需的上下文环境
        """
        self._ide = ide

    @property
    @abstractmethod
    def id(self) -> str:
        """获取插件ID

        Returns:
            str: 插件的唯一标识符
        """
        pass

    @property
    def name(self) -> str:
        """获取插件名称

        Returns:
            str: 插件的显示名称
        """
        return self.__class__.__name__

    @property
    def version(self) -> str:
        """获取插件版本

        Returns:
            str: 插件的版本号
        """
        return "1.0.0"

    @property
    def description(self) -> str:
        """获取插件描述

        Returns:
            str: 插件的详细描述
        """
        return ""

    @abstractmethod
    def get_views(self) -> PluginViews:
        """获取插件视图

        Returns:
            PluginViews: 插件的视图集合
        """
        pass

    def initialize(self) -> None:
        """初始化插件

        在此处执行插件的初始化操作
        """
        pass

    def cleanup(self) -> None:
        """清理插件资源

        在此处执行插件的清理操作
        """
        pass

class PluginManager:
    """插件管理器"""

    def __init__(self) -> None:
        """初始化插件管理器"""
        self._plugin_dirs: List[Path] = []
        self._plugin_classes: Dict[str, Type[Plugin]] = {}
        self._logger = logging.getLogger(__name__)
        self._ide = None

    def set_ide(self, ide: IDEProtocol) -> None:
        """设置IDE实例

        Args:
            ide: IDE实例
        """
        self._ide = ide
        self._logger.info("IDE实例已设置")

    def add_plugin_directory(self, directory: Path) -> None:
        """添加插件目录

        Args:
            directory: 要添加的插件目录路径
        """
        if directory.is_dir() and directory not in self._plugin_dirs:
            self._plugin_dirs.append(directory)
            self._logger.info(f"添加插件目录: {directory}")

    def discover_plugins(self) -> List[Type[Plugin]]:
        """发现插件

        Returns:
            List[Type[Plugin]]: 发现的插件类列表
        """
        self._logger.info("开始扫描插件...")
        for plugin_dir in self._plugin_dirs:
            self._scan_directory(plugin_dir)
        self._logger.info(f"发现插件: {list(self._plugin_classes.keys())}")
        return list(self._plugin_classes.values())

    def get_plugin_class(self, plugin_id: str) -> Optional[Type[Plugin]]:
        """根据ID获取插件类

        Args:
            plugin_id: 插件ID

        Returns:
            Optional[Type[Plugin]]: 对应的插件类，如果不存在则返回None
        """
        plugin_class = self._plugin_classes.get(plugin_id)
        self._logger.debug(f"获取插件类 {plugin_id}: {'成功' if plugin_class else '失败'}")
        return plugin_class

    def _load_plugin(self, plugin_class: Type[Plugin]) -> None:
        """加载单个插件

        Args:
            plugin_class: 插件类
        """
        try:
            self._logger.info(f"正在加载插件: {plugin_class.__name__}")
            plugin = plugin_class(self._ide)
            plugin_id = plugin.id

            # 获取并注册插件视图
            views = plugin.get_views()
            if hasattr(self._ide, 'layout'):
                self._ide.layout.register_plugin_views(plugin_id, views)
                self._logger.info(f"插件视图注册成功: {plugin_id}")
            else:
                self._logger.warning(f"IDE实例缺少layout属性，无法注册插件视图: {plugin_id}")

            # 初始化插件
            plugin.initialize()
            self._logger.info(f"插件初始化完成: {plugin_id}")
        except Exception as e:
            self._logger.error(f"加载插件失败: {plugin_class.__name__} - {str(e)}")
            import traceback
            self._logger.error(traceback.format_exc())

    def _load_plugin_module(
        self, 
        spec_name: str, 
        file_path: Path
    ) -> Optional[Any]:
        """加载插件模块

        Args:
            spec_name: 模块规范名称
            file_path: 模块文件路径

        Returns:
            Optional[Any]: 加载的模块，如果加载失败则返回None
        """
        try:
            self._logger.debug(f"正在加载模块: {file_path}")
            spec = importlib.util.spec_from_file_location(spec_name, file_path)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self._logger.debug(f"模块加载成功: {file_path}")
                return module
        except Exception as e:
            self._logger.error(f"加载插件模块失败: {file_path} - {str(e)}")
            import traceback
            self._logger.error(traceback.format_exc())
        return None

    def _scan_directory(self, directory: Path) -> None:
        """扫描目录寻找插件

        Args:
            directory: 要扫描的目录
        """
        self._logger.info(f"扫描目录: {directory}")
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                setup_file = item / "setup.py"
                if setup_file.exists():
                    self._logger.debug(f"发现setup.py: {setup_file}")
                    module = self._load_plugin_module(
                        f"{item.name}.setup", 
                        setup_file
                    )
                    if module and hasattr(module, 'get_plugin_id') and hasattr(module, 'get_plugin_class'):
                        try:
                            plugin_id = module.get_plugin_id()
                            plugin_class = module.get_plugin_class()
                            if issubclass(plugin_class, Plugin) and plugin_class != Plugin:
                                self._plugin_classes[plugin_id] = plugin_class
                                self._logger.info(f"注册插件: {plugin_id}")
                        except Exception as e:
                            self._logger.error(
                                f"加载插件失败: {setup_file} - {str(e)}"
                            )
                            import traceback
                            self._logger.error(traceback.format_exc())
