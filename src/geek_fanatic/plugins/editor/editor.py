"""
编辑器核心实现
"""
from typing import Dict, List, Optional, Tuple, Any

from PySide6.QtCore import Property, Signal, QObject, Qt, Slot

from geek_fanatic.plugins.editor.buffer import TextBuffer
from geek_fanatic.plugins.editor.features.folding import CodeFolding
from geek_fanatic.plugins.editor.features.highlight import SyntaxHighlight
from geek_fanatic.plugins.editor.features.indent import CodeIndent
from geek_fanatic.plugins.editor.types import Position

class Editor(QObject):
    """编辑器核心实现"""
    
    # 信号定义
    contentChanged = Signal()
    selectionChanged = Signal()
    cursorPositionChanged = Signal(int, int)  # line, column
    
    def __init__(self, ide: Optional[Any] = None) -> None:
        """初始化编辑器"""
        super().__init__()
        self._ide = ide
        self._buffer = TextBuffer()
        self._features: Dict[str, 'EditorFeature'] = {}
        self._cursor_position = Position(0, 0)
        self._selection: Optional[Tuple[Position, Position]] = None
        
        # 初始化编辑器功能
        self.initialize_features()
        
        # 连接信号
        self._buffer.contentChanged.connect(self.contentChanged)
        
    def initialize_features(self) -> None:
        """初始化编辑器功能"""
        self._features["folding"] = CodeFolding(self)
        self._features["highlight"] = SyntaxHighlight(self)
        self._features["indent"] = CodeIndent(self)
        
        # 初始化所有功能
        for feature in self._features.values():
            feature.initialize()
        
    @Property(str)
    def content(self) -> str:
        """获取编辑器内容"""
        return self._buffer.get_content()
        
    @Slot(str)
    def set_content(self, content: str) -> None:
        """设置编辑器内容"""
        self._buffer.set_content(content)
        
    @Property(int)
    def cursor_line(self) -> int:
        """获取光标所在行"""
        return self._cursor_position.line
        
    @Property(int)
    def cursor_column(self) -> int:
        """获取光标所在列"""
        return self._cursor_position.column
        
    @Slot(int, int)
    def set_cursor_position(self, line: int, column: int) -> None:
        """设置光标位置"""
        old_pos = self._cursor_position
        self._cursor_position = Position(line, column)
        if old_pos.line != line or old_pos.column != column:
            self.cursorPositionChanged.emit(line, column)
            
    def has_selection(self) -> bool:
        """是否有选中文本"""
        return self._selection is not None
        
    @Slot(int, int, int, int)
    def set_selection(self, start_line: int, start_col: int,
                     end_line: int, end_col: int) -> None:
        """设置选中区域"""
        old_selection = self._selection
        self._selection = (
            Position(start_line, start_col),
            Position(end_line, end_col)
        )
        if old_selection != self._selection:
            self.selectionChanged.emit()
            
    def clear_selection(self) -> None:
        """清除选中"""
        if self._selection:
            self._selection = None
            self.selectionChanged.emit()
            
    @Slot(str)
    def insert_text(self, text: str) -> None:
        """插入文本"""
        if self.has_selection():
            # 如果有选中文本，先删除选中内容
            self.delete_selection()
            
        self._buffer.insert(self._cursor_position, text)
        
        # 更新光标位置
        lines = text.split('\n')
        if len(lines) > 1:
            # 多行插入
            new_line = self._cursor_position.line + len(lines) - 1
            new_col = len(lines[-1])
        else:
            # 单行插入
            new_line = self._cursor_position.line
            new_col = self._cursor_position.column + len(text)
            
        self.set_cursor_position(new_line, new_col)
        
    def delete_selection(self) -> None:
        """删除选中文本"""
        if not self.has_selection():
            return
            
        assert self._selection is not None
        start, end = self._selection
        self._buffer.delete(start, end)
        self.set_cursor_position(start.line, start.column)
        self.clear_selection()
        
    @Slot()
    def delete_at_cursor(self) -> None:
        """删除光标处的字符"""
        if self.has_selection():
            self.delete_selection()
        else:
            current_line = self._buffer.get_line(self._cursor_position.line)
            if self._cursor_position.column < len(current_line):
                # 删除当前位置的字符
                end_pos = Position(
                    self._cursor_position.line,
                    self._cursor_position.column + 1
                )
                self._buffer.delete(self._cursor_position, end_pos)
            elif self._cursor_position.line < self._buffer.get_line_count() - 1:
                # 删除行尾换行符
                end_pos = Position(
                    self._cursor_position.line + 1,
                    0
                )
                self._buffer.delete(self._cursor_position, end_pos)
            
    def cleanup(self) -> None:
        """清理编辑器资源"""
        # 清理所有功能
        for feature in self._features.values():
            feature.cleanup()
        self._features.clear()
        
        # 清理缓冲区
        self._buffer = TextBuffer()
        self._cursor_position = Position(0, 0)
        self._selection = None