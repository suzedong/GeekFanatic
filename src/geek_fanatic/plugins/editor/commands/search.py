"""
查找和替换命令实现
"""
from dataclasses import dataclass
import re
from typing import List, Optional, Tuple

from PySide6.QtCore import QObject

from geek_fanatic.core.command import Command, command
from geek_fanatic.plugins.editor.editor import Editor
from geek_fanatic.plugins.editor.types import Position

@dataclass
class SearchResult:
    """搜索结果"""
    start: Position
    end: Position
    text: str

class SearchState:
    """搜索状态"""
    def __init__(self) -> None:
        self.query: str = ""
        self.results: List[SearchResult] = []
        self.current_index: int = -1
        self.case_sensitive: bool = False
        self.use_regex: bool = False
        self.whole_word: bool = False

@command("editor.find")
class FindCommand(Command):
    """查找命令"""
    
    def __init__(self) -> None:
        super().__init__()
        self._search_state = SearchState()
        
    def execute(self, editor: Editor, query: str,
                case_sensitive: bool = False,
                use_regex: bool = False,
                whole_word: bool = False) -> None:
        """执行查找命令"""
        self._search_state.query = query
        self._search_state.case_sensitive = case_sensitive
        self._search_state.use_regex = use_regex
        self._search_state.whole_word = whole_word
        
        # 清空旧的搜索结果
        self._search_state.results.clear()
        self._search_state.current_index = -1
        
        if not query:
            return
            
        # 构建搜索模式
        if use_regex:
            try:
                pattern = re.compile(query, 0 if case_sensitive else re.IGNORECASE)
            except re.error:
                return
        else:
            pattern = re.compile(
                re.escape(query),
                0 if case_sensitive else re.IGNORECASE
            )
            
        # 在每一行中搜索
        for line_num, line in enumerate(editor._buffer._content):
            for match in pattern.finditer(line):
                if whole_word:
                    # 检查单词边界
                    if (match.start() > 0 and 
                        line[match.start() - 1].isalnum()):
                        continue
                    if (match.end() < len(line) and 
                        line[match.end()].isalnum()):
                        continue
                        
                self._search_state.results.append(
                    SearchResult(
                        Position(line_num, match.start()),
                        Position(line_num, match.end()),
                        match.group()
                    )
                )
                
        if self._search_state.results:
            self._search_state.current_index = 0
            self._select_current_result(editor)
            
    def find_next(self, editor: Editor) -> None:
        """查找下一个"""
        if not self._search_state.results:
            return
            
        self._search_state.current_index = (
            (self._search_state.current_index + 1) % 
            len(self._search_state.results)
        )
        self._select_current_result(editor)
        
    def find_previous(self, editor: Editor) -> None:
        """查找上一个"""
        if not self._search_state.results:
            return
            
        self._search_state.current_index = (
            (self._search_state.current_index - 1) % 
            len(self._search_state.results)
        )
        self._select_current_result(editor)
        
    def _select_current_result(self, editor: Editor) -> None:
        """选中当前搜索结果"""
        result = self._search_state.results[self._search_state.current_index]
        editor.set_selection(
            result.start.line,
            result.start.column,
            result.end.line,
            result.end.column
        )

@command("editor.replace")
class ReplaceCommand(Command):
    """替换命令"""
    
    def execute(self, editor: Editor, 
                find_command: FindCommand,
                replace_text: str) -> None:
        """执行替换命令"""
        if not find_command._search_state.results:
            return
            
        # 获取当前搜索结果
        current = find_command._search_state.results[
            find_command._search_state.current_index
        ]
        
        # 替换文本
        editor.set_selection(
            current.start.line,
            current.start.column,
            current.end.line,
            current.end.column
        )
        editor.insert_text(replace_text)
        
        # 更新搜索结果
        find_command.execute(
            editor,
            find_command._search_state.query,
            find_command._search_state.case_sensitive,
            find_command._search_state.use_regex,
            find_command._search_state.whole_word
        )

@command("editor.replaceAll")
class ReplaceAllCommand(Command):
    """全部替换命令"""
    
    def execute(self, editor: Editor,
                find_command: FindCommand,
                replace_text: str) -> None:
        """执行全部替换命令"""
        if not find_command._search_state.results:
            return
            
        # 从后向前替换，以避免位置改变影响结果
        for result in reversed(find_command._search_state.results):
            editor.set_selection(
                result.start.line,
                result.start.column,
                result.end.line,
                result.end.column
            )
            editor.insert_text(replace_text)
            
        # 清空搜索结果
        find_command._search_state.results.clear()
        find_command._search_state.current_index = -1