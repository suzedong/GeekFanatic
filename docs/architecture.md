# GeekFanatic 架构设计

GeekFanatic 是一个模仿 VSCode 界面布局的程序框架，提供了灵活的插件系统和统一的界面布局。

## 整体架构

### 核心模块

1. 布局管理 (core/layout.py)
- 提供类似 VSCode 的三区域布局
  * 活动栏：48px宽，用于切换插件
  * 侧边栏：可调整宽度，显示插件的辅助视图
  * 工作区：主要功能区域，显示插件的核心功能

2. 基础组件 (core/widgets/)
- activity_bar.py：活动栏组件实现
- side_bar.py：侧边栏视图容器
- work_area.py：工作区组件实现

3. 插件系统 (core/plugin.py)
- 插件管理和加载
- 插件生命周期管理
- IDE接口协议定义

4. 其他核心功能
- 命令系统 (core/command.py)
- 配置系统 (core/config.py)
- 视图系统 (core/view.py)
- 主题系统 (core/theme.py)
- 窗口管理 (core/window.py)

### 插件架构

每个插件需要提供以下组件：

1. 活动栏项目
- 图标：用于在活动栏中显示
- 名称：悬停提示
- 点击事件：切换到该插件的功能

2. 侧边栏视图
- 继承自 SideBarView
- 提供插件的辅助功能
- 与工作区内容联动

3. 工作区内容
- 插件的主要功能界面
- 通过 WorkTab 系统管理

### 交互流程

1. 插件切换
- 用户点击活动栏图标
- 系统切换到对应插件
- 显示插件的侧边栏视图和工作区内容

2. 视图联动
- 侧边栏视图操作
- 触发工作区内容更新
- 保持两个区域的同步

## 示例：编辑器插件

编辑器插件展示了完整的功能实现：

1. 活动栏集成
- 显示编辑器图标
- 点击激活编辑器功能

2. 侧边栏实现
- 文件浏览器视图
- 文件树展示
- 文件选择功能

3. 工作区功能
- 多标签页管理
- 文本编辑功能
- 基础编辑命令

4. 交互联动
- 侧边栏选择文件
- 工作区打开编辑器
- 自动创建新标签页

## 扩展机制

1. 插件注册
```python
class MyPlugin(Plugin):
    def initialize(self) -> None:
        # 注册到布局系统
        self._register_to_layout()
        # 注册命令
        self._register_commands()
        # 注册配置
        self._register_configuration()
```

2. 布局接入
```python
def _register_to_layout(self) -> None:
    layout = self._ide_impl.layout
    # 添加活动栏图标
    layout.activity_bar.add_item(...)
    # 添加侧边栏视图
    layout.side_bar.add_view(...)
    # 添加工作区内容
    layout.work_area.add_tab(...)
```

3. 视图通信
```python
# 侧边栏视图发送信号
self.someAction.emit(data)

# 工作区接收并处理
def _on_side_bar_action(self, data):
    # 更新工作区内容
    self.update_work_area(data)
```

## 配置和资源

1. 配置系统
- 插件级配置
- 用户配置
- 工作区配置

2. 资源管理
- 图标资源
- 主题资源
- 样式表

## 未来扩展

1. 布局增强
- 面板区域
- 状态栏
- 更多分割视图

2. 功能扩展
- 多语言支持
- 调试集成
- 版本控制