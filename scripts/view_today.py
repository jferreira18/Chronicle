from db.database import get_db_connection


def view_today():
    conn = get_db_connection()
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT *
        FROM activity_log
        ORDER BY start_time DESC
    """).fetchall()

    conn.close()

    for row in rows:
        print(
            f"{row['start_time']} | "
            f"{row['app_name']} | "
            f"{row['window_title']} | "
            f"{row['duration_seconds']}s"
        )


if __name__ == "__main__":
    view_today()