import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from app_searcher import AppSearcher
from AppKit import NSWorkspace, NSScreen

def get_main_wallpaper_path():
    screen = NSScreen.mainScreen()
    url = NSWorkspace.sharedWorkspace().desktopImageURLForScreen_(screen)
    return url.path()


class Main(QScrollArea):
    def __init__(self):
        super().__init__()

        self._searcher = AppSearcher()
        self._searcher.search()

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
            background-color: rgb(17, 49, 70);
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
        frm.setVerticalSpacing(50)
        cols = 6
        for i, app in enumerate(self._searcher.get_display_apps()):
            r, c = divmod(i, cols)
            icon = app.draw()

            frm.addWidget(icon, r, c, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        frm.setRowStretch(frm.rowCount(), 1)
        self.setWidget(inner)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    win = Main()
    sys.exit(application.exec())
