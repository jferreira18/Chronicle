from pathlib import Path
import json
import subprocess
import re


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OUTPUT_DIR = Path("outputs")
MODEL_NAME = "qwen2.5:7b"

LOGGER_PROCESS = None


class AskRequest(BaseModel):
    question: str

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

def clean_ollama_output(text: str) -> str:
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    text = text.replace("�", "")
    return text.strip()


def load_recent_context():
    context_parts = []

    for prefix in ["daily_summary", "weekly_review"]:
        files = sorted(OUTPUT_DIR.glob(f"{prefix}_*.json"))

        if files:
            latest = files[-1]

            with open(latest, "r", encoding="utf-8") as f:
                context_parts.append(
                    f"{prefix.upper()}:\n{json.dumps(json.load(f), indent=2)}"
                )

    ai_files = sorted(OUTPUT_DIR.glob("ai_recap_*.txt"))

    if ai_files:
        latest_ai = ai_files[-1]

        context_parts.append(
            f"AI_RECAP:\n{latest_ai.read_text(encoding='utf-8')}"
        )

    return "\n\n".join(context_parts)

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

@app.post("/ask")
def ask_chronicle(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    context = load_recent_context()

    if not context:
        raise HTTPException(
            status_code=404,
            detail="No Chronicle context found.",
        )

    prompt = f"""
You are Chronicle, a local-first AI workflow memory assistant.

Answer the user's question using only the Chronicle context below.

Be practical, concise, and evidence-based.
Do not invent activity that is not present in the context.

Chronicle Context:
------------------
{context}

User Question:
--------------
{request.question}

Answer:
"""

    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=result.stderr,
        )

    answer = clean_ollama_output(result.stdout)

    return {
        "question": request.question,
        "answer": answer,
        "model": MODEL_NAME,
    }

@app.post("/logger/start")
def start_logger():
    global LOGGER_PROCESS

    if LOGGER_PROCESS is not None and LOGGER_PROCESS.poll() is None:
        return {"status": "already_running"}

    LOGGER_PROCESS = subprocess.Popen(
        ["python", "-m", "scripts.run_logger"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return {"status": "started", "pid": LOGGER_PROCESS.pid}


@app.post("/logger/stop")
def stop_logger():
    global LOGGER_PROCESS

    if LOGGER_PROCESS is None or LOGGER_PROCESS.poll() is not None:
        regenerate_daily_summary()
        return {"status": "not_running", "summary": "regenerated"}

    LOGGER_PROCESS.terminate()
    LOGGER_PROCESS = None

    regenerate_daily_summary()

    return {"status": "stopped", "summary": "regenerated"}


@app.get("/logger/status")
def logger_status():
    if LOGGER_PROCESS is not None and LOGGER_PROCESS.poll() is None:
        return {"status": "running", "pid": LOGGER_PROCESS.pid}

    return {"status": "stopped"}

@app.post("/refresh/daily")
def refresh_daily():
    regenerate_daily_summary()
    return load_latest_json("daily_summary")


def regenerate_daily_summary():
    result = subprocess.run(
        ["python", "-m", "scripts.summarize_day"],
        text=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)

    return {"status": "summary_regenerated"}