"""
布局管理系统实现
"""

from typing import Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QStackedWidget
)

from .widgets.activity_bar import ActivityBar
from .widgets.side_bar import SideBar
from .widgets.work_area import WorkArea
from .plugin import PluginViews
from .view import ViewRegistry, ViewInfo, ViewType

class Layout:
    """布局管理器，负责管理主窗口的整体布局结构"""

    def __init__(self, window: QMainWindow, view_registry: ViewRegistry) -> None:
        """初始化布局管理器

        Args:
            window: 主窗口实例
            view_registry: 视图注册表实例
        """
        self._window = window
        self._view_registry = view_registry
        self._current_plugin: Optional[str] = None
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
        # 活动栏项目点击时显示对应的视图
        self._activity_bar.itemClicked.connect(self._on_activity_item_clicked)
        
        # 侧边栏视图变更时更新活动栏状态
        self._side_bar.viewChanged.connect(self._on_side_view_changed)

    def register_plugin_views(self, plugin_id: str, views: PluginViews) -> None:
        """注册插件视图

        Args:
            plugin_id: 插件ID
            views: 插件视图集合
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"正在注册插件视图: {plugin_id}")
        
        # 注册活动栏图标
        for icon in views.activity_icons:
            logger.info(f"注册活动栏图标: {icon.id}")
            
            # 注册到 ViewRegistry
            self._view_registry.register_view(
                icon.id,
                icon.tooltip,
                icon.icon,
                priority=0 if not icon.bottom else -1
            )
            
            # 添加到活动栏
            self._activity_bar.add_item(
                icon.id,
                icon.icon,
                icon.tooltip,
                icon.bottom
            )
            
        # 注册侧边栏视图
        for view_id, component in views.side_views.items():
            logger.info(f"注册侧边栏视图: {view_id}")
            
            # 注册侧边栏视图组件
            self._view_registry.register_view(
                view_id,  # 不再使用 .side 后缀
                view_id,  # 使用相同的 ID 作为标题
                component
            )
            
        # 注册工作区视图
        for view_id, component in views.work_views.items():
            logger.info(f"注册工作区视图: {view_id}")
            
            self._view_registry.register_view(
                view_id,  # 不再使用 .work 后缀
                view_id,
                component
            )
            
        # 如果是第一个插件，自动显示它的视图
        if not self._current_plugin and views.activity_icons:
            first_view_id = views.activity_icons[0].id
            logger.info(f"切换到第一个视图: {first_view_id}")
            self.switch_to_view(first_view_id)
            self._current_plugin = plugin_id

    def switch_to_view(self, view_id: str) -> None:
        """切换到指定视图

        Args:
            view_id: 视图ID
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"切换到视图: {view_id}")
        
        # 获取视图信息
        view_info = self._view_registry.get_view(view_id)
        if not view_info:
            logger.warning(f"未找到视图: {view_id}")
            return
            
        # 更新活动栏
        logger.debug("更新活动栏状态")
        self._activity_bar.set_active_item(view_id)
        
        # 更新侧边栏
        side_view = self._view_registry.get_view(view_id)
        if side_view and view_id in self._view_registry._views:
            logger.debug(f"更新侧边栏视图: {view_id}")
            self._side_bar.clear()
            self._side_bar.add_view(side_view["component"], view_id)
            self._side_bar.set_current_view(view_id)
        else:
            logger.debug(f"未找到侧边栏视图: {view_id}")
            
        # 更新工作区
        work_views = {}
        for vid, view in self._view_registry._views.items():
            if view["type"] == ViewType.WIDGET and "editor" in vid:
                work_views[vid] = view["component"]
                logger.debug(f"添加工作区视图: {vid}")
                
        if work_views:
            logger.debug(f"切换工作区视图: {list(work_views.keys())}")
            self._work_area.switch_to_plugin_views(work_views)
        else:
            logger.debug("未找到工作区视图")

    def _on_activity_item_clicked(self, item_id: str) -> None:
        """处理活动栏项目点击
        
        Args:
            item_id: 点击的项目ID
        """
        self.switch_to_view(item_id)

    def _on_side_view_changed(self, view_id: str) -> None:
        """处理侧边栏视图变更
        
        Args:
            view_id: 变更的视图ID
        """
        # 当用户在侧边栏切换视图时，更新对应的活动栏状态
        self._activity_bar.set_active_item(view_id.replace(".side", ""))

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
        pass

    def restore_layout(self) -> None:
        """恢复布局状态"""
        # TODO: 实现布局状态的恢复
        pass

    def reset_layout(self) -> None:
        """重置布局到默认状态"""
        self._activity_bar.setFixedWidth(48)
        self._side_bar.setMinimumWidth(200)
        sizes = [48, 200, self._splitter.width() - 248]
        self._splitter.setSizes(sizes)