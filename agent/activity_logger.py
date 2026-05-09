import time
from datetime import datetime

import psutil
import win32gui
import win32process

from services.activity_service import save_activity


POLL_SECONDS = 15


def get_active_window():
    hwnd = win32gui.GetForegroundWindow()

    window_title = win32gui.GetWindowText(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        process = psutil.Process(pid)
        app_name = process.name()

    except psutil.Error:
        app_name = "Unknown"

    return app_name, window_title


def run_activity_logger():
    print("Chronicle activity logger started.")

    current_app, current_title = get_active_window()

    session_start = datetime.now()

    while True:
        time.sleep(POLL_SECONDS)

        new_app, new_title = get_active_window()

        if (
            new_app != current_app
            or new_title != current_title
        ):
            session_end = datetime.now()

            duration_seconds = int(
                (session_end - session_start).total_seconds()
            )

            save_activity(
                start_time=session_start.isoformat(),
                end_time=session_end.isoformat(),
                app_name=current_app,
                window_title=current_title,
                duration_seconds=duration_seconds
            )

            print(
                f"[SAVED] "
                f"{current_app} | "
                f"{current_title} | "
                f"{duration_seconds}s"
            )

            current_app = new_app
            current_title = new_title

            session_start = session_end