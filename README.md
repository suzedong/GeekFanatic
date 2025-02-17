# GeekFanatic IDE

一个现代化的 Python 集成开发环境。

## 特性

- 基于 Qt 6 构建的现代界面
  * 使用 QtWidgets 构建主界面
  * 使用 QML 实现高级编辑器功能
- 强大的代码编辑功能
  * 代码折叠
  * 语法高亮
  * 智能缩进
- 插件系统支持
- 主题系统支持
- 完整的开发工具
  * 集成终端
  * 文件浏览器
  * 搜索与替换
  * 源代码管理集成

## 系统要求

- Python 3.9.6
- Qt 6.6.1
- 支持的操作系统：Windows, Linux, macOS

## 安装

使用 Poetry 安装：

```bash
poetry install
```

## 开发

### 环境设置

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/geekfanatic.git
cd geekfanatic
```

2. 安装依赖：
```bash
poetry install
```

### 运行开发版本

```bash
poetry run python -m geek_fanatic
```

### 运行测试

```bash
poetry run pytest
```

## 项目结构

```
src/geek_fanatic/
├── core/               # 核心功能模块
│   ├── app.py         # 应用程序核心
│   ├── command.py     # 命令系统
│   ├── config.py      # 配置管理
│   ├── plugin.py      # 插件系统
│   ├── theme.py       # 主题系统
│   ├── view.py        # 视图管理
│   └── window.py      # 窗口管理
├── plugins/           # 插件系统
│   └── editor/       # 编辑器插件
│       ├── features/  # 编辑器功能
│       ├── commands/  # 编辑器命令
│       └── ui/       # 编辑器界面
├── ui/               # 用户界面
│   ├── widgets/     # Qt 部件
│   └── resources/   # 资源文件
└── __main__.py      # 程序入口
```

## 代码规范

- 使用 Python 3.9.6
- 使用类型注解（Type Hints）增强代码可读性和安全性
  ```python
  def add_numbers(a: int, b: int) -> int:
      """对两个整数进行相加"""
      return a + b
  
  def get_user_name() -> str:
      """获取用户名"""
      return "张三"

  class User:
      def __init__(self, name: str, age: int):
          self.name = name
          self.age = age
  ```
- 使用 f-strings 进行字符串格式化（更简洁的字符串插值语法）
  ```python
  name = "张三"
  age = 25
  # 推荐使用 f-strings
  message = f"用户 {name} 的年龄是 {age} 岁"  # 简洁易读
  
  # 不推荐使用旧式格式化
  old_message = "用户 {} 的年龄是 {} 岁".format(name, age)  # 较繁琐
  old_message2 = "用户 %s 的年龄是 %d 岁" % (name, age)     # 更繁琐
  
  # f-strings 还支持表达式
  price = 19.99
  count = 3
  total = f"总价：¥{price * count:.2f}"  # 可以包含表达式和格式说明符
  ```
- 使用 Black 进行代码格式化（自动统一代码风格）
  ```python
  # 格式化前的代码：格式不统一，难以阅读
  def calculate_total(prices,discount_rate = 0.1,   tax_rate=0.05):
      subtotal=sum(  prices)
      discount=subtotal*discount_rate
      tax=(subtotal-discount)*tax_rate
      return subtotal-discount+tax

  # 使用 Black 格式化后的代码：格式统一，易于阅读
  def calculate_total(
      prices,
      discount_rate=0.1,
      tax_rate=0.05,
  ):
      subtotal = sum(prices)
      discount = subtotal * discount_rate
      tax = (subtotal - discount) * tax_rate
      return subtotal - discount + tax
  
  # Black 会自动处理：
  # - 适当的空格和换行
  # - 一致的缩进
  # - 统一的引号使用
  # - 规范的参数列表格式
  # - PEP 8 规范的最大行长度
  ```
- 使用 isort 进行导入排序（自动组织 Python 的 import 语句）
  ```python
  # 排序前的导入语句：混乱无序
  import sys
  from typing import List
  import os
  from PyQt6.QtCore import *
  import json
  from datetime import datetime
  from .utils import helper
  import random
  from PyQt6.QtWidgets import QMainWindow
  
  # 使用 isort 排序后的导入语句：结构清晰
  import json
  import os
  import random
  import sys
  from datetime import datetime
  from typing import List
  
  from PyQt6.QtCore import (    # 第三方库按字母顺序排列
      QSize,
      Qt,
      pyqtSignal,
  )
  from PyQt6.QtWidgets import QMainWindow
  
  from .utils import helper     # 本地模块最后导入
  
  # isort 会自动：
  # - 按类型分组（标准库、第三方库、本地模块）
  # - 每组内按字母顺序排序
  # - 移除未使用的导入
  # - 合并相同模块的导入
  # - 保持代码整洁一致
  ```
- 使用 mypy 进行静态类型检查（在运行前发现类型错误）
  ```python
  # 有类型错误的代码
  def get_user_age(name: str) -> int:
      ages = {"张三": "25"}  # 错误：值的类型与返回类型不匹配
      return ages[name]      # mypy 会报错，因为试图返回 str 而不是 int

  # mypy 错误信息：
  # error: Incompatible return value type (got "str", expected "int")

  # 修复后的代码
  def get_user_age(name: str) -> int:
      ages = {"张三": 25}    # 正确：值的类型为 int
      return ages[name]

  # 更多 mypy 类型检查示例
  from typing import List, Dict, Optional

  class UserManager:
      def __init__(self) -> None:
          self.users: Dict[str, int] = {}    # 类型注解：字典的键为str，值为int
      
      def add_user(self, name: str, age: int) -> None:
          self.users[name] = age    # 正确：类型匹配
          
      def get_user_age(self, name: str) -> Optional[int]:
          return self.users.get(name)    # 正确：可能返回 None
      
      def get_users_list(self) -> List[str]:
          return list(self.users.keys())    # 正确：返回字符串列表

  # mypy 可以检查出的常见错误：
  # 1. 类型不匹配
  # 2. 可能的 None 值未处理
  # 3. 参数类型错误
  # 4. 返回类型错误
  # 5. 属性访问错误
  # 6. 容器类型错误
  ```
- 使用 pylint/flake8 进行代码质量检查
- 使用中文注释和文档
- 遵循 PEP 8 编码规范（Python 官方代码风格指南）
  ```python
  # 不符合 PEP 8 规范的代码
  class userManager:                         # 类名应使用 CamelCase
      def __init__ ( self,name ):           # 参数周围不应有空格
          self.Name=name                    # 变量名应使用 snake_case
  
      def GetUserInfo(self):                # 方法名应使用 snake_case
          return{'name':self.Name}          # 字典键后应有空格
  
      def set_user_age( self, Age:int ):    # 参数周围不应有空格
          self.user_age=Age                 # 等号两边应有空格
  
  
  # 符合 PEP 8 规范的代码
  class UserManager:
      """用户管理类。
      
      用于处理用户信息的管理操作。
      """
      
      def __init__(self, name: str):
          """初始化用户管理器。
          
          Args:
              name: 用户名
          """
          self.name = name
      
      def get_user_info(self) -> dict:
          """获取用户信息。
          
          Returns:
              包含用户信息的字典
          """
          return {"name": self.name}
      
      def set_user_age(self, age: int) -> None:
          """设置用户年龄。
          
          Args:
              age: 用户年龄
          """
          self.user_age = age
  
  # PEP 8 主要规范：
  # 1. 代码布局
  #    - 使用 4 个空格缩进
  #    - 每行最大长度 79 字符
  #    - 顶层函数和类定义用两个空行分隔
  #    - 方法定义用一个空行分隔
  #
  # 2. 命名规范
  #    - 函数名、变量名、模块名：snake_case
  #    - 类名：CamelCase
  #    - 常量：UPPER_CASE
  #    - 不使用单字母名称，除了计数器和迭代器
  #
  # 3. 表达式和语句
  #    - 在二元运算符两边各加一个空格
  #    - 不要在函数调用的()内加空格
  #    - 逗号、冒号、分号之后要加空格
  #
  # 4. 导入
  #    - 每个导入应该独占一行
  #    - 导入顺序：标准库 > 第三方库 > 本地库
  #    - 避免使用通配符导入（from module import *）
  #
  # 5. 注释
  #    - 注释应该是完整的句子
  #    - 行内注释应该至少用两个空格和代码分开
  #    - 每个函数都应该有文档字符串
  ```

### 执行代码检查

在提交代码前，请确保运行以下代码检查：

1. 格式化代码（使用 Black）：
```bash
# 检查代码格式但不修改
poetry run black --check src tests

# 自动修复代码格式
poetry run black src tests
```

2. 排序导入语句（使用 isort）：
```bash
# 检查导入语句排序但不修改
poetry run isort --check-only src tests

# 自动修复导入语句排序
poetry run isort src tests
```

3. 静态类型检查（使用 mypy）：
```bash
# 检查整个项目的类型注解
poetry run mypy src

# 严格模式检查
poetry run mypy src --strict

# 检查特定文件
poetry run mypy src/geek_fanatic/core/app.py
```

4. 代码质量检查（使用 pylint）：
```bash
# 检查 src 目录
poetry run pylint src

# 检查 tests 目录
poetry run pylint tests

# 检查特定文件
poetry run pylint src/geek_fanatic/core/app.py
```

5. 代码风格检查（使用 flake8）：
```bash
# 检查整个项目
poetry run flake8 src tests

# 检查特定目录
poetry run flake8 src/geek_fanatic/core

# 生成错误报告
poetry run flake8 src tests --output-file=flake8_report.txt
```

6. 一键执行所有检查：
```bash
# 顺序执行所有检查（建议在提交前运行）
poetry run black --check src tests && \
poetry run isort --check-only src tests && \
poetry run mypy src --strict && \
poetry run pylint src tests && \
poetry run flake8 src tests
```

常见错误代码说明：
- BLACK: 代码格式不符合 Black 标准
- ISORT: 导入语句顺序不规范
- MYPY: 类型检查错误
  * 返回类型不匹配
  * 参数类型错误
  * 可能的 None 值未处理
  * 容器类型不正确
- pylint 错误代码：
  * C：违反编码规范（如 C0103 命名不规范）
  * R：代码重构建议（如 R0903 方法太少）
  * W：编程警告（如 W0311 缩进不规范）
  * E：编程错误（如 E0401 导入错误）
- flake8 错误代码：
  * E***/W***: pycodestyle 错误和警告
  * F***: PyFlakes 错误
  * C9**: McCabe 复杂度检查

## 贡献

1. Fork 此仓库
2. 创建您的功能分支：`git checkout -b feature/amazing-feature`
3. 提交您的更改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 打开一个 Pull Request

## 许可证

此项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。