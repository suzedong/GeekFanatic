# GeekFanatic

GeekFanatic 是一个模仿 VSCode 界面布局的程序框架，它提供了类似 VSCode 的用户界面布局和插件系统。

## 特性

- VSCode风格的三区域布局
  * 活动栏：切换不同的插件功能
  * 侧边栏：显示插件的辅助功能
  * 工作区：展示插件的主要功能界面

- 灵活的插件系统
  * 插件生命周期管理
  * 统一的布局接入点
  * 简单的开发方式

- 示例编辑器插件
  * 文件浏览功能
  * 基础文本编辑
  * 标签页管理

## 安装

使用 Poetry 安装依赖：

```bash
poetry install
```

## 运行

```bash
poetry run python -m geek_fanatic
```

## 开发插件

1. 创建插件类

```python
from geek_fanatic.core.plugin import Plugin

class MyPlugin(Plugin):
    @property
    def id(self) -> str:
        return "my.plugin.id"

    def initialize(self) -> None:
        # 注册到布局系统
        self._register_to_layout()
```

2. 添加布局组件

```python
def _register_to_layout(self) -> None:
    layout = self._ide_impl.layout
    
    # 添加活动栏图标
    layout.activity_bar.add_item(
        self.id,
        icon,
        self.name
    )
    
    # 添加侧边栏视图
    layout.side_bar.add_view(my_view)
    
    # 添加工作区内容
    layout.work_area.add_tab("main", my_tab)
```

3. 注册插件

在 setup.py 中：

```python
def get_plugin_id() -> str:
    return "my.plugin.id"

def get_plugin_class():
    return MyPlugin
```

## 项目结构

```
src/geek_fanatic/
├── core/           # 核心功能
│   ├── widgets/    # 基础UI组件
│   └── layout.py   # 布局管理
├── plugins/        # 插件目录
│   └── editor/     # 编辑器插件示例
└── resources/      # 资源文件
```

## 文档

- [架构设计](docs/architecture.md)
- [开发计划](docs/development_plan.md)
- [编辑器插件示例](docs/example_editor_plugin.md)

## 开发指南

1. 创建虚拟环境
```bash
poetry shell
```

2. 安装开发依赖
```bash
poetry install
```

3. 运行测试
```bash
poetry run pytest
```

4. 代码检查
```bash
poetry run mypy src
poetry run pylint src
```

## 贡献

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License

## 致谢

- VSCode 界面设计的启发
- PySide6 UI框架的支持