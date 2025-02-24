#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基础编辑器命令模块
"""

from typing import Optional

from ....core.command import Command, command
from ..editor import Editor

@command("editor.delete")
class DeleteCommand(Command):
    """删除命令"""
    
    def execute(self, editor: Optional[Editor] = None) -> None:
        if editor is None or not hasattr(editor, 'delete_at_cursor'):
            return
            
        if editor.has_selection():
            editor.delete_selection()
        else:
            editor.delete_at_cursor()

@command("editor.undo")
class UndoCommand(Command):
    """撤销命令"""
    
    def execute(self, editor: Optional[Editor] = None) -> None:
        if editor is None:
            return
            
        editor.undo()

@command("editor.redo")
class RedoCommand(Command):
    """重做命令"""
    
    def execute(self, editor: Optional[Editor] = None) -> None:
        if editor is None:
            return
            
        editor.redo()

@command("editor.clear_selection")
class ClearSelectionCommand(Command):
    """清除选择命令"""
    
    def execute(self, editor: Optional[Editor] = None) -> None:
        if editor is None:
            return
            
        editor.clear_selection()
