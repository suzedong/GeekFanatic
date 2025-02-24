"""
配置系统实现
"""

from typing import Any, Dict, Optional, TypeVar, Union, cast, TypedDict, Callable

# pylint: disable=no-name-in-module,import-error
from PySide6 import QtCore
from PySide6.QtCore import QObject

T = TypeVar('T')

class SchemaDict(TypedDict, total=False):
    """配置模式字典类型"""
    type: type
    default: Any
    description: str

class ValidatedSchemaDict(SchemaDict):
    """带验证器的配置模式类型"""
    validator: Optional[Callable[[Any], bool]]

SchemaType = Dict[str, ValidatedSchemaDict]

class ConfigValue:
    """配置值包装器"""

    def __init__(self, value: Any, schema: Optional[ValidatedSchemaDict] = None) -> None:
        """初始化配置值包装器

        Args:
            value: 配置值
            schema: 配置模式，用于验证值
        """
        self.value = value
        self.schema = schema or cast(ValidatedSchemaDict, {})

    def validate(self) -> bool:
        """验证值是否符合模式

        Returns:
            bool: 验证是否通过
        """
        if not self.schema:
            return True

        try:
            # 检查类型
            expected_type = self.schema.get('type')
            if expected_type and not isinstance(self.value, expected_type):
                return False

            # 调用验证器
            validator = self.schema.get('validator')
            if validator and callable(validator):
                validation_result = validator(self.value)
                return bool(validation_result)

            return True
            
        except Exception:
            return False

    def get_value(self, expected_type: type[T]) -> Optional[T]:
        """获取类型安全的值

        Args:
            expected_type: 期望的值类型

        Returns:
            Optional[T]: 如果值类型匹配则返回，否则返回 None
        """
        return cast(T, self.value) if isinstance(self.value, expected_type) else None

class ConfigRegistry(QObject):
    """配置注册表"""

    def __init__(self) -> None:
        """初始化配置注册表"""
        super().__init__()
        self._config: Dict[str, ConfigValue] = {}
        self._schema: SchemaType = {}

    def register(self, schema: Dict[str, ValidatedSchemaDict]) -> None:
        """注册配置模式

        Args:
            schema: 配置模式定义
        
        示例:
            ```python
            registry.register({
                "editor.fontSize": {
                    "type": int,
                    "default": 14,
                    "description": "Editor font size in points"
                }
            })
            ```
        """
        validated_schema = {
            key: cast(ValidatedSchemaDict, value) 
            for key, value in schema.items()
            if isinstance(value, dict) and 'type' in value
        }
        self._schema.update(validated_schema)

    def unregister(self, key: str) -> None:
        """注销配置

        Args:
            key: 配置键
        """
        if key in self._schema:
            del self._schema[key]
            self._config.pop(key, None)

    def set(self, key: str, value: Any) -> bool:
        """设置配置项的值

        Args:
            key: 配置键
            value: 配置值

        Returns:
            bool: 设置是否成功
        """
        try:
            schema = self._schema.get(key)
            config_value = ConfigValue(value, schema)
            
            # 验证值是否符合模式
            if not config_value.validate():
                return False
                
            self._config[key] = config_value
            return True
        except Exception:
            return False

    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """获取配置项的值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            Optional[T]: 配置值，如果不存在则返回默认值
        """
        config_value = self._config.get(key)
        if config_value is not None:
            return cast(T, config_value.value)
        
        # 如果未设置值，查找模式中的默认值
        schema = self._schema.get(key)
        if schema and 'default' in schema:
            return cast(T, schema['default'])
            
        return default

    def get_typed(self, key: str, expected_type: type[T], default: Optional[T] = None) -> Optional[T]:
        """获取类型安全的配置值

        Args:
            key: 配置键
            expected_type: 期望的值类型
            default: 默认值

        Returns:
            Optional[T]: 配置值，如果不存在或类型不匹配则返回默认值
        """
        config_value = self._config.get(key)
        if config_value is not None:
            return config_value.get_value(expected_type) or default
            
        # 如果未设置值，查找模式中的默认值
        schema = self._schema.get(key)
        if schema and 'default' in schema:
            default_value = schema['default']
            if isinstance(default_value, expected_type):
                return cast(T, default_value)
                
        return default

    def get_schema(self, key: str) -> Optional[ValidatedSchemaDict]:
        """获取配置项的模式

        Args:
            key: 配置键

        Returns:
            Optional[ValidatedSchemaDict]: 配置模式，如果不存在则返回 None
        """
        return self._schema.get(key)

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置

        Returns:
            Dict[str, Any]: 所有配置的副本
        """
        result_dict: Dict[str, Any] = {}
        for key in self._schema:
            value = self.get(key)
            if value is not None:
                result_dict[key] = value
        return result_dict

    def validate_all(self) -> bool:
        """验证所有配置值

        Returns:
            bool: 所有配置是否都有效
        """
        return all(
            config_value.validate()
            for config_value in self._config.values()
        )

    def merge(self, other: Dict[str, Any]) -> bool:
        """合并配置

        Args:
            other: 要合并的配置字典

        Returns:
            bool: 合并是否成功
        """
        try:
            for key, value in other.items():
                if not self.set(key, value):
                    return False
            return True
        except Exception:
            return False

    def clear(self) -> None:
        """清空所有配置"""
        self._config.clear()
        self._schema.clear()
