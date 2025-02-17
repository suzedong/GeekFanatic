"""
编辑器功能测试模块
"""
import pytest
from PySide6.QtCore import QObject

from geek_fanatic.core.command import CommandRegistry
from geek_fanatic.plugins.editor.buffer import TextBuffer
from geek_fanatic.plugins.editor.commands.basic import (
    DeleteCommand,
    RedoCommand,
    SelectAllCommand,
    UndoCommand,
)
from geek_fanatic.plugins.editor.commands.search import (
    FindCommand,
    ReplaceAllCommand,
    ReplaceCommand,
)
from geek_fanatic.plugins.editor.editor import Editor
from geek_fanatic.plugins.editor.features.folding import CodeFolding
from geek_fanatic.plugins.editor.features.highlight import SyntaxHighlight
from geek_fanatic.plugins.editor.features.indent import CodeIndent
from geek_fanatic.plugins.editor.types import Position


class MockGeekFanatic:
    """模拟的 GeekFanatic 实例"""
    
    def __init__(self) -> None:
        self.command_registry = CommandRegistry()
        self.config_registry = {
            "editor": {
                "font": {
                    "family": "Consolas",
                    "size": 14
                },
                "indentation": "spaces",
                "tabSize": 4
            }
        }
        
    def get_config(self, path: str) -> dict:
        """获取配置"""
        return self.config_registry.get(path, {})

@pytest.fixture
def mock_ide():
    """创建模拟的 IDE 实例"""
    return MockGeekFanatic()

@pytest.fixture
def editor(mock_ide):
    """创建编辑器实例"""
    editor = Editor(ide=mock_ide)
    editor._ide = mock_ide
    return editor

def test_editor_initialization(editor):
    """测试编辑器初始化"""
    assert editor.content == ""
    assert editor.cursor_line == 0
    assert editor.cursor_column == 0
    assert not editor.has_selection()

def test_insert_text(editor):
    """测试文本插入"""
    editor.insert_text("Hello")
    assert editor.content == "Hello"
    assert editor.cursor_line == 0
    assert editor.cursor_column == 5
    
    # 测试多行插入
    editor.set_cursor_position(0, 5)
    editor.insert_text("\nWorld")
    assert editor.content == "Hello\nWorld"
    assert editor.cursor_line == 1
    assert editor.cursor_column == 5

def test_delete_text(editor):
    """测试文本删除"""
    editor.insert_text("Hello World")
    editor.set_cursor_position(0, 5)
    DeleteCommand().execute(editor)
    assert editor.content == "HelloWorld"
    
    # 测试选中删除
    editor.set_selection(0, 0, 0, 5)
    DeleteCommand().execute(editor)
    assert editor.content == "World"

def test_undo_redo(editor):
    """测试撤销重做"""
    # 插入文本
    editor.insert_text("Hello")
    assert editor.content == "Hello"
    
    # 撤销
    UndoCommand().execute(editor)
    assert editor.content == ""
    
    # 重做
    RedoCommand().execute(editor)
    assert editor.content == "Hello"

def test_select_all(editor):
    """测试全选"""
    editor.insert_text("Hello\nWorld")
    SelectAllCommand().execute(editor)
    assert editor.has_selection()
    assert editor._selection == (Position(0, 0), Position(1, 5))

def test_find_command(editor):
    """测试查找功能"""
    editor.insert_text("Hello World\nHello Python")
    find_cmd = FindCommand()
    
    # 基本查找
    find_cmd.execute(editor, "Hello")
    assert len(find_cmd._search_state.results) == 2
    assert find_cmd._search_state.current_index == 0
    assert editor.has_selection()
    
    # 大小写敏感查找
    find_cmd.execute(editor, "HELLO", case_sensitive=True)
    assert len(find_cmd._search_state.results) == 0
    
    # 正则表达式查找
    find_cmd.execute(editor, r"H\w+o", use_regex=True)
    assert len(find_cmd._search_state.results) == 2
    
    # 全词匹配
    find_cmd.execute(editor, "Hello", whole_word=True)
    assert len(find_cmd._search_state.results) == 2

def test_replace_command(editor):
    """测试替换功能"""
    editor.insert_text("Hello World\nHello Python")
    find_cmd = FindCommand()
    find_cmd.execute(editor, "Hello")
    
    # 替换单个
    replace_cmd = ReplaceCommand()
    replace_cmd.execute(editor, find_cmd, "Hi")
    assert editor.content == "Hi World\nHello Python"
    
    # 替换所有
    replace_all_cmd = ReplaceAllCommand()
    replace_all_cmd.execute(editor, find_cmd, "Hi")
    assert editor.content == "Hi World\nHi Python"

def test_folding_feature(editor):
    """测试代码折叠功能"""
    code = """def test():
    if True:
        print('test')
        print('more')
    return None"""
    editor.insert_text(code)
    
    folding = editor._features["folding"]
    folding.compute_folds()
    regions = folding.get_folding_regions()
    
    assert len(regions) >= 1
    # 'if True:' 块应该可以折叠
    assert any(r.start_line == 1 for r in regions)

def test_highlight_feature(editor):
    """测试语法高亮功能"""
    code = 'def test(x: int) -> str:\n    return str(x)'
    editor.insert_text(code)
    
    highlight = editor._features["highlight"]
    tokens = highlight.highlight_line(0)
    
    # 'def' 应该被识别为关键字
    assert any(t.type.name == "keyword" and t.text == "def" for t in tokens)
    # 'str' 应该被识别为内置函数
    assert any(t.text == "str" for t in tokens)

def test_indent_feature(editor):
    """测试代码缩进功能"""
    code = "def test():"
    editor.insert_text(code)
    
    indent = editor._features["indent"]
    # 冒号后应该增加缩进
    next_line_indent = indent.get_indent(1)
    
    if indent._use_spaces:
        assert len(next_line_indent) == indent._tab_size
    else:
        assert next_line_indent == "\t"
        
    # 测试减少缩进
    editor.insert_text("\n    return None")
    indent.unindent_line(1)
    assert editor._buffer.get_line(1) == "return None"

def test_multi_line_operations(editor):
    """测试多行操作"""
    # 插入多行
    editor.insert_text("Line 1\nLine 2\nLine 3")
    assert editor._buffer.get_line_count() == 3
    
    # 删除中间行
    # 选择从第一行末尾（包括换行符）到第二行末尾（包括换行符）
    editor.set_selection(0, 6, 2, 0)
    DeleteCommand().execute(editor)
    assert editor.content == "Line 1Line 3"

@pytest.mark.parametrize("text,line,col", [
    ("Hello", 0, 5),
    ("Hi\nWorld", 1, 5),
    ("One\nTwo\nThree", 2, 5)
])
def test_cursor_movement(editor, text, line, col):
    """测试光标移动"""
    editor.insert_text(text)
    assert editor.cursor_line == line
    assert editor.cursor_column == col