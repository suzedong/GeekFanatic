"""
编辑器插件安装配置
"""
from geek_fanatic.core.plugin import Plugin
from geek_fanatic.plugins.editor.widgets import Editor

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
        
    def _register_commands(self) -> None:
        """注册编辑器命令"""
        from geek_fanatic.plugins.editor.commands.basic import (
            DeleteCommand,
            UndoCommand,
            RedoCommand,
            SelectAllCommand,
            CopyCommand,
            PasteCommand,
            CutCommand
        )
        from geek_fanatic.plugins.editor.commands.search import (
            FindCommand,
            ReplaceCommand,
            ReplaceAllCommand
        )
        
        for cmd_cls in [
            DeleteCommand,
            UndoCommand,
            RedoCommand,
            SelectAllCommand,
            CopyCommand,
            PasteCommand,
            CutCommand,
            FindCommand,
            ReplaceCommand,
            ReplaceAllCommand
        ]:
            self._ide.command_registry.register(cmd_cls())
        
    def _register_configuration(self) -> None:
        """注册编辑器配置"""
        config = {
            "editor": {
                "font": {
                    "family": {
                        "type": "string",
                        "default": "Consolas",
                        "description": "编辑器字体"
                    },
                    "size": {
                        "type": "number",
                        "default": 14,
                        "description": "字体大小"
                    }
                },
                "indentation": {
                    "type": "string",
                    "enum": ["spaces", "tabs"],
                    "default": "spaces",
                    "description": "缩进类型"
                },
                "tabSize": {
                    "type": "number",
                    "default": 4,
                    "description": "制表符宽度"
                }
            }
        }
        self._ide.config_registry.register(config)
        
    def _register_views(self) -> None:
        """注册编辑器视图"""
        # 创建自定义编辑器部件
        editor = Editor()
        
        # 连接编辑器事件
        editor.cursorPositionChanged.connect(self._on_cursor_position_changed)
        
        # 注册视图
        self._ide.register_view(
            view_id="editor",
            title="Editor",
            widget=editor,
            icon="edit",
            priority=100
        )
        
    def _on_cursor_position_changed(self, line: int, column: int) -> None:
        """处理光标位置变化"""
        print(f"Cursor position: Line {line}, Column {column}")