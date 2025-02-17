"""
编辑器插件入口模块
"""

from typing import Any, Dict

from PySide6.QtCore import QObject
from PySide6.QtQml import qmlRegisterType

from geek_fanatic.core.plugin import Plugin

from .editor import Editor


class EditorPlugin(Plugin):
    """编辑器插件实现"""

    @property
    def id(self) -> str:
        return "geekfanatic.editor"

    @property
    def name(self) -> str:
        return "Editor"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "GeekFanatic 的核心编辑器插件，提供基础的文本编辑功能"

    def initialize(self) -> None:
        """初始化插件"""
        super().initialize()
        # 注册命令
        self._register_commands()
        # 注册配置
        self._register_configuration()
        # 注册视图
        self._register_views()

    def register_types(self) -> None:
        """注册 QML 类型"""
        qmlRegisterType(Editor, "GeekFanatic.Editor", 1, 0, "EditorComponent")

    def _register_commands(self) -> None:
        """注册编辑器命令"""
        from .commands.basic import DeleteCommand, RedoCommand, UndoCommand
        from .commands.search import FindCommand, ReplaceCommand

        self._ide.command_registry.register(DeleteCommand())
        self._ide.command_registry.register(UndoCommand())
        self._ide.command_registry.register(RedoCommand())
        self._ide.command_registry.register(FindCommand())
        self._ide.command_registry.register(ReplaceCommand())

    def _register_configuration(self) -> None:
        """注册编辑器配置"""
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
        self._ide.config_registry.register(config)

    def _register_views(self) -> None:
        """注册编辑器视图"""
        self._ide.view_registry.register_view(
            view_id="editor", title="Editor", component="EditorComponent"
        )
