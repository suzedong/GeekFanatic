"""
搜索相关命令
"""

from geek_fanatic.core.command import Command


class FindCommand(Command):
    def __init__(self) -> None:
        super().__init__(id="editor.find", description="查找")

    def execute(self) -> None:
        pass


class ReplaceCommand(Command):
    def __init__(self) -> None:
        super().__init__(id="editor.replace", description="替换")

    def execute(self) -> None:
        pass
