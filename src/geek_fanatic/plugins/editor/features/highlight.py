"""
语法高亮功能实现
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Pattern, Tuple
import re

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCharFormat, QColor

from geek_fanatic.plugins.editor.features import EditorFeature

@dataclass
class TokenType:
    """标记类型"""
    name: str
    pattern: str
    color: str
    
    def __post_init__(self) -> None:
        self.regex = re.compile(self.pattern)

@dataclass
class Token:
    """语法标记"""
    type: TokenType
    text: str
    start: int
    end: int

class SyntaxHighlight(EditorFeature):
    """语法高亮功能实现"""
    
    def __init__(self, editor: 'Editor') -> None:
        """初始化语法高亮"""
        super().__init__(editor)
        self._token_types: Dict[str, TokenType] = {}
        self._formats: Dict[str, QTextCharFormat] = {}
        self._current_language: Optional[str] = None
        
        # 初始化默认标记类型
        self._initialize_default_tokens()
        
    def initialize(self) -> None:
        """初始化功能"""
        # 连接文本改变信号
        self._editor.contentChanged.connect(self._rehighlight)
        
    def cleanup(self) -> None:
        """清理功能"""
        self._token_types.clear()
        self._formats.clear()
        
    def _initialize_default_tokens(self) -> None:
        """初始化默认标记类型"""
        self.register_token_type(
            TokenType("keyword", r"\b(def|class|if|else|for|while|return|import|from|in|is|not|and|or|True|False|None|try|except|finally|raise|with|as|assert|break|continue|global|lambda|pass|yield)\b", "#0000FF")
        )
        self.register_token_type(
            TokenType("string", r'"[^"]*"|\'[^\']*\'', "#008000")
        )
        self.register_token_type(
            TokenType("number", r"\b\d+(\.\d+)?\b", "#800000")
        )
        self.register_token_type(
            TokenType("comment", r"#[^\n]*", "#808080")
        )
        self.register_token_type(
            TokenType("builtin", r"\b(print|len|str|int|float|list|dict|set|tuple|range|enumerate|zip|map|filter|sorted|any|all|sum|min|max|abs|round|type|isinstance|hasattr|getattr|setattr|delattr)\b", "#800080")
        )
        
    def register_token_type(self, token_type: TokenType) -> None:
        """注册标记类型"""
        self._token_types[token_type.name] = token_type
        
        # 创建对应的文本格式
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(token_type.color))
        self._formats[token_type.name] = text_format
        
    def set_language(self, language: str) -> None:
        """设置当前语言"""
        if language != self._current_language:
            self._current_language = language
            # TODO: 加载语言特定的标记类型
            self._rehighlight()
            
    def _rehighlight(self) -> None:
        """重新高亮所有文本"""
        content = self._editor.content
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            self.highlight_line(line_num)
            
    def highlight_line(self, line_number: int) -> List[Token]:
        """高亮单行文本"""
        line = self._editor._buffer.get_line(line_number)
        tokens = self._tokenize_line(line)
        # 应用高亮
        self.apply_highlighting(line_number, tokens)
        return tokens
        
    def _tokenize_line(self, line: str) -> List[Token]:
        """对单行文本进行词法分析"""
        tokens: List[Token] = []
        
        # 对每种标记类型进行匹配
        for token_type in self._token_types.values():
            for match in token_type.regex.finditer(line):
                tokens.append(Token(
                    type=token_type,
                    text=match.group(),
                    start=match.start(),
                    end=match.end()
                ))
                
        # 按开始位置排序
        tokens.sort(key=lambda t: t.start)
        return tokens
        
    def get_format(self, token_type: str) -> Optional[QTextCharFormat]:
        """获取标记类型对应的文本格式"""
        return self._formats.get(token_type)
        
    def apply_highlighting(self, line_number: int, tokens: List[Token]) -> None:
        """应用高亮效果"""
        # 这个方法将由 QML 文本组件调用来设置文本格式
        pass