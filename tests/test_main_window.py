"""
主窗口测试模块
"""

import pytest
from PySide6.QtWidgets import QApplication, QLabel

from geek_fanatic.ui.main_window import MainWindow


@pytest.fixture
def app(qapp):
    """提供Qt应用程序实例"""
    qapp.setApplicationName("GeekFanatic")
    return qapp


@pytest.fixture
def main_window(app):
    """提供主窗口实例"""
    window = MainWindow()
    return window


def test_window_title(main_window):
    """测试窗口标题"""
    assert main_window.windowTitle() == "GeekFanatic"


def test_window_geometry(main_window):
    """测试窗口几何属性"""
    assert main_window.width() == 1280
    assert main_window.height() == 800


def test_status_bar(main_window):
    """测试状态栏"""
    status_bar = main_window.statusBar()
    assert status_bar is not None
    assert status_bar.height() == 22

    # 获取状态栏中的标签
    labels = [widget for widget in status_bar.children() if isinstance(widget, QLabel)]
    assert len(labels) > 0
    assert labels[0].text() == "就绪"
