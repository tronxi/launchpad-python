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
        self._apps.clear()
        for root in self._roots:
            if not os.path.isdir(root):
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                for d in dirnames:
                    if d.endswith(".app"):
                        full_path = os.path.join(dirpath, d)
                        self._apps.append(App(d, os.path.realpath(full_path)))
                dirnames[:] = [dn for dn in dirnames if not dn.endswith(".app")]

    def get_apps(self):
        return self._apps
