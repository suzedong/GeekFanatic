"""
命令系统实现
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class Command(ABC):
    """命令基类"""

    def __init__(self, id: str, description: str = "") -> None:
        """初始化命令"""
        self.id = id
        self.description = description

    @abstractmethod
    def execute(self) -> None:
        """执行命令"""
        pass


class CommandRegistry:
    """命令注册表"""

    def __init__(self):
        """初始化命令注册表"""
        self._commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        """注册命令"""
        self._commands[command.id] = command

    def unregister(self, command_id: str) -> None:
        """注销命令"""
        if command_id in self._commands:
            del self._commands[command_id]

    def execute(self, command_id: str) -> None:
        """执行命令"""
        if command_id in self._commands:
            self._commands[command_id].execute()

    def get_command(self, command_id: str) -> Optional[Command]:
        """获取命令"""
        return self._commands.get(command_id)

    def get_all_commands(self) -> List[Command]:
        """获取所有命令"""
        return list(self._commands.values())
