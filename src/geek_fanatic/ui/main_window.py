"""
主窗口模块
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
)

class MainWindow(QMainWindow):
    """IDE主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GeekFanatic")
        self.setGeometry(100, 100, 1280, 800)
        
        # 设置中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 设置主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建活动栏
        activity_bar = QFrame()
        activity_bar.setFixedWidth(48)
        activity_bar.setStyleSheet("background-color: #333333;")
        main_layout.addWidget(activity_bar)
        
        # 创建侧边栏
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #252526;")
        main_layout.addWidget(sidebar)
        
        # 创建编辑器区域
        editor_area = QFrame()
        editor_area.setStyleSheet("background-color: #1e1e1e;")
        main_layout.addWidget(editor_area)
        
        # 创建状态栏
        self.statusBar().setFixedHeight(22)
        self.statusBar().setStyleSheet("background-color: #007acc; color: white;")
        
        # 添加状态栏信息
        status_label = QLabel("就绪")
        self.statusBar().addWidget(status_label)