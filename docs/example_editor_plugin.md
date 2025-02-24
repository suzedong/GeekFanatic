# 编辑器插件示例

本文档展示如何使用GeekFanatic的插件系统实现一个完整的编辑器插件。

## 插件结构

```
editor/
├── __init__.py          # 插件入口
├── editor.py            # 编辑器实现
├── file_explorer.py     # 文件浏览器视图
├── buffer.py           # 文本缓冲区
├── types.py           # 类型定义
└── commands/          # 编辑命令
    ├── __init__.py
    └── basic.py      # 基础命令
```

## 插件入口

```python
class EditorPlugin(Plugin):
    def __init__(self, ide: Optional[IDEProtocol]) -> None:
        super().__init__(ide)
        self._file_explorer = FileExplorer()
        self._editors: Dict[str, Editor] = {}

    @property
    def id(self) -> str:
        return "geekfanatic.editor"

    def initialize(self) -> None:
        # 注册命令
        self._register_commands()
        # 注册配置
        self._register_configuration()
        # 注册到布局系统
        self._register_to_layout()
        # 连接信号
        self._connect_signals()
```

## 布局集成

### 活动栏项目

```python
def _register_to_layout(self) -> None:
    layout = self._ide_impl.layout
    
    # 添加活动栏图标
    layout.activity_bar.add_item(
        self.id,
        QIcon(":/icons/explorer.svg"),
        self.name
    )
```

### 侧边栏视图

```python
class FileExplorer(SideBarView):
    # 信号定义
    fileSelected = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__("explorer", "资源管理器", parent)
        self._setup_explorer()

    def _setup_explorer(self) -> None:
        # 创建文件系统模型
        self._model = QFileSystemModel()
        self._model.setRootPath(QDir.currentPath())
        
        # 创建树视图
        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.clicked.connect(self._on_item_clicked)
```

### 工作区集成

```python
def _on_file_selected(self, file_path: str) -> None:
    # 创建新的编辑器和标签页
    editor = Editor()
    tab = WorkTab(file_path, Path(file_path).name)
    
    # 设置编辑器内容
    editor.setParent(tab.content_widget)
    tab.content_widget.layout().addWidget(editor)
    
    # 添加到工作区
    self._ide_impl.layout.work_area.add_tab("main", tab)
```

## 功能实现

### 编辑器组件

```python
class Editor(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self._buffer = TextBuffer()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self._setup_style()

    def _setup_style(self) -> None:
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                selection-background-color: #264f78;
                font-family: 'Consolas';
                font-size: 14px;
            }
        """)
```

### 基础命令

```python
@command("editor.delete")
class DeleteCommand(Command):
    def execute(self) -> None:
        # 删除选中内容或当前字符
        pass

@command("editor.undo")
class UndoCommand(Command):
    def execute(self) -> None:
        # 撤销上一步操作
        pass

@command("editor.redo")
class RedoCommand(Command):
    def execute(self) -> None:
        # 重做操作
        pass
```

## 配置系统

```python
def _register_configuration(self) -> None:
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
                }
            },
            "indentation": {
                "type": "string",
                "enum": ["spaces", "tabs"],
                "default": "spaces",
                "description": "缩进类型",
            }
        }
    }
    self._ide_impl.config_registry.register(config)
```

## 交互流程

1. 插件激活
- 用户点击活动栏中的编辑器图标
- 显示文件浏览器视图
- 准备工作区

2. 文件操作
- 在文件浏览器中选择文件
- 创建新的编辑器标签页
- 加载并显示文件内容

3. 编辑功能
- 文本编辑
- 命令执行
- 配置应用

## 注意事项

1. 性能优化
- 大文件处理
- 内存管理
- 响应速度

2. 错误处理
- 文件操作异常
- 编码问题
- 权限问题

3. 用户体验
- 状态提示
- 进度显示
- 快捷键支持

## 扩展建议

1. 功能增强
- 语法高亮
- 代码折叠
- 自动完成

2. 界面优化
- 主题支持
- 自定义样式
- 动画效果

3. 集成功能
- Git支持
- 调试功能
- 终端集成