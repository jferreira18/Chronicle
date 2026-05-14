from collections import defaultdict
from scripts.sessionize import build_sessions
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def summarize_day():
    sessions = build_sessions()

    total_seconds = sum(s["duration_seconds"] for s in sessions)

    topic_totals = defaultdict(int)
    category_totals = defaultdict(int)
    app_totals = defaultdict(int)

    for s in sessions:
        topic_totals[s["topic"]] += s["duration_seconds"]
        category_totals[s["category"]] += s["duration_seconds"]

        for app in s["apps"]:
            app_totals[app] += s["duration_seconds"]

    print("\nDaily Chronicle Summary")
    print("=" * 30)
    print(f"Total tracked time: {round(total_seconds / 60, 1)} minutes")
    print(f"Total sessions: {len(sessions)}")

    print("\nTop Topics:")
    for topic, seconds in sorted(topic_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"- {topic}: {round(seconds / 60, 1)} min")

    print("\nTop Categories:")
    for category, seconds in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"- {category}: {round(seconds / 60, 1)} min")

    print("\nMajor Activity Blocks:")
    for s in sessions:
        if s["duration_seconds"] < 30:
            continue

        start = s["start"].strftime("%H:%M")
        end = s["end"].strftime("%H:%M")
        minutes = round(s["duration_seconds"] / 60, 1)

        print(f"\n{start}-{end} | {s['topic']} | {minutes} min")
        for item in s["evidence"][:3]:
            print(f"  - {item}")

    summary_path = OUTPUT_DIR / f"daily_summary_{datetime.now().date()}.txt"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Daily Chronicle Summary\n")
        f.write("=======================\n")
        f.write(f"Total tracked time: {round(total_seconds / 60, 1)} minutes\n")
        f.write(f"Total sessions: {len(sessions)}\n\n")

        f.write("Top Topics:\n")
        for topic, seconds in sorted(topic_totals.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {topic}: {round(seconds / 60, 1)} min\n")

        f.write("\nMajor Activity Blocks:\n")
        for s in sessions:
            if s["duration_seconds"] < 30:
                continue

            start = s["start"].strftime("%H:%M")
            end = s["end"].strftime("%H:%M")
            minutes = round(s["duration_seconds"] / 60, 1)

            f.write(f"\n{start}-{end} | {s['topic']} | {minutes} min\n")
            for item in s["evidence"][:3]:
                f.write(f"  - {item}\n")

    print(f"\nSaved summary to: {summary_path}")
if __name__ == "__main__":
    summarize_day()