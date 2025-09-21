import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QScrollArea, QLineEdit, QPushButton, QDialog
from PyQt6.QtCore import Qt
from app_searcher import AppSearcher
from AppKit import NSWorkspace, NSScreen

from settings_dialog import SettingsDialog


def get_main_wallpaper_path():
    screen = NSScreen.mainScreen()
    url = NSWorkspace.sharedWorkspace().desktopImageURLForScreen_(screen)
    return url.path()


class Main(QScrollArea):
    def __init__(self):
        super().__init__()

        self._searcher = AppSearcher()
        self._searcher.search()
        self.cols = 7

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
        QLineEdit {
            padding: 8px;
            font-size: 18px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        """)

    def _build_ui(self):
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        self.frm = QGridLayout(inner)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self._on_search_changed)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.search_bar.setFocus()

        self.settings_btn = QPushButton()
        self.settings_btn.setText("⚙")
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                font-size: 25px;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """)
        self.settings_btn.clicked.connect(self._open_settings)

        self.frm.addWidget(self.settings_btn, 0, self.cols - 1)
        self.frm.addWidget(self.search_bar, 0, 0, 1, self.cols - 1,
                           alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignVCenter)

        self.frm.setContentsMargins(12, 12, 12, 12)
        self.frm.setHorizontalSpacing(12)
        self.frm.setVerticalSpacing(25)
        self._populate_apps(self._searcher.get_display_apps())
        self.frm.setRowStretch(self.frm.rowCount(), 1)
        self.setWidget(inner)

    def _populate_apps(self, apps):
        for i in reversed(range(self.frm.count())):
            item = self.frm.itemAt(i)
            if item:
                w = item.widget()
                if w and not isinstance(w, (QLineEdit, QPushButton)):
                    w.setParent(None)
        for i, app in enumerate(apps):
            r, c = divmod(i, self.cols)
            icon = app.draw()

            self.frm.addWidget(icon, r + 1, c, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def _on_search_changed(self, text: str):
        text = text.strip().lower()
        if not text:
            self._populate_apps(self._searcher.get_display_apps())
        else:
            apps = []
            for app in self._searcher.get_apps():
                app_name = app.name.lower().removesuffix(".app")
                if text in app_name:
                    apps.append(app)
            self._populate_apps(apps)

    def mousePressEvent(self, event):
        self.search_bar.setFocus()
        super().mousePressEvent(event)

    def changeEvent(self, event):
        if event.type() == event.Type.ActivationChange:
            active_window = QApplication.activeWindow()
            if not self.isActiveWindow() and not isinstance(active_window, QDialog):
                QApplication.quit()
        super().changeEvent(event)

    def _open_settings(self):
        dialog = SettingsDialog(self, on_close=self._refresh_apps)
        dialog.setWindowIcon(
            QIcon("assets/icons/settings.svg")
        )
        dialog.exec()

    def _refresh_apps(self):
        self.search_bar.setText("")
        self._on_search_changed("")

if __name__ == "__main__":
    application = QApplication(sys.argv)
    win = Main()
    sys.exit(application.exec())
