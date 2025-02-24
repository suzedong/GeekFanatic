"""
编辑器插件入口模块
"""

from pathlib import Path
from typing import Any, Dict, Protocol, Optional

from PySide6.QtGui import QIcon

from geek_fanatic.core.plugin import Plugin
from geek_fanatic.core.config import ConfigRegistry
from geek_fanatic.core.view import ViewRegistry
from geek_fanatic.core.command import CommandRegistry
from geek_fanatic.core.layout import Layout
from geek_fanatic.core.widgets.work_area import WorkTab

from .editor import Editor
from .file_explorer import FileExplorer
from .commands.basic import DeleteCommand, RedoCommand, UndoCommand

class IDEProtocol(Protocol):
    """IDE 接口协议"""
    command_registry: CommandRegistry
    config_registry: ConfigRegistry
    view_registry: ViewRegistry
    layout: Layout

class EditorPlugin(Plugin):
    """编辑器插件实现"""

    def __init__(self, ide: Optional[IDEProtocol]) -> None:
        """初始化插件"""
        super().__init__(ide)
        if ide is None:
            raise ValueError("IDE instance is required")
        self._ide_impl = ide
        self._file_explorer = FileExplorer()
        self._editors: Dict[str, Editor] = {}

    @property
    def id(self) -> str:
        """获取插件ID"""
        return "geekfanatic.editor"

    @property
    def name(self) -> str:
        """获取插件名称"""
        return "编辑器"

    @property
    def version(self) -> str:
        """获取插件版本"""
        return "1.0.0"

    @property
    def description(self) -> str:
        """获取插件描述"""
        return "提供基础的文本编辑功能"

    def initialize(self) -> None:
        """初始化插件"""
        super().initialize()
        
        # 注册命令
        self._register_commands()
        
        # 注册配置
        self._register_configuration()
        
        # 注册到布局系统
        self._register_to_layout()
        
        # 连接信号
        self._connect_signals()

    def _register_commands(self) -> None:
        """注册编辑器命令"""
        commands = [
            DeleteCommand(),
            UndoCommand(),
            RedoCommand(),
        ]

        for command in commands:
            self._ide_impl.command_registry.register(command)

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
        self._ide_impl.config_registry.register(config)

    def _register_to_layout(self) -> None:
        """注册到布局系统"""
        layout = self._ide_impl.layout
        
        # 添加到侧边栏
        layout.side_bar.add_view(self._file_explorer)
        
        # 添加活动栏图标
        icons_dir = Path(__file__).parent.parent.parent / "resources" / "icons"
        layout.activity_bar.add_item(
            self.id,
            QIcon(str(icons_dir / "explorer.svg")),
            self.name
        )

    def _connect_signals(self) -> None:
        """连接信号"""
        # 监听文件浏览器的文件选择
        self._file_explorer.fileSelected.connect(self._on_file_selected)

    def _on_file_selected(self, file_path: str) -> None:
        """处理文件选择事件"""
        # 如果文件已经打开，激活对应标签页
        if file_path in self._editors:
            editor = self._editors[file_path]
            self._ide_impl.layout.work_area.set_active_group("main")
            return

        # 否则创建新的编辑器和标签页
        editor = Editor()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                editor.setPlainText(f.read())
        except Exception as e:
            print(f"Error loading file: {e}")
            return

        # 创建标签页
        tab = WorkTab(file_path, Path(file_path).name)
        editor.setParent(tab.content_widget)
        # 将编辑器添加到标签页的内容区域
        tab.content_widget.layout().addWidget(editor)
        
        # 保存编辑器引用
        self._editors[file_path] = editor
        
        # 添加到工作区
        self._ide_impl.layout.work_area.add_tab("main", tab)

    def cleanup(self) -> None:
        """清理插件"""
        # 关闭所有编辑器
        self._editors.clear()
        super().cleanup()
