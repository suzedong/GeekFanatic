"""
命令系统实现
"""

from abc import ABC, abstractmethod
from functools import wraps
from typing import Dict, List, Optional, Type, TypeVar, cast

T = TypeVar('T', bound='Command')

def command(command_id: str) -> callable:
    """命令装饰器
    
    用于标记和注册命令类。
    
    Args:
        command_id: 命令ID
        
    Returns:
        装饰后的命令类
    """
    def decorator(cls: Type[T]) -> Type[T]:
        @wraps(cls)
        def wrapper(*args, **kwargs) -> T:
            instance = cls(*args, **kwargs)
            instance.id = command_id
            return instance
        return cast(Type[T], wrapper)
    return decorator

class Command(ABC):
    """命令基类"""

    def __init__(self, description: str = "") -> None:
        """初始化命令"""
        self.id: str = ""  # 由装饰器设置
        self.description = description

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        """执行命令
        
        子类可以定义自己的参数列表。
        """
        pass

class CommandRegistry:
    """命令注册表"""

    def __init__(self) -> None:
        """初始化命令注册表"""
        self._commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        """注册命令"""
        self._commands[command.id] = command

    def unregister(self, command_id: str) -> None:
        """注销命令"""
        if command_id in self._commands:
            del self._commands[command_id]

    def execute(self, command_id: str, *args, **kwargs) -> None:
        """执行命令"""
        if command_id in self._commands:
            self._commands[command_id].execute(*args, **kwargs)

    def get_command(self, command_id: str) -> Optional[Command]:
        """获取命令"""
        return self._commands.get(command_id)

    def get_all_commands(self) -> List[Command]:
        """获取所有命令"""
        return list(self._commands.values())
