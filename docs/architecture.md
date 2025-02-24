# GeekFanatic 架构文档

## 整体架构

GeekFanatic 采用插件化架构，主要由以下部分组成：
- 核心框架：提供基础设施和插件管理
- 插件系统：提供扩展功能
- UI 框架：基于 Qt 实现的用户界面

## 界面布局

整体界面分为三个主要区域：
1. 活动栏 (Activity Bar)：显示已安装插件的图标，用于切换插件
2. 侧边栏 (Side Bar)：显示当前插件的辅助功能区域，如文件浏览器、设置面板等
3. 工作区 (Work Area)：显示插件的主要功能区域，如编辑器、插件详情等

### 布局管理

布局管理由 `Layout` 类负责，实现了：
- 界面区域的初始化和组织
- 插件视图的管理和切换
- 布局状态的保存和恢复

## 插件系统

### 插件结构

每个插件必须包含：
- setup.py：插件的注册配置
- __init__.py：插件的主要实现

### 插件接口

插件需要实现以下接口：
```python
class Plugin(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """插件唯一标识符"""
        pass

    @abstractmethod
    def get_views(self) -> PluginViews:
        """获取插件视图"""
        pass

    def initialize(self) -> None:
        """初始化插件"""
        pass

    def cleanup(self) -> None:
        """清理插件资源"""
        pass
```

### 插件视图

插件视图通过 `PluginViews` 类统一管理：
```python
class PluginViews:
    def __init__(self):
        self.activity_icon: Optional[ActivityIcon] = None  # 活动栏图标
        self.side_views: Dict[str, QWidget] = {}          # 侧边栏视图
        self.work_views: Dict[str, QWidget] = {}          # 工作区视图
```

### 注册规范

1. 活动栏图标：
   - 用于切换插件
   - 只显示图标和悬停提示

2. 侧边栏视图：
   - 显示插件的辅助功能
   - 如：文件浏览器、插件列表、菜单区、设置区等

3. 工作区视图：
   - 显示插件的主要功能
   - 如：编辑器内容、插件详情、业务内容等

## 插件示例

以编辑器插件为例：

```python
class EditorPlugin(Plugin):
    def get_views(self) -> PluginViews:
        views = PluginViews()
        
        # 活动栏图标
        views.activity_icon = ActivityIcon(
            icon=QIcon("explorer.svg"),
            tooltip="文件浏览器"
        )
        
        # 侧边栏：文件浏览器
        views.side_views["explorer"] = FileExplorer()
        
        # 工作区：编辑器
        views.work_views["editor"] = EditorManager()
        
        return views
```

## 开发规范

1. 插件开发：
   - 遵循插件接口规范
   - 实现必要的生命周期方法
   - 合理组织视图结构

2. 视图开发：
   - 活动栏仅提供图标
   - 侧边栏实现辅助功能
   - 工作区实现主要功能

3. 资源管理：
   - 合理管理插件资源
   - 及时清理不需要的资源
   - 实现适当的错误处理

## 依赖关系

- 核心框架：
  * Qt 框架
  * Python 标准库

- 插件系统：
  * 核心框架提供的接口
  * 插件特定的依赖

## 扩展机制

1. 插件管理：
   - 支持动态发现插件
   - 统一的注册机制
   - 完整的生命周期管理

2. 界面扩展：
   - 基于视图的界面组织
   - 灵活的布局管理
   - 统一的交互模式

3. 功能扩展：
   - 命令系统
   - 配置系统
   - 主题系统

## 后续规划

1. 完善插件系统：
   - 插件依赖管理
   - 版本控制
   - 热加载支持

2. 增强布局管理：
   - 布局状态持久化
   - 自定义布局支持
   - 多视图组织

3. 提升开发体验：
   - 完善开发文档
   - 提供开发模板
   - 增加调试支持