"""
语法高亮功能实现
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Pattern, Tuple, TYPE_CHECKING, cast, Any, Callable

# pylint: disable=no-name-in-module,import-error
from PySide6 import QtCore
from PySide6.QtCore import QObject
from PySide6.QtGui import QColor, QTextCharFormat

from geek_fanatic.plugins.editor.features import EditorFeature
from geek_fanatic.plugins.editor.buffer import TextBuffer

if TYPE_CHECKING:
    from geek_fanatic.plugins.editor.editor import Editor

@dataclass
class TokenType:
    """标记类型"""

    name: str  # 标记名称
    pattern: str  # 匹配模式
    color: str  # 颜色值

    def __post_init__(self) -> None:
        """初始化后处理

        编译正则表达式以提高性能
        """
        self.regex: Pattern[str] = re.compile(self.pattern)

@dataclass
class Token:
    """语法标记"""

    type: TokenType  # 标记类型
    text: str  # 标记文本
    start: int  # 起始位置
    end: int  # 结束位置

class SyntaxHighlight(EditorFeature):
    """语法高亮功能实现"""

    def __init__(self, editor: "Editor") -> None:
        """初始化语法高亮

        Args:
            editor: 编辑器实例
        """
        super().__init__(editor)
        self._token_types: Dict[str, TokenType] = {}
        self._formats: Dict[str, QTextCharFormat] = {}
        self._current_language: Optional[str] = None

        # 初始化默认标记类型
        self._initialize_default_tokens()

    def initialize(self) -> None:
        """初始化功能"""
        # 连接文本改变信号
        # 注：这里使用动态方式连接信号，避免类型检查问题
        try:
            content_changed = getattr(self._editor, "contentChanged", None)
            if content_changed is not None and callable(getattr(content_changed, "connect", None)):
                # 使用动态调用避免类型检查
                getattr(content_changed, "connect")(self._rehighlight)
        except (AttributeError, TypeError):
            pass

    def cleanup(self) -> None:
        """清理功能"""
        self._token_types.clear()
        self._formats.clear()

    def _initialize_default_tokens(self) -> None:
        """初始化默认标记类型"""
        # Python 关键字
        self.register_token_type(
            TokenType(
                "keyword",
                r"\b(def|class|if|else|for|while|return|import|from|in|is|not|and|or"
                r"|True|False|None|try|except|finally|raise|with|as|assert|break|continue"
                r"|global|lambda|pass|yield)\b",
                "#0000FF",
            )
        )
        # 字符串
        self.register_token_type(
            TokenType(
                "string",
                r'"[^"]*"|\'[^\']*\'',
                "#008000"
            )
        )
        # 数字
        self.register_token_type(
            TokenType(
                "number",
                r"\b\d+(\.\d+)?\b",
                "#800000"
            )
        )
        # 注释
        self.register_token_type(
            TokenType(
                "comment",
                r"#[^\n]*",
                "#808080"
            )
        )
        # 内置函数
        self.register_token_type(
            TokenType(
                "builtin",
                r"\b(print|len|str|int|float|list|dict|set|tuple|range|enumerate|zip"
                r"|map|filter|sorted|any|all|sum|min|max|abs|round|type|isinstance"
                r"|hasattr|getattr|setattr|delattr)\b",
                "#800080",
            )
        )

    def register_token_type(self, token_type: TokenType) -> None:
        """注册标记类型

        Args:
            token_type: 要注册的标记类型
        """
        self._token_types[token_type.name] = token_type

        # 创建对应的文本格式
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(token_type.color))
        self._formats[token_type.name] = text_format

    def set_language(self, language: str) -> None:
        """设置当前语言

        Args:
            language: 语言标识符
        """
        if language != self._current_language:
            self._current_language = language
            # TODO: 加载语言特定的标记类型
            self._rehighlight()

    def _rehighlight(self) -> None:
        """重新高亮所有文本"""
        if hasattr(self._editor, "content"):
            content = getattr(self._editor, "content")
            if isinstance(content, str):
                lines = content.split("\n")
                for line_num, line in enumerate(lines):
                    self.highlight_line(line_num)

    def highlight_line(self, line_number: int) -> List[Token]:
        """高亮单行文本

        Args:
            line_number: 行号

        Returns:
            List[Token]: 识别出的标记列表
        """
        if hasattr(self._editor, "_buffer"):
            buffer = getattr(self._editor, "_buffer")
            if isinstance(buffer, TextBuffer):
                line = buffer.get_line(line_number)
                tokens = self._tokenize_line(line)
                # 应用高亮
                self.apply_highlighting(line_number, tokens)
                return tokens
        return []

    def _tokenize_line(self, line: str) -> List[Token]:
        """对单行文本进行词法分析

        Args:
            line: 要分析的文本行

        Returns:
            List[Token]: 识别出的标记列表
        """
        tokens: List[Token] = []

        # 对每种标记类型进行匹配
        for token_type in self._token_types.values():
            for match in token_type.regex.finditer(line):
                tokens.append(
                    Token(
                        type=token_type,
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                    )
                )

        # 按开始位置排序
        tokens.sort(key=lambda t: t.start)
        return tokens

    def get_format(self, token_type: str) -> Optional[QTextCharFormat]:
        """获取标记类型对应的文本格式

        Args:
            token_type: 标记类型名称

        Returns:
            Optional[QTextCharFormat]: 对应的文本格式，如果不存在则返回None
        """
        return self._formats.get(token_type)

    def apply_highlighting(self, line_number: int, tokens: List[Token]) -> None:
        """应用高亮效果

        Args:
            line_number: 行号
            tokens: 要应用高亮的标记列表
        """
        # 这个方法将由 QML 文本组件调用来设置文本格式
        pass
