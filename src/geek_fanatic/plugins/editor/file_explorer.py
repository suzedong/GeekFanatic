"""
文件浏览器视图实现
"""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QDir, QFileInfo, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QFileSystemModel,
    QLabel
)

class FileExplorer(QWidget):
    """文件浏览器视图
    
    提供文件系统浏览功能。
    """
    
    # 信号定义
    fileSelected = Signal(str)  # 文件选择信号

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """初始化文件浏览器"""
        super().__init__(parent)
        self.setWindowTitle("资源管理器")
        self._setup_explorer()

    def _setup_explorer(self) -> None:
        """设置文件浏览器"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建文件系统模型
        self._model = QFileSystemModel()
        self._model.setRootPath(QDir.currentPath())
        
        # 设置过滤器
        self._model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)

        # 创建树视图
        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.setRootIndex(self._model.index(QDir.currentPath()))
        
        # 只显示文件名列
        self._tree.hideColumn(1)  # 大小
        self._tree.hideColumn(2)  # 类型
        self._tree.hideColumn(3)  # 修改日期
        
        # 设置样式
        self._tree.setStyleSheet("""
            QTreeView {
                background: #252526;
                border: none;
            }
            QTreeView::item {
                color: #CCCCCC;
                padding: 2px;
            }
            QTreeView::item:selected {
                background: #094771;
            }
            QTreeView::item:hover {
                background: #2A2D2E;
            }
        """)
        
        layout.addWidget(self._tree)
        
        # 连接信号
        self._tree.clicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, index) -> None:
        """处理项目点击事件"""
        file_path = self._model.filePath(index)
        if Path(file_path).is_file():
            self.fileSelected.emit(file_path)

    def set_root_path(self, path: str) -> None:
        """设置根路径
        
        Args:
            path: 根路径
        """
        self._model.setRootPath(path)
        self._tree.setRootIndex(self._model.index(path))

    def get_selected_path(self) -> Optional[str]:
        """获取选中的文件路径
        
        Returns:
            Optional[str]: 选中的文件路径，如果没有选中则返回None
        """
        indexes = self._tree.selectedIndexes()
        if not indexes:
            return None
            
        file_path = self._model.filePath(indexes[0])
        return file_path if Path(file_path).is_file() else None

    def expand_to_path(self, path: str) -> None:
        """展开到指定路径
        
        Args:
            path: 要展开到的路径
        """
        index = self._model.index(path)
        self._tree.expand(index)
        self._tree.scrollTo(index)