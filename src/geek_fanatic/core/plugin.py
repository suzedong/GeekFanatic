"""
插件系统核心实现
"""

import importlib.util
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type, Any, cast, Protocol, runtime_checkable

@runtime_checkable
class IDEProtocol(Protocol):
    """IDE 接口协议"""
    pass

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

    def register_types(self) -> None:
        """注册QML类型

        在此处注册插件提供的QML类型
        """
        pass

class PluginManager:
    """插件管理器"""

    def __init__(self) -> None:
        """初始化插件管理器"""
        self._plugin_dirs: List[Path] = []
        self._plugin_classes: Dict[str, Type[Plugin]] = {}
        self._logger = logging.getLogger(__name__)

    def add_plugin_directory(self, directory: Path) -> None:
        """添加插件目录

        Args:
            directory: 要添加的插件目录路径
        """
        if directory.is_dir() and directory not in self._plugin_dirs:
            self._plugin_dirs.append(directory)

    def discover_plugins(self) -> List[Type[Plugin]]:
        """发现插件

        Returns:
            List[Type[Plugin]]: 发现的插件类列表
        """
        for plugin_dir in self._plugin_dirs:
            self._scan_directory(plugin_dir)
        return list(self._plugin_classes.values())

    def get_plugin_class(self, plugin_id: str) -> Optional[Type[Plugin]]:
        """根据ID获取插件类

        Args:
            plugin_id: 插件ID

        Returns:
            Optional[Type[Plugin]]: 对应的插件类，如果不存在则返回None
        """
        return self._plugin_classes.get(plugin_id)

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
            spec = importlib.util.spec_from_file_location(spec_name, file_path)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
        except Exception as e:
            self._logger.error(f"加载插件模块失败: {file_path} - {str(e)}")
        return None

    def _process_plugin_class(self, attr: Any, plugin_id: str) -> None:
        """处理插件类

        Args:
            attr: 要检查的属性
            plugin_id: 插件ID
        """
        if (isinstance(attr, type) 
            and issubclass(attr, Plugin) 
            and attr != Plugin):
            self._plugin_classes[plugin_id] = cast(Type[Plugin], attr)

    def _scan_directory(self, directory: Path) -> None:
        """扫描目录寻找插件

        Args:
            directory: 要扫描的目录
        """
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                setup_file = item / "setup.py"
                if setup_file.exists():
                    module = self._load_plugin_module(
                        f"{item.name}.setup", 
                        setup_file
                    )
                    if module:
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            try:
                                if (isinstance(attr, type) 
                                    and issubclass(attr, Plugin) 
                                    and attr != Plugin):
                                    # 创建临时实例以获取插件ID
                                    plugin_class = cast(Type[Plugin], attr)
                                    temp_instance = plugin_class(None)
                                    plugin_id = temp_instance.id
                                    self._plugin_classes[plugin_id] = plugin_class
                            except Exception as e:
                                self._logger.error(
                                    f"处理插件类失败: {attr_name} in {setup_file} - {str(e)}"
                                )

            elif item.suffix == ".py" and not item.name.startswith("_"):
                module = self._load_plugin_module(item.stem, item)
                if module:
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        try:
                            if (isinstance(attr, type) 
                                and issubclass(attr, Plugin) 
                                and attr != Plugin):
                                # 创建临时实例以获取插件ID
                                plugin_class = cast(Type[Plugin], attr)
                                temp_instance = plugin_class(None)
                                plugin_id = temp_instance.id
                                self._plugin_classes[plugin_id] = plugin_class
                        except Exception as e:
                            self._logger.error(
                                f"处理插件类失败: {attr_name} in {item} - {str(e)}"
                            )
