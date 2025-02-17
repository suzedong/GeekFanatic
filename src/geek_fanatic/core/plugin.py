"""
插件系统核心实现
"""

import importlib.util
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type

from PySide6.QtCore import QObject


class Plugin(ABC):
    """插件基类"""

    def __init__(self, ide) -> None:
        """初始化插件"""
        self._ide = ide

    @property
    @abstractmethod
    def id(self) -> str:
        """获取插件ID"""
        pass

    @property
    def name(self) -> str:
        """获取插件名称"""
        return self.__class__.__name__

    @property
    def version(self) -> str:
        """获取插件版本"""
        return "1.0.0"

    @property
    def description(self) -> str:
        """获取插件描述"""
        return ""

    def initialize(self) -> None:
        """初始化插件"""
        pass

    def cleanup(self) -> None:
        """清理插件资源"""
        pass

    def register_types(self) -> None:
        """注册QML类型"""
        pass


class PluginManager:
    """插件管理器"""

    def __init__(self) -> None:
        """初始化插件管理器"""
        self._plugin_dirs: List[Path] = []
        self._plugin_classes: Dict[str, Type[Plugin]] = {}
        self._logger = logging.getLogger(__name__)

    def add_plugin_directory(self, directory: Path) -> None:
        """添加插件目录"""
        if directory.is_dir() and directory not in self._plugin_dirs:
            self._plugin_dirs.append(directory)

    def discover_plugins(self) -> List[Type[Plugin]]:
        """发现插件"""
        for plugin_dir in self._plugin_dirs:
            self._scan_directory(plugin_dir)
        return list(self._plugin_classes.values())

    def get_plugin_class(self, plugin_id: str) -> Optional[Type[Plugin]]:
        """根据ID获取插件类"""
        return self._plugin_classes.get(plugin_id)

    def _scan_directory(self, directory: Path) -> None:
        """扫描目录寻找插件"""
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                setup_file = item / "setup.py"
                if setup_file.exists():
                    try:
                        # 动态导入 setup.py
                        spec = importlib.util.spec_from_file_location(
                            f"{item.name}.setup", setup_file
                        )
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)

                            # 查找继承自 Plugin 的类
                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                if (
                                    isinstance(attr, type)
                                    and issubclass(attr, Plugin)
                                    and attr != Plugin
                                ):
                                    plugin_class = attr
                                    # 创建临时实例以获取插件ID
                                    temp_instance = plugin_class(None)
                                    plugin_id = temp_instance.id
                                    self._plugin_classes[plugin_id] = plugin_class
                    except Exception as e:
                        self._logger.error(f"加载插件失败: {setup_file} - {str(e)}")

            elif item.suffix == ".py" and not item.name.startswith("_"):
                try:
                    # 动态导入 .py 文件
                    spec = importlib.util.spec_from_file_location(item.stem, item)
                    if spec is not None and spec.loader is not None:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # 查找继承自 Plugin 的类
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (
                                isinstance(attr, type)
                                and issubclass(attr, Plugin)
                                and attr != Plugin
                            ):
                                plugin_class = attr
                                # 创建临时实例以获取插件ID
                                temp_instance = plugin_class(None)
                                plugin_id = temp_instance.id
                                self._plugin_classes[plugin_id] = plugin_class
                except Exception as e:
                    self._logger.error(f"加载插件失败: {item} - {str(e)}")
