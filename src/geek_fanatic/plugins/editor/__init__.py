"""
编辑器插件入口模块
"""

from typing import Any, Dict, Protocol, Optional, Type

# pylint: disable=no-name-in-module
from PySide6 import QtQml
from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlEngine

from geek_fanatic.core.plugin import Plugin
from geek_fanatic.core.config import ConfigRegistry
from geek_fanatic.core.view import ViewRegistry, ViewType
from geek_fanatic.core.command import CommandRegistry

from .editor import Editor
from .commands.basic import DeleteCommand, RedoCommand, UndoCommand
from .commands.search import FindCommand, ReplaceCommand

class IDEProtocol(Protocol):
    """IDE 接口协议"""
    command_registry: CommandRegistry
    config_registry: ConfigRegistry
    view_registry: ViewRegistry

# QML 类型注册常量
MODULE_URI = "GeekFanatic.Editor"
MAJOR_VERSION = 1
MINOR_VERSION = 0

def register_qml_type(
    type_class: Type[QObject], 
    uri: str, 
    major_version: int, 
    minor_version: int, 
    name: str
) -> bool:
    """注册 QML 类型的辅助函数

    Args:
        type_class: 要注册的类（必须是 QObject 子类）
        uri: QML URI
        major_version: 主版本号
        minor_version: 次版本号
        name: QML 类型名称

    Returns:
        bool: 注册是否成功

    Raises:
        RuntimeError: 如果注册失败
        TypeError: 如果类不是 QObject 子类
    """
    try:
        # 确保类是 QObject 子类
        if not issubclass(type_class, QObject):
            raise TypeError(f"{type_class.__name__} must be a QObject subclass")

        # 创建一个临时的 QML 引擎进行注册
        engine = QQmlEngine()
        result = QtQml.qmlRegisterType(type_class, uri, major_version, minor_version, name)  # type: ignore

        if result == -1:
            raise RuntimeError(f"Failed to register QML type: {name}")
        return True

    except Exception as e:
        raise RuntimeError(f"QML registration error: {e}") from e

class EditorPlugin(Plugin):
    """编辑器插件实现"""

    def __init__(self, ide: Optional[IDEProtocol]) -> None:
        """初始化插件

        Args:
            ide: IDE 实例

        Raises:
            ValueError: 如果 IDE 实例为 None
        """
        super().__init__(ide)
        if ide is None:
            raise ValueError("IDE instance is required")
        self._ide_impl = ide

    @property
    def id(self) -> str:
        """获取插件ID"""
        return "geekfanatic.editor"

    @property
    def name(self) -> str:
        """获取插件名称"""
        return "Editor"

    @property
    def version(self) -> str:
        """获取插件版本"""
        return "1.0.0"

    @property
    def description(self) -> str:
        """获取插件描述"""
        return "GeekFanatic 的核心编辑器插件，提供基础的文本编辑功能"

    def initialize(self) -> None:
        """初始化插件

        注册插件的各种组件：命令、配置和视图。
        如果任何注册失败，会记录错误但继续执行。

        Raises:
            RuntimeError: 如果初始化过程中发生严重错误
        """
        super().initialize()
        
        try:
            # 注册命令
            self._register_commands()
            # 注册配置
            self._register_configuration()
            # 注册视图
            self._register_views()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EditorPlugin: {e}") from e

    def register_types(self) -> None:
        """注册 QML 类型

        将编辑器组件注册到 QML 系统中，使其可在 QML 中使用。

        Raises:
            RuntimeError: 如果 QML 类型注册失败
        """
        try:
            # 对于类型检查器禁用此行
            QtQml.qmlRegisterType(Editor, MODULE_URI, MAJOR_VERSION, MINOR_VERSION, "EditorComponent")  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to register QML types: {e}") from e

    def _register_commands(self) -> None:
        """注册编辑器命令

        注册编辑器的基本命令和搜索命令。
        """
        commands = [
            DeleteCommand(),
            UndoCommand(),
            RedoCommand(),
            FindCommand(),
            ReplaceCommand(),
        ]

        for command in commands:
            self._ide_impl.command_registry.register(command)

    def _register_configuration(self) -> None:
        """注册编辑器配置

        设置编辑器的默认配置，包括字体、缩进等设置。
        """
        config: Dict[str, Any] = {
            "editor": {
                "font": {
                    "family": {
                        "type": "string",
                        "default": "Consolas",
                        "description": "编辑器字体",
                    },
                    "size": {
                        "type": "number",
                        "default": 14,
                        "description": "字体大小",
                    },
                },
                "indentation": {
                    "type": "string",
                    "enum": ["spaces", "tabs"],
                    "default": "spaces",
                    "description": "缩进类型",
                },
                "tabSize": {
                    "type": "number",
                    "default": 4,
                    "description": "制表符宽度",
                },
            }
        }

        self._ide_impl.config_registry.register(config)

    def _register_views(self) -> None:
        """注册编辑器视图

        注册编辑器的主视图组件。
        """
        self._ide_impl.view_registry.register_view(
            view_id="editor",
            title="Editor",
            component="EditorComponent",
            view_type=ViewType.QML,
            icon="icons/editor.svg",
            priority=100,
        )
