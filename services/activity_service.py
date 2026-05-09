from db.database import get_db_connection


def save_activity(
    start_time,
    end_time,
    app_name,
    window_title,
    duration_seconds
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO activity_log (
            start_time,
            end_time,
            app_name,
            window_title,
            duration_seconds
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        start_time,
        end_time,
        app_name,
        window_title,
        duration_seconds
    ))

    conn.commit()
    conn.close()