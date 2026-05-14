import subprocess
from pathlib import Path
from datetime import datetime


OUTPUT_DIR = Path("outputs")
MODEL_NAME = "qwen2.5:7b"


def get_latest_summary_file():
    summaries = sorted(OUTPUT_DIR.glob("daily_summary_*.txt"))

    if not summaries:
        raise FileNotFoundError(
            "No daily summary files found. Run: python -m scripts.summarize_day"
        )

    return summaries[-1]


def build_prompt(summary_text: str) -> str:
    return f"""
You are Chronicle, a local AI assistant that helps the user understand their work patterns.

Use the activity summary below to produce a concise daily recap.

Focus on:
1. What the user mostly worked on
2. Notable context switches
3. Possible related projects or themes
4. One useful recommendation for tomorrow

Do not invent information not supported by the activity summary.

Activity Summary:
-----------------
{summary_text}

Return your answer in this format:

Daily Recap:
Focus Areas:
Context Switching:
Possible Themes:
Recommendation:
"""


def ask_ollama(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


def save_response(response: str):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / f"ai_recap_{datetime.now().date()}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response)

    return output_path


def main():
    summary_file = get_latest_summary_file()
    summary_text = summary_file.read_text(encoding="utf-8")

    print(f"Using summary file: {summary_file}")
    print(f"Using model: {MODEL_NAME}")
    print("\nAsking Chronicle...\n")

    prompt = build_prompt(summary_text)
    response = ask_ollama(prompt)

    print(response)

    output_path = save_response(response)
    print(f"\nSaved AI recap to: {output_path}")


if __name__ == "__main__":
    main()