"""
应用程序测试模块
"""
import pytest

from geek_fanatic import GeekFanatic
from geek_fanatic.core.theme import ThemeManager
from geek_fanatic.core.window import WindowManager
from geek_fanatic.core.plugin import PluginManager

@pytest.fixture
def app():
    """提供应用程序核心实例"""
    return GeekFanatic()

def test_app_managers(app):
    """测试应用程序管理器实例"""
    assert app.theme_manager is not None
    assert isinstance(app.theme_manager, ThemeManager)
    assert app.window_manager is not None
    assert isinstance(app.window_manager, WindowManager)
    assert app.plugin_manager is not None
    assert isinstance(app.plugin_manager, PluginManager)

def test_app_plugin_system(app):
    """测试插件系统"""
    # 初始化时没有加载任何插件
    assert not app.is_plugin_loaded("test_plugin")
    
    # 插件信息查询返回空字符串
    assert app.get_plugin_info("test_plugin") == ""