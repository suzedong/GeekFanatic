"""
编辑器插件安装配置
"""

from typing import Type
from geek_fanatic.core.plugin import Plugin
from geek_fanatic.plugins.editor import EditorPlugin

def get_plugin_id() -> str:
    """获取插件ID

    Returns:
        str: 插件的唯一标识符
    """
    return "geekfanatic.editor"

def get_plugin_class() -> Type[Plugin]:
    """获取插件类

    Returns:
        Type[Plugin]: 插件类
    """
    return EditorPlugin
