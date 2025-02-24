from PySide6.QtGui import QIcon
from pathlib import Path

base_dir = Path("src/geek_fanatic/resources/resources")
icons = ["explorer", "search", "git", "debug", "extensions", "settings"]

for icon_name in icons:
    icon_path = base_dir / f"{icon_name}.svg"
    icon = QIcon(str(icon_path))
    print(f"\nTesting {icon_name} icon:")
    print(f"Icon path: {icon_path}")
    print(f"Icon path exists: {icon_path.exists()}")
    print(f"Icon is null: {icon.isNull()}")
    print(f"Available sizes: {icon.availableSizes()}")
