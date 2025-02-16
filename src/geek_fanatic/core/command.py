"""
命令系统核心模块
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Type

class Command(ABC):
    """命令基类"""
    
    @property
    def id(self) -> str:
        """获取命令ID"""
        return self.__class__._command_id  # type: ignore
        
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> None:
        """执行命令"""
        pass

def command(command_id: str) -> Callable[[Type[Command]], Type[Command]]:
    """命令注册装饰器"""
    def decorator(cls: Type[Command]) -> Type[Command]:
        cls._command_id = command_id  # type: ignore
        return cls
    return decorator

class CommandRegistry:
    """命令注册表"""
    
    def __init__(self) -> None:
        """初始化命令注册表"""
        self._commands: Dict[str, Command] = {}
        
    def register(self, command: Command) -> None:
        """注册命令"""
        self._commands[command.id] = command
        
    def get(self, command_id: str) -> Optional[Command]:
        """获取命令"""
        return self._commands.get(command_id)
        
    def execute(self, command_id: str, *args: Any, **kwargs: Any) -> None:
        """执行命令"""
        command = self.get(command_id)
        if command is None:
            raise ValueError(f"未找到命令: {command_id}")
        command.execute(*args, **kwargs)