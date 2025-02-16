"""
配置注册表实现
"""
from typing import Any, Dict, Optional

class ConfigRegistry:
    """配置注册表"""
    
    def __init__(self) -> None:
        """初始化配置注册表"""
        self._configs: Dict[str, Dict] = {}
        self._values: Dict[str, Any] = {}
        
    def register(self, config: Dict[str, Any]) -> None:
        """注册配置模式"""
        # 深度合并配置
        self._merge_config(self._configs, config)
        
        # 初始化默认值
        self._initialize_defaults(config)
        
    def _merge_config(self, target: Dict, source: Dict) -> None:
        """深度合并字典"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict):
                if isinstance(value, dict):
                    self._merge_config(target[key], value)
                else:
                    target[key] = value
            else:
                target[key] = value
                
    def _initialize_defaults(self, config: Dict) -> None:
        """初始化默认值"""
        def init_defaults(path: str, cfg: Dict) -> None:
            for key, value in cfg.items():
                full_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    if "default" in value:
                        self._values[full_path] = value["default"]
                    else:
                        init_defaults(full_path, value)
                        
        init_defaults("", config)
        
    def get(self, path: str, default: Any = None) -> Any:
        """获取配置值"""
        # 如果路径直接存在于值中，返回它
        if path in self._values:
            return self._values[path]
            
        # 否则尝试查找配置节点
        node = self._configs
        for part in path.split('.'):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return default
                
        # 如果找到的节点是一个有默认值的配置项
        if isinstance(node, dict) and "default" in node:
            return node["default"]
            
        # 如果是一个普通字典，返回整个字典
        if isinstance(node, dict):
            return node
            
        return default
        
    def set(self, path: str, value: Any) -> None:
        """设置配置值"""
        self._values[path] = value
        
    def get_schema(self, path: str = "") -> Optional[Dict]:
        """获取配置模式"""
        if not path:
            return self._configs
            
        node = self._configs
        for part in path.split('.'):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None
                
        return node if isinstance(node, dict) else None