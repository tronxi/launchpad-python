import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QScrollArea, QVBoxLayout, QFrame, \
    QFileIconProvider, QSizePolicy
from PyQt6.QtCore import Qt, QFileInfo
import subprocess
from src.app_searcher import AppSearcher
from AppKit import NSWorkspace, NSScreen


def _run_app(app):
    subprocess.run(["open", app.path])


def get_main_wallpaper_path():
    screen = NSScreen.mainScreen()
    url = NSWorkspace.sharedWorkspace().desktopImageURLForScreen_(screen)
    return url.path()


class Main(QScrollArea):
    def __init__(self):
        super().__init__()

        self._searcher = AppSearcher()
        self._searcher.search()
        self._provider = QFileIconProvider()

        self.setWindowTitle("Launchpad")
        self._build_ui()
        self.showFullScreen()
        self.setWidgetResizable(True)
        self.setObjectName("root")
        # img = get_main_wallpaper_path()
        # self.setStyleSheet(f"""
        # #root {{
        #     border-image: url("{img}") 0 0 0 0;
        # }}
        # """)
        self.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: rgb(16, 87, 194);
        }
        QScrollArea > QWidget {
            background: transparent;
        }
        """)

    def _build_ui(self):
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        frm = QGridLayout(inner)
        frm.setContentsMargins(12, 12, 12, 12)
        frm.setHorizontalSpacing(12)
        frm.setVerticalSpacing(8)
        cols = 6
        for i, app in enumerate(self._searcher.get_apps()):
            r, c = divmod(i, cols)
            icon = self._build_icon(app)

            frm.addWidget(icon, r, c, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.setWidget(inner)

    def _build_icon(self, app):
        icon = QWidget()

        icon_image = self._provider.icon(QFileInfo(app.path))
        icon_pixmap = icon_image.pixmap(80, 80)

        icon_layout = QVBoxLayout(icon)
        icon_layout.setContentsMargins(10, 10, 10, 10)
        icon_layout.setSpacing(6)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon_pixmap)
        # icon_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        name_lbl = QLabel(app.name[:-4])
        name_lbl.setWordWrap(True)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        icon_layout.addWidget(icon_lbl)
        icon_layout.addWidget(name_lbl)
        icon.setCursor(Qt.CursorShape.PointingHandCursor)
        icon.mouseReleaseEvent = lambda _: _run_app(app)
        return icon


if __name__ == "__main__":
    application = QApplication(sys.argv)
    win = Main()
    sys.exit(application.exec())
