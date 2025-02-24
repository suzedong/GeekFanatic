"""
工作区域组件实现
"""

from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSplitter
)

class WorkTab(QWidget):
    """工作区标签页"""

    # 信号定义
    closeRequested = Signal(str)  # 关闭请求信号，参数为标签页ID

    def __init__(
        self,
        tab_id: str,
        title: str,
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化工作区标签页

        Args:
            tab_id: 标签页唯一标识
            title: 标签页标题
            parent: 父组件
        """
        super().__init__(parent)
        self.tab_id = tab_id
        self.title = title
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        title_bar = QWidget()
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 5, 10, 5)
        
        # 标题
        title_label = QLabel(self.title)
        title_layout.addWidget(title_label)
        
        # 关闭按钮
        close_button = QPushButton("×")
        close_button.setFixedSize(16, 16)
        close_button.clicked.connect(lambda: self.closeRequested.emit(self.tab_id))
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #CCCCCC;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        title_layout.addWidget(close_button)
        
        layout.addWidget(title_bar)
        
        # 内容区域
        self._content = QWidget()
        content_layout = QVBoxLayout(self._content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        layout.addWidget(self._content)

    @property
    def content_widget(self) -> QWidget:
        """获取内容区域组件"""
        return self._content

class WorkGroup(QWidget):
    """工作区组
    
    管理一组工作区标签页
    """

    # 信号定义
    tabChanged = Signal(str)  # 标签页切换信号，参数为标签页ID
    tabClosed = Signal(str)   # 标签页关闭信号，参数为标签页ID

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化工作区组"""
        super().__init__(parent)
        self._tabs: Dict[str, WorkTab] = {}
        self._tab_index_map: Dict[int, str] = {}  # 索引到tab_id的映射
        self._current_tab: Optional[str] = None
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标签页容器
        self._tab_widget = QTabWidget()
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.setMovable(True)
        self._tab_widget.setDocumentMode(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self._tab_widget.currentChanged.connect(self._on_current_changed)
        
        layout.addWidget(self._tab_widget)

    def add_tab(self, tab: WorkTab) -> None:
        """添加标签页"""
        if tab.tab_id in self._tabs:
            return

        self._tabs[tab.tab_id] = tab
        index = self._tab_widget.addTab(tab, tab.title)
        self._tab_index_map[index] = tab.tab_id
        tab.closeRequested.connect(lambda tab_id: self._on_tab_close_requested_by_id(tab_id))

    def remove_tab(self, tab_id: str) -> None:
        """移除标签页"""
        if tab_id not in self._tabs:
            return

        tab = self._tabs.pop(tab_id)
        index = self._tab_widget.indexOf(tab)
        self._tab_widget.removeTab(index)
        self._tab_index_map.pop(index, None)
        
        if self._current_tab == tab_id:
            self._current_tab = None

    def _on_tab_close_requested(self, index: int) -> None:
        """处理标签页关闭请求"""
        tab_id = self._tab_index_map.get(index)
        if tab_id:
            self._on_tab_close_requested_by_id(tab_id)

    def _on_tab_close_requested_by_id(self, tab_id: str) -> None:
        """通过ID处理标签页关闭请求"""
        self.tabClosed.emit(tab_id)
        self.remove_tab(tab_id)

    def _on_current_changed(self, index: int) -> None:
        """处理当前标签页变化"""
        tab_id = self._tab_index_map.get(index)
        if tab_id:
            self._current_tab = tab_id
            self.tabChanged.emit(tab_id)

class WorkArea(QWidget):
    """工作区域组件
    
    提供插件功能区域显示，包括：
    - 多工作区组支持
    - 标签页管理
    - 拖拽分割
    """

    # 信号定义
    activeGroupChanged = Signal(str)  # 活动工作区组变更信号
    activeTabChanged = Signal(str)    # 活动标签页变更信号

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化工作区域"""
        super().__init__(parent)
        self._groups: Dict[str, WorkGroup] = {}
        self._active_group: Optional[str] = None
        
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self) -> None:
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建分割器
        self._splitter = QSplitter()
        self._splitter.setOrientation(Qt.Orientation.Horizontal)
        layout.addWidget(self._splitter)

        # 创建初始工作区组
        self.add_group("main")

    def _setup_style(self) -> None:
        """设置样式"""
        self.setStyleSheet("""
            WorkArea {
                background: #1E1E1E;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background: #2D2D2D;
                color: #CCCCCC;
                padding: 5px 10px;
                border: none;
                border-right: 1px solid #1E1E1E;
            }
            QTabBar::tab:selected {
                background: #1E1E1E;
            }
            QTabBar::tab:hover {
                background: #3D3D3D;
            }
        """)

    def add_group(self, group_id: str) -> None:
        """添加工作区组"""
        if group_id in self._groups:
            return

        group = WorkGroup()
        self._groups[group_id] = group
        self._splitter.addWidget(group)
        
        # 连接信号
        group.tabChanged.connect(lambda tab_id: self.activeTabChanged.emit(tab_id))
        
        # 如果是第一个组，设置为活动组
        if len(self._groups) == 1:
            self.set_active_group(group_id)

    def remove_group(self, group_id: str) -> None:
        """移除工作区组"""
        if group_id not in self._groups:
            return

        group = self._groups.pop(group_id)
        self._splitter.removeWidget(group)
        
        if self._active_group == group_id:
            next_group = next(iter(self._groups)) if self._groups else None
            if next_group:
                self.set_active_group(next_group)
            self._active_group = None

    def set_active_group(self, group_id: str) -> None:
        """设置活动工作区组"""
        if group_id not in self._groups:
            return

        self._active_group = group_id
        self.activeGroupChanged.emit(group_id)

    def get_active_group(self) -> Optional[str]:
        """获取活动工作区组ID"""
        return self._active_group

    def add_tab(self, group_id: str, tab: WorkTab) -> None:
        """添加标签页到指定工作区组"""
        if group_id not in self._groups:
            return

        group = self._groups[group_id]
        group.add_tab(tab)

    def remove_tab(self, group_id: str, tab_id: str) -> None:
        """从指定工作区组移除标签页"""
        if group_id not in self._groups:
            return

        group = self._groups[group_id]
        group.remove_tab(tab_id)

    def get_group(self, group_id: str) -> Optional[WorkGroup]:
        """获取指定工作区组"""
        return self._groups.get(group_id)