"""
基础编辑命令实现
"""
from typing import Any, Optional

from PySide6.QtCore import QObject

from geek_fanatic.core.command import Command, command
from geek_fanatic.plugins.editor.editor import Editor

@command("editor.delete")
class DeleteCommand(Command):
    """删除命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行删除命令"""
        if editor.has_selection():
            editor.delete_selection()
        else:
            editor.delete_at_cursor()

@command("editor.undo")
class UndoCommand(Command):
    """撤销命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行撤销命令"""
        editor._buffer.undo()

@command("editor.redo")
class RedoCommand(Command):
    """重做命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行重做命令"""
        editor._buffer.redo()

@command("editor.selectAll")
class SelectAllCommand(Command):
    """全选命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行全选命令"""
        content = editor.content
        if not content:
            return
            
        lines = content.split('\n')
        last_line = len(lines) - 1
        last_col = len(lines[last_line])
        editor.set_selection(0, 0, last_line, last_col)

@command("editor.copy")
class CopyCommand(Command):
    """复制命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行复制命令"""
        if not editor.has_selection():
            return
            
        # 此处应调用系统剪贴板API
        # 暂时通过编辑器内部缓存实现
        editor._clipboard = editor._buffer._get_text(
            editor._selection[0],
            editor._selection[1]
        )

@command("editor.paste")
class PasteCommand(Command):
    """粘贴命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行粘贴命令"""
        # 此处应调用系统剪贴板API
        # 暂时通过编辑器内部缓存实现
        if hasattr(editor, '_clipboard'):
            editor.insert_text(editor._clipboard)

@command("editor.cut")
class CutCommand(Command):
    """剪切命令"""
    
    def execute(self, editor: Editor) -> None:
        """执行剪切命令"""
        if not editor.has_selection():
            return
            
        # 先复制
        CopyCommand().execute(editor)
        # 再删除
        editor.delete_selection()