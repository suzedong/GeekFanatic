"""
代码折叠功能实现
"""

import re
from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtCore import QObject, Signal

from geek_fanatic.plugins.editor.features import EditorFeature
from geek_fanatic.plugins.editor.types import Position


@dataclass
class FoldRegion:
    """折叠区域"""

    start_line: int
    end_line: int
    is_folded: bool = False


class CodeFolding(EditorFeature):
    """代码折叠功能实现"""

    def __init__(self, editor: "Editor") -> None:
        """初始化代码折叠"""
        super().__init__(editor)
        self._folded_regions: List[FoldRegion] = []
        self._indentation_pattern = re.compile(r"^(\s*)\S")

    def initialize(self) -> None:
        """初始化功能"""
        # 连接文本改变信号，重新计算折叠区域
        self._editor.contentChanged.connect(self.compute_folds)

    def cleanup(self) -> None:
        """清理功能"""
        self._folded_regions.clear()

    def compute_folds(self) -> None:
        """计算可折叠区域"""
        self._folded_regions.clear()
        content = self._editor.content
        if not content:
            return

        lines = content.split("\n")
        current_indent = -1
        fold_start = -1
        last_indents = []  # 存储每个缩进级别的最后一个行号

        for i, line in enumerate(lines):
            # 跳过空行
            if not line.strip():
                continue

            # 计算当前行的缩进级别
            match = self._indentation_pattern.match(line)
            if not match:
                indent = 0
            else:
                indent = len(match.group(1))

            # 如果这一行以冒号结尾，标记为可折叠区域的开始
            if line.rstrip().endswith(":"):
                self._folded_regions.append(
                    FoldRegion(start_line=i, end_line=i)  # 临时设置，后面会更新
                )
                last_indents.append((i, indent))
                continue

            # 如果缩进减少，说明前面的块结束
            while last_indents and indent <= last_indents[-1][1]:
                start_line, _ = last_indents.pop()
                # 更新该块的结束行
                for region in self._folded_regions:
                    if region.start_line == start_line:
                        region.end_line = i - 1
                        break

            # 如果是新的更大缩进，可能是新块的开始
            if not last_indents or indent > last_indents[-1][1]:
                last_indents.append((i, indent))

        # 处理未关闭的块
        while last_indents:
            start_line, _ = last_indents.pop()
            for region in self._folded_regions:
                if region.start_line == start_line:
                    region.end_line = len(lines) - 1
                    break

        # 移除无效的折叠区域（开始和结束行相同）
        self._folded_regions = [
            r for r in self._folded_regions if r.end_line > r.start_line
        ]

    def toggle_fold(self, line: int) -> None:
        """切换指定行的折叠状态"""
        for region in self._folded_regions:
            if region.start_line == line:
                region.is_folded = not region.is_folded
                break

    def is_line_folded(self, line: int) -> bool:
        """判断指定行是否被折叠"""
        for region in self._folded_regions:
            if region.is_folded and region.start_line < line <= region.end_line:
                return True
        return False

    def get_visible_line_count(self) -> int:
        """获取可见行数（考虑折叠）"""
        total_lines = len(self._editor.content.split("\n"))
        hidden_lines = 0

        for region in self._folded_regions:
            if region.is_folded:
                hidden_lines += region.end_line - region.start_line

        return total_lines - hidden_lines

    def get_folding_regions(self) -> List[FoldRegion]:
        """获取所有折叠区域"""
        return self._folded_regions.copy()

    def get_fold_level(self, line: int) -> int:
        """获取指定行的折叠级别（缩进级别）"""
        text = self._editor._buffer.get_line(line)
        match = self._indentation_pattern.match(text)
        if match:
            return len(match.group(1))
        return 0
