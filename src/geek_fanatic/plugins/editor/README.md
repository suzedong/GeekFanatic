# GeekFanatic 编辑器插件

## 功能概述

编辑器插件是 GeekFanatic 的核心默认插件，提供基础的文本编辑功能，包括：

- 基本文本编辑（插入、删除等）
- 选择操作（选中、复制、剪切、粘贴）
- 撤销/重做支持
- 查找和替换功能

## 架构设计

插件采用模块化设计，主要包含以下组件：

### 1. 核心类

- `EditorPlugin`: 插件入口类，负责注册命令、配置和视图
- `Editor`: 编辑器核心类，处理文本编辑操作
- `TextBuffer`: 文本缓冲区类，管理文本内容和操作历史

### 2. 编辑命令

基础命令（basic.py）:
- `DeleteCommand`: 删除文本
- `UndoCommand`: 撤销操作
- `RedoCommand`: 重做操作
- `SelectAllCommand`: 全选文本
- `CopyCommand`: 复制文本
- `PasteCommand`: 粘贴文本
- `CutCommand`: 剪切文本

查找替换命令（search.py）:
- `FindCommand`: 查找文本
- `ReplaceCommand`: 替换文本
- `ReplaceAllCommand`: 全部替换

## 配置项

```json
{
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
```

## 快捷键

| 命令 | 快捷键 | 功能描述 |
|------|--------|----------|
| `editor.delete` | Delete | 删除光标后的字符或选中内容 |
| `editor.undo` | Ctrl+Z | 撤销上一步操作 |
| `editor.redo` | Ctrl+Y | 重做上一步操作 |
| `editor.selectAll` | Ctrl+A | 全选文本 |
| `editor.copy` | Ctrl+C | 复制选中内容 |
| `editor.paste` | Ctrl+V | 粘贴内容 |
| `editor.cut` | Ctrl+X | 剪切选中内容 |
| `editor.find` | Ctrl+F | 查找文本 |
| `editor.replace` | Ctrl+H | 替换文本 |

## 特性实现

### 文本操作

编辑器通过 `TextBuffer` 类管理文本内容，支持以下操作：
- 插入文本（单行/多行）
- 删除文本
- 撤销/重做操作历史
- 按行访问和修改内容

### 选择操作

支持多种选择模式：
- 普通选择（鼠标拖拽）
- 全文选择（Ctrl+A）
- 行选择（点击行号）
- 跨行选择

### 查找替换

查找功能支持：
- 普通文本查找
- 正则表达式匹配
- 大小写敏感
- 全词匹配
- 前向/后向查找

替换功能支持：
- 单个替换
- 全部替换
- 选区内替换

## 开发说明

### 添加新命令

1. 在 `commands` 目录下创建命令类
2. 使用 `@command` 装饰器注册命令
3. 实现 `execute` 方法

示例：
```python
@command("editor.newCommand")
class NewCommand(Command):
    def execute(self, editor: Editor) -> None:
        # 实现命令逻辑
        pass
```

### 添加新功能

1. 在 `features` 目录下创建功能类
2. 继承 `EditorFeature` 基类
3. 在 `Editor` 类中注册功能

### 单元测试

运行测试：
```bash
pytest tests/test_editor.py -v
```

所有核心功能都应该有对应的单元测试，包括：
- 基本文本操作测试
- 命令执行测试
- 边界条件测试
- 性能测试（大文件操作）

## 未来计划

1. 性能优化
   - 实现虚拟滚动
   - 大文件处理优化
   - 增量更新机制

2. 功能增强
   - 多光标支持
   - 代码折叠
   - 自动补全
   - 语法高亮

3. 可扩展性
   - 语言服务支持
   - 主题定制
   - 命令扩展机制