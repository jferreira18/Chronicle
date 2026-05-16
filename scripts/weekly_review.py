from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import json

OUTPUT_DIR = Path("outputs")
DAYS_BACK = 7


def get_recent_summary_files(days_back=DAYS_BACK):
    cutoff = datetime.now().date() - timedelta(days=days_back)

    files = []

    for path in OUTPUT_DIR.glob("daily_summary_*.txt"):
        date_text = path.stem.replace("daily_summary_", "")

        try:
            file_date = datetime.fromisoformat(date_text).date()
        except ValueError:
            continue

        if file_date >= cutoff:
            files.append((file_date, path))

    return sorted(files, key=lambda x: x[0])


def parse_topic_lines(summary_text):
    topics = {}

    in_topic_section = False

    for line in summary_text.splitlines():
        stripped = line.strip()

        if stripped == "Top Topics:":
            in_topic_section = True
            continue

        if in_topic_section and stripped == "":
            break

        if in_topic_section and stripped.startswith("- "):
            try:
                topic_part, minutes_part = stripped[2:].rsplit(":", 1)
                minutes = float(minutes_part.replace("min", "").strip())
                topics[topic_part.strip()] = minutes
            except ValueError:
                continue

    return topics


def collect_weekly_data(summary_files):
    weekly_topic_totals = defaultdict(float)
    daily_totals = {}
    active_days = 0

    for file_date, path in summary_files:
        text = path.read_text(encoding="utf-8")
        topics = parse_topic_lines(text)

        if topics:
            active_days += 1

        day_total = sum(topics.values())
        daily_totals[file_date] = day_total

        for topic, minutes in topics.items():
            weekly_topic_totals[topic] += minutes

    return weekly_topic_totals, daily_totals, active_days


def build_weekly_review():
    summary_files = get_recent_summary_files()

    if not summary_files:
        raise FileNotFoundError(
            "No daily summaries found. Run: python -m scripts.summarize_day"
        )

    weekly_topic_totals, daily_totals, active_days = collect_weekly_data(summary_files)

    total_minutes = sum(weekly_topic_totals.values())

    lines = []
    lines.append("Weekly Chronicle Review")
    lines.append("=======================")
    lines.append(f"Review window: last {DAYS_BACK} days")
    lines.append(f"Summary files used: {len(summary_files)}")
    lines.append(f"Active tracked days: {active_days}")
    lines.append(f"Total summarized time: {round(total_minutes, 1)} minutes")
    lines.append("")

    lines.append("Daily Totals:")
    for day, minutes in daily_totals.items():
        lines.append(f"- {day}: {round(minutes, 1)} min")

    lines.append("")
    lines.append("Top Weekly Topics:")
    for topic, minutes in sorted(
        weekly_topic_totals.items(), key=lambda x: x[1], reverse=True
    ):
        lines.append(f"- {topic}: {round(minutes, 1)} min")

    lines.append("")
    lines.append("Recurring Themes:")
    recurring_topics = [
        topic for topic, minutes in weekly_topic_totals.items()
        if minutes >= 5
    ]

    if recurring_topics:
        for topic in sorted(
            recurring_topics,
            key=lambda t: weekly_topic_totals[t],
            reverse=True
        ):
            lines.append(f"- {topic}")
    else:
        lines.append("- No strong recurring themes detected yet.")

    lines.append("")
    lines.append("Suggested Reflection:")
    if weekly_topic_totals:
        top_topic = max(weekly_topic_totals.items(), key=lambda x: x[1])[0]
        lines.append(
            f"- Your dominant theme was {top_topic}. Consider whether this reflects your intended priority for the week."
        )
    else:
        lines.append("- Not enough topic data to generate a reflection.")

    return "\n".join(lines)


def save_weekly_review(review_text):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / f"weekly_review_{datetime.now().date()}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(review_text)

    return output_path

def save_weekly_review_json(summary_files, weekly_topic_totals, daily_totals, active_days):
    output_path = OUTPUT_DIR / f"weekly_review_{datetime.now().date()}.json"

    total_minutes = sum(weekly_topic_totals.values())

    weekly_json = {
        "date": str(datetime.now().date()),
        "review_window_days": DAYS_BACK,
        "summary_files_used": [
            {
                "date": str(file_date),
                "path": str(path),
            }
            for file_date, path in summary_files
        ],
        "active_tracked_days": active_days,
        "total_summarized_minutes": round(total_minutes, 1),
        "daily_totals": [
            {
                "date": str(day),
                "minutes": round(minutes, 1),
            }
            for day, minutes in daily_totals.items()
        ],
        "top_weekly_topics": [
            {
                "topic": topic,
                "minutes": round(minutes, 1),
            }
            for topic, minutes in sorted(
                weekly_topic_totals.items(),
                key=lambda x: x[1],
                reverse=True,
            )
        ],
        "recurring_themes": [
            topic
            for topic, minutes in sorted(
                weekly_topic_totals.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            if minutes >= 5
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(weekly_json, f, indent=2)

    return output_path


def main():
    summary_files = get_recent_summary_files()

    if not summary_files:
        raise FileNotFoundError(
            "No daily summaries found. Run: python -m scripts.summarize_day"
        )

    weekly_topic_totals, daily_totals, active_days = collect_weekly_data(summary_files)

    review = build_weekly_review()
    print(review)

    text_path = save_weekly_review(review)
    json_path = save_weekly_review_json(
        summary_files,
        weekly_topic_totals,
        daily_totals,
        active_days,
    )

    print(f"\nSaved weekly review to: {text_path}")
    print(f"Saved weekly JSON to: {json_path}")


if __name__ == "__main__":
    main()