# GeekFanatic IDE

一个现代化的 Python 集成开发环境。

## 特性

- 基于 Qt 6 构建的现代界面
- 强大的代码编辑功能
- 插件系统支持
- 主题系统支持
- 完整的开发工具

## 系统要求

- Python 3.11+
- Qt 6.5+
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

3. 安装 pre-commit hooks：
```bash
poetry run pre-commit install
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
├── plugins/           # 插件系统
│   └── editor/       # 编辑器插件
├── ui/               # 用户界面
│   ├── widgets/     # Qt 部件
│   └── resources/   # 资源文件
└── __main__.py      # 程序入口
```

## 代码规范

- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 mypy 进行类型检查
- 遵循 PEP 8 编码规范
- 使用中文注释和文档

## 贡献

1. Fork 此仓库
2. 创建您的功能分支：`git checkout -b feature/amazing-feature`
3. 提交您的更改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 打开一个 Pull Request

## 许可证

此项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。