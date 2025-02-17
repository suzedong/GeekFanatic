# -*- coding: utf-8 -*-
"""
资源管理模块

本模块提供对项目中各种资源文件的路径管理。
"""

from pathlib import Path

# 根资源目录
RESOURCE_DIR = Path(__file__).parent

# 子资源目录
IMAGES_DIR = RESOURCE_DIR / "images"  # 图片资源目录
STYLES_DIR = RESOURCE_DIR / "styles"  # 样式表目录
I18N_DIR = RESOURCE_DIR / "i18n"      # 国际化资源目录

__all__ = ["RESOURCE_DIR", "IMAGES_DIR", "STYLES_DIR", "I18N_DIR"]