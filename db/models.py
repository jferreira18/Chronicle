CREATE_ACTIVITY_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    app_name TEXT,
    window_title TEXT,
    duration_seconds INTEGER NOT NULL
);
"""