"""
搜索相关命令
"""
from geek_fanatic.core.command import Command


class FindCommand(Command):
    def __init__(self):
        super().__init__("editor.find", "查找")
        
    def execute(self):
        pass

class ReplaceCommand(Command):
    def __init__(self):
        super().__init__("editor.replace", "替换")
        
    def execute(self):
        pass