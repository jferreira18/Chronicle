import sqlite3
from pathlib import Path

from db.models import CREATE_ACTIVITY_LOG_TABLE


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "chronicle.db"


def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(CREATE_ACTIVITY_LOG_TABLE)

    conn.commit()
    conn.close()