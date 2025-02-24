from PySide6.QtCore import QSize, QByteArray, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QLabel

def create_icon_from_svg(svg_content: str, size: int = 24) -> QIcon:
    """从 SVG 内容创建图标"""
    renderer = QSvgRenderer(QByteArray(svg_content.encode()))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

# 测试代码
EXPLORER_SVG = """
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <path fill="#CCCCCC" d="M3 3h18v18H3V3m2 2v14h14V5H5z"/>
    <path fill="#CCCCCC" d="M7 7h10v10H7V7m2 2v6h6V9H9z"/>
</svg>
"""

app = QApplication([])
icon = create_icon_from_svg(EXPLORER_SVG)
label = QLabel()
label.setPixmap(icon.pixmap(24, 24))
label.show()
app.exec()
