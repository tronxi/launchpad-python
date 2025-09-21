import json

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QPlainTextEdit, QMessageBox
from PyQt6.QtCore import Qt

from create_folders import FolderCreator


class SettingsDialog(QDialog):
    def __init__(self, parent=None, on_close=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.resize(1200, 800)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.json_path = "apps.json"
        self._on_close = on_close

        layout = QVBoxLayout(self)
        self.editor = QPlainTextEdit()
        layout.addWidget(self.editor)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_json)
        layout.addWidget(save_btn)

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(json.dumps(json.load(f), indent=5, ensure_ascii=False))
        except FileNotFoundError:
            self.editor.setPlainText("{}")

        self.setStyleSheet("""
        QDialog {
            background-color: #1e1e1e;
            color: white;
            border-radius: 12px;
        }
        QPushButton {
            background-color: #2b2b2b;
            color: white;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #3c3c3c;
        }
        """)

    def save_json(self):
        text = self.editor.toPlainText()
        try:
            data = json.loads(text)
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "OK", "File saved successfully")
            FolderCreator().create_structure_from_json(self.json_path)
            self.close()
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON:\n{e}")

    def closeEvent(self, event):
        if callable(self._on_close):
            self._on_close()
        super().closeEvent(event)
