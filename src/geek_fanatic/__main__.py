"""
GeekFanatic IDE 主入口
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 修改为相对导入
from .core.app import GeekFanatic
from .plugins.editor.ui.widgets.editor import Editor

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget,
    QHBoxLayout, QSplitter, QTextEdit, QTreeView, QDockWidget, QMenuBar,
    QStatusBar, QToolBar, QFrame, QFileSystemModel
)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self, ide):
        super().__init__()
        self.ide = ide
        self.setWindowTitle("GeekFanatic")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._setup_styles()
        self._connect_signals()
        
    def _setup_ui(self):
        """设置界面"""
        # 创建菜单栏
        self._create_menu_bar()
        
        # 创建工具栏
        self._create_tool_bar()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 创建左侧导航面板
        nav_panel = QFrame()
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建文件树
        self.file_tree = QTreeView()
        self.file_tree.setHeaderHidden(True)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(QDir.currentPath()))
        # 只显示文件名
        self.file_tree.hideColumn(1)  # 大小
        self.file_tree.hideColumn(2)  # 类型
        self.file_tree.hideColumn(3)  # 修改时间
        nav_layout.addWidget(self.file_tree)
        
        splitter.addWidget(nav_panel)
        
        # 创建编辑区域
        editor_panel = QFrame()
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        self.editor = Editor()
        editor_layout.addWidget(self.editor)
        
        splitter.addWidget(editor_panel)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)  # 导航面板
        splitter.setStretchFactor(1, 4)  # 编辑区域
        
    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("&File")
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        file_menu.addAction(self.new_action)
        
        self.open_action = QAction("Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)
        
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        file_menu.addAction(self.save_action)
        
        file_menu.addSeparator()
        self.exit_action = QAction("Exit", self)
        file_menu.addAction(self.exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("&Edit")
        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(self.cut_action)
        
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(self.copy_action)
        
        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(self.paste_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("&View")
        self.toggle_tree_action = QAction("Toggle File Tree", self)
        view_menu.addAction(self.toggle_tree_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("&Help")
        self.about_action = QAction("About", self)
        help_menu.addAction(self.about_action)
        
    def _create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        
        self.run_action = QAction("Run", self)
        toolbar.addAction(self.run_action)
        
        self.debug_action = QAction("Debug", self)
        toolbar.addAction(self.debug_action)
        
    def _connect_signals(self):
        """连接信号"""
        # 文件树
        self.file_tree.clicked.connect(self._on_file_clicked)
        
        # 编辑器
        self.editor.cursorPositionChanged.connect(self._on_cursor_position_changed)
        
        # 菜单动作
        self.new_action.triggered.connect(self._on_new)
        self.open_action.triggered.connect(self._on_open)
        self.save_action.triggered.connect(self._on_save)
        self.exit_action.triggered.connect(self.close)
        
    def _setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QToolBar {
                background-color: #2d2d2d;
                border: none;
            }
            QToolButton {
                color: white;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: #3d3d3d;
            }
            QTreeView {
                background-color: #252526;
                color: white;
                border: none;
            }
            QTreeView::item:selected {
                background-color: #094771;
            }
            QStatusBar {
                background-color: #007acc;
                color: white;
            }
            QFrame {
                background-color: #1e1e1e;
                border: none;
            }
        """)
        
    def _on_file_clicked(self, index):
        """处理文件点击"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.statusBar.showMessage(f"Loaded: {file_path}")
            except Exception as e:
                self.statusBar.showMessage(f"Error loading file: {str(e)}")
        
    def _on_cursor_position_changed(self, line: int, column: int):
        """处理光标位置变化"""
        self.statusBar.showMessage(f"Line: {line}, Column: {column}")
        
    def _on_new(self):
        """新建文件"""
        self.editor.clear()
        self.statusBar.showMessage("New file created")
        
    def _on_open(self):
        """打开文件"""
        self.statusBar.showMessage("Open file...")
        
    def _on_save(self):
        """保存文件"""
        self.statusBar.showMessage("File saved")

def main():
    """应用程序主入口"""
    # 添加源代码目录到Python路径
    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, src_path)
    
    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setApplicationName("GeekFanatic")
    app.setOrganizationName("GeekFanatic")
    
    try:
        # 创建核心实例
        ide = GeekFanatic()
        
        # 初始化插件系统
        ide.initialize_plugins()
        
        # 创建并显示主窗口
        window = MainWindow(ide)
        window.show()
        
        return app.exec()
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())