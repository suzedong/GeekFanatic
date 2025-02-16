# GeekFanatic

GeekFanatic一个采用现代化程序架构的桌面应用程序，完整模仿Visual Studio Code的界面布局与核心架构，基于 Python 和 Qt 框架开发。

GeekFanatic为后续通过插件方式开发各类功能预留扩展点。文本编辑器将作为第一个默认插件来开发。

## 功能特点

- 现代化界面设计，完整模仿 VSCode 界面布局
- 插件化架构设计，支持功能扩展
- 主题系统支持，可自定义界面外观
- 基础文本编辑器功能
- 支持窗口布局调整
- 文件变更实时监控
- 跨平台支持

## 系统要求

- Python 3.11
- PySide6 6.5.3
- 支持的操作系统：Windows、Linux、macOS

## 技术栈

- **GUI 框架**: PySide6 (Qt for Python)
- **UI 技术**: Qt Quick/QML
- **文件监控**: watchdog
- **代码质量工具**:
  - black (代码格式化)
  - isort (import 排序)
  - mypy (类型检查)
  - pylint (代码分析)
- **测试框架**: pytest + pytest-qt

## 项目结构

```
GeekFanatic/
├── src/
│   └── geek_fanatic/
│       ├── core/           # 核心模块
│       │   ├── app.py     # 应用程序核心类
│       │   ├── plugin.py  # 插件系统
│       │   ├── theme.py   # 主题管理
│       │   └── window.py  # 窗口管理
│       ├── plugins/        # 插件目录
│       ├── resources/      # 资源文件
│       │   └── icons/     # 图标资源
│       ├── ui/            # 界面组件
│       │   ├── main.qml   # 主窗口
│       │   ├── ActivityBar.qml
│       │   ├── SideBar.qml
│       │   ├── EditorArea.qml
│       │   ├── Panel.qml
│       │   └── StatusBar.qml
│       └── __main__.py    # 程序入口
├── tests/                 # 测试目录
├── pyproject.toml        # 项目配置
└── README.md            # 项目文档
```

## 安装方法

1. 克隆项目代码：
```bash
git clone https://github.com/suzedong/geek-fanatic.git
cd geek-fanatic
```

2. 使用 Poetry 安装依赖：
```bash
poetry install
```

## 运行方法

```bash
poetry run python -m geek_fanatic
```

## 插件开发

GeekFanatic 提供了完整的插件 API，您可以通过以下步骤开发新插件：

1. 在 `plugins` 目录下创建新的插件包
2. 继承 `Plugin` 基类实现插件功能
3. 实现必要的生命周期方法
4. 注册插件到插件管理器

插件示例：

```python
from geek_fanatic.core.plugin import Plugin

class MyPlugin(Plugin):
    @property
    def id(self) -> str:
        return "my_plugin"
        
    @property
    def name(self) -> str:
        return "My Plugin"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def description(self) -> str:
        return "这是一个示例插件"
        
    def initialize(self) -> None:
        # 插件初始化代码
        pass
```

## 主题开发

您可以通过以下步骤创建自定义主题：

1. 创建新的主题类
2. 定义颜色方案
3. 注册主题到主题管理器

主题示例：

```python
from geek_fanatic.core.theme import Theme, ThemeType

my_theme = Theme(
    name="My Theme",
    type=ThemeType.DARK,
    colors={
        "editor.background": "#1e1e1e",
        "editor.foreground": "#d4d4d4",
        # 其他颜色定义...
    }
)
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目主页：https://github.com/suzedong/geek-fanatic
- 问题反馈：https://github.com/suzedong/geek-fanatic/issues