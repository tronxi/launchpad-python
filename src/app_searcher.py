from pathlib import Path

from app import App
import os
import sqlite3

from display_app import DisplayApp


class AppSearcher:
    def __init__(self):
        self._apps = []
        self._display_apps = []
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
                            id = self._save_app(app)
                            app.id = id
                            id = self._add_display_app("", self._retrieve_latest_position() + 1)
                            self._link_app_to_display(id, app.id)
                dirnames[:] = [dn for dn in dirnames if not dn.endswith(".app")]
        for app in database_apps:
            if app not in file_apps:
                self._delete_app(app)
        self._apps.extend(file_apps)

    def _init_db(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                         create table if not exists display_app
                         (
                             id       integer primary key autoincrement,
                             name     text    not null,
                             position integer not null unique
                         )
                         """)
            conn.execute("""
                         create table if not exists app
                         (
                             id   integer primary key autoincrement,
                             name text not null,
                             path text not null unique
                         )
                         """)
            conn.execute("""
                         create table if not exists display_app_app
                         (
                             display_app_id integer not null references display_app (id) on delete cascade,
                             app_id         integer not null references app (id) on delete cascade,
                             primary key (display_app_id, app_id)
                         );
                         """)

    def _retrieve_database_apps(self):
        database_apps = []
        with sqlite3.connect(self._db_path) as conn:
            for row in conn.execute("select name, path from app"):
                database_apps.append(App(row[0], row[1]))
        return database_apps

    def _retrieve_latest_position(self):
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute("select max(position) from display_app")
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else 0

    def _save_app(self, app):
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute("insert into app (name, path) values (?, ?)", (app.name, app.path))
            return cur.lastrowid

    def _delete_app(self, app):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("delete from app where name = ? and path = ?", (app.name, app.path))

    def _add_display_app(self, name, position):
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute("insert into display_app (name, position) values (?, ?)", (name, position))
            return cur.lastrowid

    def _link_app_to_display(self, display_id, app_id):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("insert or ignore into display_app_app (display_app_id, app_id) values (?, ?)",
                         (display_id, app_id))

    def get_display_apps(self):
        display_apps = []
        with sqlite3.connect(self._db_path) as conn:
            for row in conn.execute("select id, name, position from display_app order by position"):
                display_id, name, position = row
                display = DisplayApp(position, name)

                apps = []
                for app_row in conn.execute("""
                                            select a.id, a.name, a.path
                                            from app a
                                                     join display_app_app da on a.id = da.app_id
                                            where da.display_app_id = ?
                                            order by lower(a.name)
                                            """, (display_id,)):
                    app = App(app_row[1], app_row[2])
                    app.id = app_row[0]
                    apps.append(app)

                display.app_list = apps
                display_apps.append(display)

        return display_apps

    def get_apps(self):
        return self._apps
