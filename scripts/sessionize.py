import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path

from scripts.categories import APP_CATEGORIES, TITLE_KEYWORDS
from scripts.categories import APP_CATEGORIES, TITLE_KEYWORDS, PROJECT_KEYWORDS

DB_PATH = Path("data/chronicle.db")


def clean_title(title: str) -> str:
    if not title:
        return "Unknown"

    title = re.sub(r"^\(\d+\)\s*", "", title)
    title = title.replace(" - Google Chrome", "")
    title = title.replace(" - Visual Studio Code", "")
    title = title.replace(" - Foxit PDF Reader", "")
    title = title.replace("• ", "")
    return title.strip()


def categorize_app(process_name: str) -> str:
    return APP_CATEGORIES.get(process_name, "Other")


def infer_topic(title: str) -> str:
    for keyword, topic in TITLE_KEYWORDS.items():
        if keyword.lower() in title.lower():
            return topic
    return "General Activity"


def load_events():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT start_time, end_time, app_name, window_title, duration_seconds
        FROM activity_log
        ORDER BY start_time ASC
    """).fetchall()

    conn.close()
    return rows


def build_sessions(max_gap_minutes=2):
    rows = load_events()
    sessions = []

    current = None
    max_gap = timedelta(minutes=max_gap_minutes)

    for row in rows:
        timestamp = datetime.fromisoformat(row["start_time"])
        process_name = row["app_name"]
        title = clean_title(row["window_title"])
        duration = int(row["duration_seconds"] or 0)

        category = categorize_app(process_name)
        topic = infer_topic(title)
        related_projects = infer_related_project(title)

        if current is None:
            current = {
                "start": timestamp,
                "end": timestamp + timedelta(seconds=duration),
                "duration_seconds": duration,
                "apps": {process_name},
                "category": category,
                "topic": topic,
                "evidence": [title],
                "related_projects": related_projects
            }
            continue

        gap = timestamp - current["end"]
        same_topic = topic == current["topic"]
        same_category = category == current["category"]

        both_general = topic == "General Activity" and current["topic"] == "General Activity"
        if gap <= max_gap and same_topic and not both_general:
            current["end"] = timestamp + timedelta(seconds=duration)
            current["duration_seconds"] += duration
            current["apps"].add(process_name)

            if title not in current["evidence"]:
                current["evidence"].append(title)

            if gap <= max_gap and same_topic and not both_general:
                current["end"] = timestamp + timedelta(seconds=duration)
                current["duration_seconds"] += duration
                current["apps"].add(process_name)

                if title not in current["evidence"]:
                    current["evidence"].append(title)

                for project in related_projects:
                    if project not in current["related_projects"]:
                        current["related_projects"].append(project)
        else:
            sessions.append(current)
            current = {
                "start": timestamp,
                "end": timestamp + timedelta(seconds=duration),
                "duration_seconds": duration,
                "apps": {process_name},
                "category": category,
                "topic": topic,
                "evidence": [title],
                "related_projects": related_projects
            }

    if current:
        sessions.append(current)

    return sessions

def infer_related_project(title: str):
    matches = []

    for project, keywords in PROJECT_KEYWORDS.items():
        score = 0
        evidence = []

        for keyword in keywords:
            if keyword.lower() in title.lower():
                score += 1
                evidence.append(keyword)

        if score > 0:
            confidence = "high" if score >= 2 else "medium"
            matches.append({
                "project": project,
                "confidence": confidence,
                "evidence": evidence,
            })

    return matches

def print_sessions():
    sessions = build_sessions()

    for s in sessions:
        start = s["start"].strftime("%H:%M")
        end = s["end"].strftime("%H:%M")
        minutes = round(s["duration_seconds"] / 60, 1)
        apps = ", ".join(sorted(s["apps"]))
        
    print(f"{start}-{end} | {s['topic']} | {minutes} min")
    for item in s["evidence"][:3]:
        print(f"  - {item}")

    if s.get("related_projects"):
        print("  Related projects:")
        for project in s["related_projects"]:
            print(
                f"    - {project['project']} "
                f"({project['confidence']}) via {', '.join(project['evidence'])}"
            )

    print()


if __name__ == "__main__":
    print_sessions()