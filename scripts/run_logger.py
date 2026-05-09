from db.database import init_db
from agent.activity_logger import run_activity_logger


if __name__ == "__main__":
    init_db()
    run_activity_logger()