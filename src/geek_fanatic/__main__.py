#!/usr/bin/env python
"""
GeekFanatic 主程序入口模块
"""
import os
import sys
from pathlib import Path

def setup_qt_env():
    """设置Qt环境变量"""
    try:
        import PySide6
        qt_root = os.path.dirname(PySide6.__file__)
        
        # 设置插件路径
        paths = {
            "QT_PLUGIN_PATH": os.path.join(qt_root, "plugins"),
            "QT_QPA_PLATFORM_PLUGIN_PATH": os.path.join(qt_root, "plugins", "platforms"),
            "QML2_IMPORT_PATH": os.path.join(qt_root, "qml"),
        }
        
        for key, value in paths.items():
            if os.path.exists(value):
                os.environ[key] = value
                print(f"Set {key}={value}")
            else:
                print(f"Warning: Path does not exist: {value}")
                
    except ImportError:
        print("Error: PySide6 not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error setting up Qt environment: {e}")
        sys.exit(1)

# 在导入 PySide6 模块之前设置环境
setup_qt_env()

from PySide6.QtWidgets import QApplication

from geek_fanatic.ui.main_window import MainWindow

def main() -> None:
    """主程序入口函数"""
    # 创建Qt应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("GeekFanatic")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()