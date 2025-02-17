"""
基本编辑器命令
"""

from geek_fanatic.core.command import Command


class DeleteCommand(Command):
    def __init__(self) -> None:
        super().__init__("editor.delete", "删除选中内容")

    def execute(self) -> None:
        pass


class UndoCommand(Command):
    def __init__(self) -> None:
        super().__init__("editor.undo", "撤销")

    def execute(self) -> None:
        pass


class RedoCommand(Command):
    def __init__(self) -> None:
        super().__init__("editor.redo", "重做")

    def execute(self) -> None:
        pass
