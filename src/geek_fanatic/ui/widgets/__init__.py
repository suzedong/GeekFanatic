# -*- coding: utf-8 -*-
"""UI 组件模块

本模块包含应用程序的所有 UI 组件实现，包括主窗口和各种对话框。
"""

from .dialogs import FileDialogs, FindReplaceDialog, SettingsDialog
from .main_window import MainWindow

__all__ = ["MainWindow", "FileDialogs", "FindReplaceDialog", "SettingsDialog"]
