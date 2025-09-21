import sqlite3
import json

from app_searcher import AppSearcher

DB_PATH = "apps.db"

def create_folder_with_apps(conn, folder_name, app_names):
    cur = conn.cursor()
    cur.execute("""
                insert into display_app (name, position)
                values (
                           ?,
                           (select coalesce(max(position), 0) + 1 from display_app)
                       )
                """, (folder_name,))
    folder_id = cur.lastrowid
    print(f"Creado folder '{folder_name}' con id={folder_id}")

    for app_name in app_names:
        if not app_name.endswith(".app"):
            app_name_db = app_name + ".app"
        else:
            app_name_db = app_name

        cur.execute("select id from app where name = ?", (app_name_db,))
        row = cur.fetchone()
        if not row:
            print(f"App '{app_name}' no existe en la base de datos.")
            continue

        app_id = row[0]
        cur.execute("delete from display_app_app where app_id = ?", (app_id,))
        cur.execute("""
                    insert into display_app_app (app_id, display_app_id)
                    values (?, ?)
                    """, (app_id, folder_id))

    cur.execute("""
                delete from display_app
                where id not in (select distinct display_app_id from display_app_app)
                """)
    conn.commit()


def create_structure_from_json(json_path):
    AppSearcher().search()
    with open(json_path, "r") as f:
        data = json.load(f)

    all_apps_from_json = set()
    for apps in data.values():
        for app in apps:
            if not app.endswith(".app"):
                all_apps_from_json.add(app + ".app")
            else:
                all_apps_from_json.add(app)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("select name from app")
        all_apps_in_db = {row[0] for row in cur.fetchall()}

        missing_apps = sorted(all_apps_in_db - all_apps_from_json)

        for folder_name, apps in data.items():
            if folder_name == "Apps":
                apps = apps + missing_apps
            create_folder_with_apps(conn, folder_name, apps)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Example: python create_folders.py <json_path>")
    else:
        create_structure_from_json(sys.argv[1])
