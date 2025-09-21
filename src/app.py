import subprocess

from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileIconProvider


class App:
    def __init__(self, name, path):
        self.id = None
        self.name = name
        self.path = path
        self._provider = QFileIconProvider()

    def draw(self, display_name=None):
        icon = QWidget()
        icon.setFixedSize(120, 140)
        icon_layout = QVBoxLayout(icon)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(6)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        icon_image = self._provider.icon(QFileInfo(self.path))
        icon_pixmap = icon_image.pixmap(100, 100)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon_pixmap)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text = display_name if display_name else self.name[:-4]
        name_lbl = QLabel(text)
        name_lbl.setWordWrap(True)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        name_lbl.setFixedWidth(100)

        icon_layout.addWidget(icon_lbl)
        icon_layout.addWidget(name_lbl)

        icon.setCursor(Qt.CursorShape.PointingHandCursor)
        icon.mouseReleaseEvent = lambda _: self._run_app()
        return icon


    def get_icon_image(self):
        return self._provider.icon(QFileInfo(self.path))

    def _run_app(self):
        subprocess.run(["open", self.path])


    def __eq__(self, other):
        if not isinstance(other, App):
            return NotImplemented
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return f"App(name={self.name!r}, path={self.path!r})"
