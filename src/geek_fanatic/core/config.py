"""
配置系统实现
"""

from typing import Any, Dict, Optional

from PySide6.QtCore import QObject


class ConfigRegistry(QObject):
    """配置注册表"""

    def __init__(self):
        """初始化配置注册表"""
        super().__init__()
        self._config: Dict[str, Any] = {}
        self._schema: Dict[str, Any] = {}

    def register(self, schema: Dict[str, Any]) -> None:
        """注册配置模式"""
        self._schema.update(schema)

    def unregister(self, key: str) -> None:
        """注销配置"""
        if key in self._schema:
            del self._schema[key]
            if key in self._config:
                del self._config[key]

    def set(self, key: str, value: Any) -> None:
        """设置配置项的值"""
        # TODO: 根据schema验证值
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项的值"""
        return self._config.get(key, default)

    def get_schema(self, key: str) -> Optional[Dict[str, Any]]:
        """获取配置项的模式"""
        return self._schema.get(key)

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
