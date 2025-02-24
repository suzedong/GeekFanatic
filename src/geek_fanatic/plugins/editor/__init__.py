"""
编辑器插件入口模块
"""

from pathlib import Path
from typing import Optional, Dict

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTabWidget

from geek_fanatic.core.plugin import Plugin, PluginViews, ActivityIcon
from geek_fanatic.core.config import ConfigRegistry
from geek_fanatic.core.view import ViewRegistry
from geek_fanatic.core.command import CommandRegistry
from geek_fanatic.core.layout import Layout
from geek_fanatic.core.widgets.work_area import WorkTab

from .editor import Editor
from .file_explorer import FileExplorer
from .commands.basic import DeleteCommand, RedoCommand, UndoCommand

class EditorManager(QWidget):
    """编辑器管理器"""
    
    def __init__(self) -> None:
        """初始化编辑器管理器"""
        super().__init__()
        self._editors: Dict[str, Editor] = {}
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """设置UI"""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        self._tab_widget = QTabWidget()
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.setMovable(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self._layout.addWidget(self._tab_widget)
    
    def open_file(self, file_path: str) -> None:
        """打开文件
        
        Args:
            file_path: 文件路径
        """
        # 如果文件已经打开，切换到对应标签
        if file_path in self._editors:
            editor = self._editors[file_path]
            self._tab_widget.setCurrentWidget(editor)
            return
            
        # 创建新编辑器
        editor = Editor()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                editor.setPlainText(f.read())
        except Exception as e:
            print(f"Error loading file: {e}")
            return
            
        # 添加到标签页
        self._editors[file_path] = editor
        self._tab_widget.addTab(editor, Path(file_path).name)
        self._tab_widget.setCurrentWidget(editor)
    
    def _on_tab_close_requested(self, index: int) -> None:
        """处理标签页关闭请求
        
        Args:
            index: 标签页索引
        """
        editor = self._tab_widget.widget(index)
        for path, ed in self._editors.items():
            if ed == editor:
                del self._editors[path]
                break
        self._tab_widget.removeTab(index)

class IDEProtocol:
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
        self._editor_manager = EditorManager()

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

    def get_views(self) -> PluginViews:
        """获取插件视图"""
        views = PluginViews()
        
        # 活动栏图标
        icons_dir = Path(__file__).parent.parent.parent / "resources" / "icons"
        views.activity_icon = ActivityIcon(
            icon=QIcon(str(icons_dir / "explorer.svg")),
            tooltip=self.name
        )
        
        # 侧边栏文件浏览器
        views.side_views["explorer"] = self._file_explorer
        
        # 工作区编辑器
        views.work_views["editor"] = self._editor_manager
        
        return views

    def initialize(self) -> None:
        """初始化插件"""
        super().initialize()
        
        # 注册命令
        self._register_commands()
        
        # 注册配置
        self._register_configuration()
        
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
        config = {
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

    def _connect_signals(self) -> None:
        """连接信号"""
        # 监听文件浏览器的文件选择
        self._file_explorer.fileSelected.connect(self._on_file_selected)

    def _on_file_selected(self, file_path: str) -> None:
        """处理文件选择事件
        
        Args:
            file_path: 文件路径
        """
        self._editor_manager.open_file(file_path)

    def cleanup(self) -> None:
        """清理插件"""
        # 清理编辑器资源
        self._editor_manager._editors.clear()
        super().cleanup()
