from pathlib import Path

from src.app import App
import os


class AppSearcher:
    def __init__(self):
        self._apps = []
        self._roots = [
            "/Applications",
            "/System/Applications",
            str(Path.home() / "Applications"),
        ]

    def search(self):
        for root in self._roots:
            apps = os.listdir(root)
            for app in apps:
                if app.endswith(".app"):
                    path = os.path.realpath(os.path.join(root, app))
                    self._apps.append(App(app, path))

    def get_apps(self):
        return self._apps
