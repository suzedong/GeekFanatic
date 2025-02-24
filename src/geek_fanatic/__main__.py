"""
GeekFanatic 主入口
"""

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow

from geek_fanatic.core.app import GeekFanatic
from geek_fanatic.core.layout import Layout

class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, app: GeekFanatic) -> None:
        """初始化主窗口"""
        super().__init__()
        self.app = app
        
        self.setWindowTitle("GeekFanatic")
        self.setGeometry(100, 100, 1200, 800)

        # 创建布局并注入到app中
        self._layout = Layout(self)
        self.app.set_layout(self._layout)

        # 初始化插件系统
        self.app.initialize_plugins()
        
        # 设置样式
        self._setup_style()

    def _setup_style(self) -> None:
        """设置样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)

def main() -> int:
    """应用程序主入口"""
    # 添加源代码目录到Python路径
    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setApplicationName("GeekFanatic")
    app.setOrganizationName("GeekFanatic")

    try:
        # 创建核心实例
        app_core = GeekFanatic()

        # 创建并显示主窗口
        window = MainWindow(app_core)
        window.show()

        return app.exec()

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
