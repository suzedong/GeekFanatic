"""
插件系统核心模块
"""
from abc import ABC, ABCMeta, abstractmethod
from importlib import util
from pathlib import Path
from typing import Dict, List, Optional, Type

from PySide6.QtCore import QObject

# 创建一个自定义元类来解决 ABC 和 QObject 的元类冲突
class PluginMeta(type(QObject), ABCMeta):
    """Plugin 元类，用于解决 ABC 和 QObject 的元类冲突"""
    pass

class Plugin(QObject, ABC, metaclass=PluginMeta):
    """插件基类，定义插件接口和生命周期方法"""
    
    def __init__(self, core_instance: 'GeekFanatic') -> None:
        """初始化插件实例"""
        super().__init__()
        self._ide = core_instance
        self._enabled = False
        
    @property
    @abstractmethod
    def id(self) -> str:
        """插件唯一标识"""
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """插件描述"""
        pass
        
    @property
    def enabled(self) -> bool:
        """插件是否启用"""
        return self._enabled
        
    def initialize(self) -> None:
        """初始化插件"""
        self._enabled = True
        
    def cleanup(self) -> None:
        """清理插件资源"""
        self._enabled = False
        
    def register_types(self) -> None:
        """注册插件提供的QML类型"""
        pass

class PluginManager:
    """插件管理器，负责插件的发现、加载和生命周期管理"""
    
    def __init__(self) -> None:
        """初始化插件管理器"""
        self._plugin_classes: Dict[str, Type[Plugin]] = {}
        self._plugin_dirs: List[Path] = []
        
    def add_plugin_directory(self, directory: Path) -> None:
        """添加插件目录"""
        if directory.is_dir() and directory not in self._plugin_dirs:
            self._plugin_dirs.append(directory)
            
    def discover_plugins(self) -> List[Type[Plugin]]:
        """发现并加载所有可用插件"""
        discovered_plugins: List[Type[Plugin]] = []
        
        # 扫描所有插件目录
        for plugin_dir in self._plugin_dirs:
            self._scan_directory(plugin_dir, discovered_plugins)
            
        return discovered_plugins
        
    def _scan_directory(self, directory: Path, discovered_plugins: List[Type[Plugin]]) -> None:
        """扫描目录查找插件"""
        for path in directory.rglob("*.py"):
            if path.stem.startswith("_"):
                continue
                
            try:
                # 动态导入模块
                spec = util.spec_from_file_location(path.stem, path)
                if spec is None or spec.loader is None:
                    continue
                    
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 查找插件类
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, Plugin) and 
                        attr is not Plugin):
                        plugin_class = attr
                        discovered_plugins.append(plugin_class)
                        self._plugin_classes[plugin_class.id] = plugin_class
                        
            except Exception as e:
                print(f"加载插件失败: {path} - {str(e)}")
                
    def get_plugin_class(self, plugin_id: str) -> Optional[Type[Plugin]]:
        """获取插件类"""
        return self._plugin_classes.get(plugin_id)