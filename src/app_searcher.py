from pathlib import Path

from src.app import App
import os
import sqlite3


class AppSearcher:
    def __init__(self):
        self._apps = []
        self._roots = [
            "/Applications",
            "/System/Applications",
            str(Path.home() / "Applications"),
        ]
        self._db_path = "apps.db"
        self._init_db()

    def search(self):
        self._apps.clear()
        database_apps = self._retrieve_database_apps()
        file_apps = []
        for root in self._roots:
            if not os.path.isdir(root):
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                for d in dirnames:
                    if d.endswith(".app"):
                        full_path = os.path.join(dirpath, d)
                        app = App(d, os.path.realpath(full_path))
                        file_apps.append(app)
                        if app not in database_apps:
                            self._save_app(app)
                dirnames[:] = [dn for dn in dirnames if not dn.endswith(".app")]
        for app in database_apps:
            if app not in file_apps:
                self._delete_app(app)
        self._apps.extend(file_apps)


    def _init_db(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                         create table if not exists app
                         (
                             id   integer primary key autoincrement,
                             name text not null,
                             path text not null unique
                         )
                         """)

    def _retrieve_database_apps(self):
        database_apps = []
        with sqlite3.connect(self._db_path) as conn:
            for row in conn.execute("select name, path from app"):
                database_apps.append(App(row[0], row[1]))
        return database_apps

    def _save_app(self, app):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("insert into app (name, path) values (?, ?)", (app.name, app.path))

    def _delete_app(self, app):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("delete from app where name = ? and path = ?", (app.name, app.path))

    def get_apps(self):
        return self._apps
