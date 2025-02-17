"""
主窗口实现
"""

from typing import Optional

from PySide6.QtCore import QDir, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileSystemModel,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSplitter,
    QStatusBar,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from geek_fanatic.plugins.editor.ui.widgets.editor import Editor

from .dialogs import FileDialogs, FindReplaceDialog, SettingsDialog


class MainWindow(QMainWindow):
    """主窗口"""

    # 信号定义
    fileOpened = Signal(str)  # 打开文件
    fileSaved = Signal(str)  # 保存文件

    def __init__(self, ide=None):
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
        self.statusBar.showMessage("就绪")

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
        file_menu = menubar.addMenu("文件(&F)")

        self.new_action = QAction("新建(&N)", self)
        self.new_action.setShortcut("Ctrl+N")
        file_menu.addAction(self.new_action)

        self.open_action = QAction("打开(&O)...", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)

        self.save_action = QAction("保存(&S)", self)
        self.save_action.setShortcut("Ctrl+S")
        file_menu.addAction(self.save_action)

        self.save_as_action = QAction("另存为(&A)...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(self.save_as_action)

        file_menu.addSeparator()

        self.exit_action = QAction("退出(&X)", self)
        self.exit_action.setShortcut("Alt+F4")
        file_menu.addAction(self.exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")

        self.undo_action = QAction("撤销(&U)", self)
        self.undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("重做(&R)", self)
        self.redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(self.redo_action)

        edit_menu.addSeparator()

        self.cut_action = QAction("剪切(&T)", self)
        self.cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("复制(&C)", self)
        self.copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("粘贴(&P)", self)
        self.paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(self.paste_action)

        edit_menu.addSeparator()

        self.find_action = QAction("查找(&F)", self)
        self.find_action.setShortcut("Ctrl+F")
        edit_menu.addAction(self.find_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")

        self.toggle_tree_action = QAction("文件树(&T)", self)
        self.toggle_tree_action.setCheckable(True)
        self.toggle_tree_action.setChecked(True)
        view_menu.addAction(self.toggle_tree_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具(&T)")

        self.settings_action = QAction("设置(&S)", self)
        tools_menu.addAction(self.settings_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")

        self.about_action = QAction("关于(&A)", self)
        help_menu.addAction(self.about_action)

    def _create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()

        toolbar.addAction(self.cut_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addSeparator()

        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)

    def _setup_styles(self):
        """设置样式"""
        self.setStyleSheet(
            """
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
        """
        )

    def _connect_signals(self):
        """连接信号"""
        # 文件操作
        self.new_action.triggered.connect(self._on_new)
        self.open_action.triggered.connect(self._on_open)
        self.save_action.triggered.connect(self._on_save)
        self.save_as_action.triggered.connect(self._on_save_as)
        self.exit_action.triggered.connect(self.close)

        # 编辑操作
        self.undo_action.triggered.connect(self.editor.undo)
        self.redo_action.triggered.connect(self.editor.redo)
        self.cut_action.triggered.connect(self.editor.cut)
        self.copy_action.triggered.connect(self.editor.copy)
        self.paste_action.triggered.connect(self.editor.paste)
        self.find_action.triggered.connect(self._show_find_dialog)

        # 视图操作
        self.toggle_tree_action.triggered.connect(self._toggle_file_tree)

        # 工具操作
        self.settings_action.triggered.connect(self._show_settings_dialog)

        # 文件树
        self.file_tree.clicked.connect(self._on_file_clicked)

        # 编辑器
        if hasattr(self.editor, "cursorPositionChanged"):
            self.editor.cursorPositionChanged.connect(self._on_cursor_changed)

    def _on_new(self):
        """新建文件"""
        self.editor.clear()
        self.statusBar.showMessage("新建文件")

    def _on_open(self):
        """打开文件"""
        file_name = FileDialogs.get_open_file_name(self)
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.statusBar.showMessage(f"已打开：{file_name}")
                self.fileOpened.emit(file_name)
            except Exception as e:
                self.statusBar.showMessage(f"打开文件失败：{str(e)}")

    def _on_save(self):
        """保存文件"""
        # TODO: 实现保存功能
        self.statusBar.showMessage("文件已保存")

    def _on_save_as(self):
        """另存为"""
        file_name = FileDialogs.get_save_file_name(self)
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(self.editor.toPlainText())
                self.statusBar.showMessage(f"已保存：{file_name}")
                self.fileSaved.emit(file_name)
            except Exception as e:
                self.statusBar.showMessage(f"保存文件失败：{str(e)}")

    def _show_find_dialog(self):
        """显示查找对话框"""
        dialog = FindReplaceDialog(self)
        dialog.show()

    def _show_settings_dialog(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec_():
            # TODO: 应用设置
            pass

    def _toggle_file_tree(self, checked: bool):
        """切换文件树显示状态"""
        self.file_tree.setVisible(checked)

    def _on_file_clicked(self, index):
        """处理文件点击"""
        file_path = self.file_model.filePath(index)
        if file_path and file_path.endswith((".txt", ".py", ".md")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.statusBar.showMessage(f"已打开：{file_path}")
            except Exception as e:
                self.statusBar.showMessage(f"打开文件失败：{str(e)}")

    def _on_cursor_changed(self, line: int, column: int):
        """处理光标位置变化"""
        self.statusBar.showMessage(f"行：{line}，列：{column}")
