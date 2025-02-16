"""
代码缩进功能实现
"""
from dataclasses import dataclass
from typing import List, Optional, Pattern
import re

from PySide6.QtCore import QObject, Signal

from geek_fanatic.plugins.editor.types import Position
from geek_fanatic.plugins.editor.features import EditorFeature

@dataclass
class IndentRule:
    """缩进规则"""
    pattern: str  # 触发缩进的正则表达式
    indent_change: int  # 缩进变化量（正数增加，负数减少）
    
    def __post_init__(self) -> None:
        self.regex = re.compile(self.pattern)

class CodeIndent(EditorFeature):
    """代码缩进功能实现"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "tabSize": 4,
        "indentation": "spaces"
    }
    
    def __init__(self, editor: 'Editor') -> None:
        """初始化代码缩进"""
        super().__init__(editor)
        self._indent_rules: List[IndentRule] = []
        self._tab_size = self.DEFAULT_CONFIG["tabSize"]
        self._use_spaces = self.DEFAULT_CONFIG["indentation"] == "spaces"
        
        # 初始化默认缩进规则
        self._initialize_default_rules()
        
    def initialize(self) -> None:
        """初始化功能"""
        # 从配置中读取缩进设置
        if hasattr(self._editor, '_ide') and self._editor._ide is not None:
            config = self._editor._ide.config_registry.get("editor", {})
            if "tabSize" in config:
                self._tab_size = config["tabSize"]
            if "indentation" in config:
                self._use_spaces = config["indentation"] == "spaces"
                
    def cleanup(self) -> None:
        """清理功能"""
        self._indent_rules.clear()
        
    def _initialize_default_rules(self) -> None:
        """初始化默认缩进规则"""
        # Python 风格的缩进规则
        self.add_indent_rule(
            IndentRule(r":\s*$", 1)  # 冒号结尾增加缩进
        )
        self.add_indent_rule(
            IndentRule(r"^\s*return\b", -1)  # return 语句减少缩进
        )
        self.add_indent_rule(
            IndentRule(r"^\s*break\b", -1)  # break 语句减少缩进
        )
        self.add_indent_rule(
            IndentRule(r"^\s*continue\b", -1)  # continue 语句减少缩进
        )
        
    def add_indent_rule(self, rule: IndentRule) -> None:
        """添加缩进规则"""
        self._indent_rules.append(rule)
        
    def get_indent(self, line: int) -> str:
        """获取指定行的缩进"""
        if line <= 0:
            return ""
            
        # 获取上一行
        prev_line = self._editor._buffer.get_line(line - 1)
        if not prev_line.strip():
            return ""
            
        # 获取上一行的缩进
        current_indent = len(prev_line) - len(prev_line.lstrip())
        
        # 应用缩进规则
        indent_change = 0
        for rule in self._indent_rules:
            if rule.regex.search(prev_line):
                indent_change += rule.indent_change
                
        # 计算新的缩进级别
        new_indent = max(0, current_indent + indent_change * self._tab_size)
        
        # 根据设置返回空格或制表符
        if self._use_spaces:
            return " " * new_indent
        else:
            return "\t" * (new_indent // self._tab_size)
            
    def indent_line(self, line: int) -> None:
        """缩进指定行"""
        current_line = self._editor._buffer.get_line(line)
        indent = self.get_indent(line)
        
        # 删除现有缩进
        stripped_line = current_line.lstrip()
        self._editor._buffer.delete(
            Position(line, 0),
            Position(line, len(current_line) - len(stripped_line))
        )
        
        # 插入新缩进
        if indent:
            self._editor._buffer.insert(Position(line, 0), indent)
            
    def indent_selection(self) -> None:
        """缩进选中区域"""
        if not self._editor.has_selection():
            return
            
        selection = self._editor._selection
        assert selection is not None
        start, end = selection
        
        # 缩进每一行
        for line in range(start.line, end.line + 1):
            self.indent_line(line)
            
    def unindent_line(self, line: int) -> None:
        """减少指定行的缩进"""
        current_line = self._editor._buffer.get_line(line)
        if not current_line:
            return
            
        # 计算要删除的缩进量
        if self._use_spaces:
            # 删除一个缩进级别的空格
            spaces_to_remove = min(
                len(current_line) - len(current_line.lstrip()),
                self._tab_size
            )
            if spaces_to_remove > 0:
                self._editor._buffer.delete(
                    Position(line, 0),
                    Position(line, spaces_to_remove)
                )
        else:
            # 删除一个制表符
            if current_line.startswith('\t'):
                self._editor._buffer.delete(
                    Position(line, 0),
                    Position(line, 1)
                )
                
    def unindent_selection(self) -> None:
        """减少选中区域的缩进"""
        if not self._editor.has_selection():
            return
            
        selection = self._editor._selection
        assert selection is not None
        start, end = selection
        
        # 减少每一行的缩进
        for line in range(start.line, end.line + 1):
            self.unindent_line(line)