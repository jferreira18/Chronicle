from pathlib import Path
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


OUTPUT_DIR = Path("outputs")

app = FastAPI(title="Chronicle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_latest_json(prefix: str):
    files = sorted(OUTPUT_DIR.glob(f"{prefix}_*.json"))

    if not files:
        raise HTTPException(status_code=404, detail=f"No {prefix} files found.")

    latest = files[-1]

    with open(latest, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["_source_file"] = str(latest)
    return data


@app.get("/")
def root():
    return {
        "name": "Chronicle API",
        "status": "running",
    }


@app.get("/daily-summary")
def daily_summary():
    return load_latest_json("daily_summary")


@app.get("/weekly-review")
def weekly_review():
    return load_latest_json("weekly_review")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ai-recap")
def ai_recap():
    files = sorted(OUTPUT_DIR.glob("ai_recap_*.txt"))

    if not files:
        raise HTTPException(status_code=404, detail="No AI recap files found.")

    latest = files[-1]

    with open(latest, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "source_file": str(latest),
        "recap": text,
    }