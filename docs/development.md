# GeekFanatic IDE 开发指南

## 技术栈

- Python 3.11+
- Qt 6.5+ (通过 PySide6)
- Poetry 包管理
- pytest 测试框架

## 架构设计

### 核心模块

1. App 核心 (core/)
   - 应用程序生命周期管理
   - 插件系统
   - 配置管理
   - 主题系统
   - 窗口管理

2. 编辑器插件 (plugins/editor/)
   - 文本编辑核心
   - 代码高亮
   - 自动补全
   - 代码折叠
   - 查找替换
   - 编辑器命令系统

3. 用户界面 (ui/)
   - 主窗口管理
   - 对话框实现
   - 资源管理
   - 样式系统

## UI 技术选择原则

1. 默认使用 QtWidgets：
   - 数据密集型视图（文件树、符号列表等）
   - 复杂输入控件
   - 性能关键组件
   - 系统集成功能
   - 开发工具组件

2. 特殊情况考虑 QML：
   - 需要丰富的动画效果
   - 移动应用界面
   - 嵌入式设备界面
   - 多媒体应用
   - 需要触屏优化

## 开发规范

1. 代码风格
   - 使用 Black 格式化代码
   - 使用 isort 整理导入
   - 遵循 PEP 8
   - 使用类型注解
   - 编写中文注释

2. 提交规范
   - 使用语义化提交信息
   - 保持提交粒度适中
   - 编写清晰的提交说明

3. 测试要求
   - 单元测试覆盖率 > 80%
   - 编写集成测试
   - UI 自动化测试

## 插件开发

1. 插件结构
   ```
   plugin_name/
   ├── __init__.py
   ├── setup.py      # 插件注册
   ├── commands/     # 命令实现
   ├── features/     # 功能实现
   └── ui/          # 界面实现
       ├── widgets/  # Qt 部件
       └── resources/ # 资源文件
   ```

2. 注册插件
   ```python
   from geek_fanatic.core.plugin import Plugin

   class MyPlugin(Plugin):
       @property
       def id(self) -> str:
           return "my.plugin.id"
        
       def initialize(self) -> None:
           # 初始化插件
           pass
   ```

## 构建与发布

1. 开发环境设置
   ```bash
   # 安装依赖
   poetry install
   
   # 安装 pre-commit hooks
   poetry run pre-commit install
   ```

2. 运行测试
   ```bash
   # 运行所有测试
   poetry run pytest
   
   # 运行特定测试
   poetry run pytest tests/test_editor.py
   ```

3. 构建应用
   ```bash
   # 构建包
   poetry build
   
   # 打包应用
   poetry run pyinstaller main.spec
   ```

## 调试技巧

1. 使用 VSCode 调试
   - 设置断点
   - 查看变量
   - 单步执行

2. 日志记录
   - 使用内置的日志系统
   - 设置适当的日志级别
   - 记录关键信息

3. 性能分析
   - 使用 cProfile
   - 分析性能瓶颈
   - 优化关键路径

## 常见问题

1. 依赖管理
   - 使用 poetry add/remove 管理依赖
   - 注意版本兼容性
   - 定期更新依赖

2. 资源管理
   - 使用 Qt Resource System
   - 注意资源路径
   - 管理资源大小

3. 性能优化
   - 使用 QThread 处理耗时操作
   - 优化渲染性能
   - 实现数据懒加载