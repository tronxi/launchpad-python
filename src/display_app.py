from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QScrollArea, QGridLayout


class DisplayApp:
    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.app_list = []

    def draw(self):
        if len(self.app_list) == 1:
            return self.app_list[0].draw(display_name=self.name)
        else:
            icon = QWidget()
            icon_pixmap =  self._compose_icon_pixmap()

            icon_layout = QVBoxLayout(icon)
            icon_layout.setContentsMargins(10, 10, 10, 10)
            icon_layout.setSpacing(6)

            icon_lbl = QLabel()
            icon_lbl.setPixmap(icon_pixmap)

            name_lbl = QLabel(self.name)
            name_lbl.setWordWrap(True)
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            icon_layout.addWidget(icon_lbl)
            icon_layout.addWidget(name_lbl)
            icon.setCursor(Qt.CursorShape.PointingHandCursor)
            icon.mouseReleaseEvent = lambda event: self._open_popup()
            return icon


    def _open_popup(self):
        self._dialog = QDialog()
        self._dialog.setWindowTitle(self.name)
        self._dialog.resize(1040, 800)
        self._dialog.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self._dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._dialog.setStyleSheet("background-color: rgb(10, 33, 48);")

        scroll = QScrollArea(self._dialog)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        grid = QGridLayout(container)
        grid.setContentsMargins(12, 12, 12, 12)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(50)

        cols = 8
        for i, app in enumerate(self.app_list):
            r, c = divmod(i, cols)
            grid.addWidget(app.draw(), r, c)

        scroll.setWidget(container)

        layout = QVBoxLayout(self._dialog)
        layout.addWidget(scroll)

        grid.setRowStretch(grid.rowCount(), 1)

        self._dialog.show()

    def _compose_icon_pixmap(self):
        size = 80
        icons = [app.get_icon_image().pixmap(size//2, size//2) for app in self.app_list[:4]]

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        positions = [
            (0, 0),
            (size//2, 0),
            (0, size//2),
            (size//2, size//2),
        ]
        for i, icon in enumerate(icons):
            painter.drawPixmap(positions[i][0], positions[i][1], icon)
        painter.end()

        return pixmap
