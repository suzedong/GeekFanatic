"""
通用对话框实现
"""

from typing import List, Optional, Tuple, cast, Any, Union

# pylint: disable=no-name-in-module,import-error
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class FileDialogs:
    """文件对话框静态方法集合"""

    @staticmethod
    def get_open_file_name(
        parent: Optional[QWidget] = None,
        caption: str = "打开文件",
        directory: str = "",
        filter: str = "所有文件 (*.*)",
    ) -> Optional[str]:
        """显示打开文件对话框

        Args:
            parent: 父窗口
            caption: 对话框标题
            directory: 初始目录
            filter: 文件过滤器

        Returns:
            如果用户选择了文件则返回文件路径，否则返回 None
        """
        parent_widget = parent if parent is not None else QWidget()
        file_name, _ = QFileDialog.getOpenFileName(cast(QWidget, parent_widget), caption, directory, filter)
        return file_name if file_name else None

    @staticmethod
    def get_save_file_name(
        parent: Optional[QWidget] = None,
        caption: str = "保存文件",
        directory: str = "",
        filter: str = "所有文件 (*.*)",
    ) -> Optional[str]:
        """显示保存文件对话框

        Args:
            parent: 父窗口
            caption: 对话框标题
            directory: 初始目录
            filter: 文件过滤器

        Returns:
            如果用户选择了保存位置则返回文件路径，否则返回 None
        """
        parent_widget = parent if parent is not None else QWidget()
        file_name, _ = QFileDialog.getSaveFileName(cast(QWidget, parent_widget), caption, directory, filter)
        return file_name if file_name else None

class FindReplaceDialog(QDialog):
    """查找替换对话框"""

    # 信号定义
    findNext = Signal(str, bool, bool)  # 查找文本，区分大小写，使用正则
    replace = Signal(str, str)  # 查找文本，替换文本
    replaceAll = Signal(str, str)  # 查找文本，替换文本

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化查找替换对话框

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("查找和替换")

        # 初始化控件
        self.find_edit: QLineEdit
        self.replace_edit: QLineEdit
        self.case_sensitive: QPushButton
        self.use_regex: QPushButton
        self.find_next_btn: QPushButton
        self.replace_btn: QPushButton
        self.replace_all_btn: QPushButton
        self.close_btn: QPushButton

        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置界面"""
        layout = QVBoxLayout(self)

        # 查找部分
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("查找："))
        self.find_edit = QLineEdit()
        find_layout.addWidget(self.find_edit)
        layout.addLayout(find_layout)

        # 替换部分
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("替换为："))
        self.replace_edit = QLineEdit()
        replace_layout.addWidget(self.replace_edit)
        layout.addLayout(replace_layout)

        # 选项
        self.case_sensitive = QPushButton("区分大小写")
        self.case_sensitive.setCheckable(True)
        self.use_regex = QPushButton("使用正则表达式")
        self.use_regex.setCheckable(True)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.use_regex)
        layout.addLayout(options_layout)

        # 按钮
        button_box = QDialogButtonBox()
        
        # 创建按钮并确保类型安全
        next_btn = button_box.addButton(
            "查找下一个", QDialogButtonBox.ButtonRole.ActionRole
        )
        self.find_next_btn = cast(QPushButton, next_btn) if next_btn else QPushButton("查找下一个")
            
        replace_btn = button_box.addButton(
            "替换", QDialogButtonBox.ButtonRole.ActionRole
        )
        self.replace_btn = cast(QPushButton, replace_btn) if replace_btn else QPushButton("替换")
            
        replace_all_btn = button_box.addButton(
            "全部替换", QDialogButtonBox.ButtonRole.ActionRole
        )
        self.replace_all_btn = cast(QPushButton, replace_all_btn) if replace_all_btn else QPushButton("全部替换")
            
        close_btn = button_box.addButton(
            QDialogButtonBox.StandardButton.Close
        )
        self.close_btn = cast(QPushButton, close_btn) if close_btn else QPushButton("关闭")

        layout.addWidget(button_box)

        # 连接信号
        self.find_next_btn.clicked.connect(self._find_next)
        self.replace_btn.clicked.connect(self._replace)
        self.replace_all_btn.clicked.connect(self._replace_all)
        self.close_btn.clicked.connect(self.close)

    def _find_next(self) -> None:
        """查找下一个匹配项"""
        text = self.find_edit.text()
        if text:
            self.findNext.emit(
                text, self.case_sensitive.isChecked(), self.use_regex.isChecked()
            )

    def _replace(self) -> None:
        """替换当前匹配项"""
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        if find_text:
            self.replace.emit(find_text, replace_text)

    def _replace_all(self) -> None:
        """替换所有匹配项"""
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        if find_text:
            self.replaceAll.emit(find_text, replace_text)

class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化设置对话框

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("设置")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置界面"""
        layout = QVBoxLayout(self)

        # TODO: 添加设置项
        layout.addWidget(QLabel("设置对话框"))

        # 按钮
        buttons = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
