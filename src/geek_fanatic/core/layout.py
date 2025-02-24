"""
布局管理系统实现
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter

from .widgets.activity_bar import ActivityBar
from .widgets.side_bar import SideBar
from .widgets.work_area import WorkArea

class Layout:
    """布局管理器，负责管理主窗口的整体布局结构"""

    def __init__(self, window: QMainWindow) -> None:
        """初始化布局管理器

        Args:
            window: 主窗口实例
        """
        self._window = window
        self._setup_layout()

    def _setup_layout(self) -> None:
        """设置主布局"""
        # 创建中央部件
        central_widget = QWidget()
        self._window.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建分割器
        self._splitter = QSplitter()
        self._splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(self._splitter)

        # 创建核心部件
        self._activity_bar = ActivityBar()  # 活动栏（插件切换）
        self._side_bar = SideBar()         # 侧边栏（插件辅助内容）
        self._work_area = WorkArea()       # 工作区（插件主要功能）

        # 添加到分割器
        self._splitter.addWidget(self._activity_bar)
        self._splitter.addWidget(self._side_bar)
        self._splitter.addWidget(self._work_area)

        # 设置分割比例
        self._splitter.setStretchFactor(0, 0)  # 活动栏固定宽度
        self._splitter.setStretchFactor(1, 1)  # 侧边栏
        self._splitter.setStretchFactor(2, 4)  # 工作区

        # 设置初始尺寸
        self._activity_bar.setFixedWidth(48)
        self._side_bar.setMinimumWidth(200)

        # 连接信号
        self._connect_signals()

    def _connect_signals(self) -> None:
        """连接信号"""
        # 活动栏项目点击时显示对应的侧边栏视图
        self._activity_bar.itemClicked.connect(self._on_activity_item_clicked)
        
        # 侧边栏视图变更时更新活动栏状态
        self._side_bar.viewChanged.connect(self._on_side_view_changed)

    def _on_activity_item_clicked(self, item_id: str) -> None:
        """处理活动栏项目点击
        
        切换到对应插件的视图和功能区
        """
        # 更新侧边栏视图
        self._side_bar.set_current_view(item_id)
        # TODO: 通知插件系统切换工作区内容

    def _on_side_view_changed(self, view_id: str) -> None:
        """处理侧边栏视图变更"""
        self._activity_bar.set_active_item(view_id)

    @property
    def activity_bar(self) -> ActivityBar:
        """获取活动栏"""
        return self._activity_bar

    @property
    def side_bar(self) -> SideBar:
        """获取侧边栏"""
        return self._side_bar

    @property
    def work_area(self) -> WorkArea:
        """获取工作区"""
        return self._work_area

    def save_layout(self) -> None:
        """保存布局状态"""
        # TODO: 实现布局状态的保存

    def restore_layout(self) -> None:
        """恢复布局状态"""
        # TODO: 实现布局状态的恢复

    def reset_layout(self) -> None:
        """重置布局到默认状态"""
        self._activity_bar.setFixedWidth(48)
        self._side_bar.setMinimumWidth(200)
        sizes = [48, 200, self._splitter.width() - 248]
        self._splitter.setSizes(sizes)