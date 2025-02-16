"""
资源模块
"""
from pathlib import Path

# 资源目录路径
RESOURCE_DIR = Path(__file__).parent

# 子目录路径
IMAGES_DIR = RESOURCE_DIR / "images"
STYLES_DIR = RESOURCE_DIR / "styles"
I18N_DIR = RESOURCE_DIR / "i18n"

__all__ = [
    'RESOURCE_DIR',
    'IMAGES_DIR',
    'STYLES_DIR',
    'I18N_DIR'
]