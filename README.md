# Chronicle

Chronicle is an AI-assisted workflow memory and productivity intelligence platform designed to passively monitor work activity, reconstruct operational timelines, and generate intelligent summaries and forecasting insights.

The long-term vision is to create a local-first “operational memory system” capable of understanding:

* what a user worked on
* how time was spent
* what research/tasks remain unfinished
* what actions should likely happen next

Chronicle aims to function as a lightweight AI executive assistant that builds contextual memory over time.

---

# Current MVP Status

## Implemented

* [x] Python project/package structure
* [x] SQLite database initialization
* [x] Active window detection
* [x] Process/application monitoring
* [x] Session duration tracking
* [x] Local behavioral event logging
* [x] Sessionization and activity grouping
* [x] Activity categorization and topic inference
* [x] Daily summary generation
* [x] Weekly behavioral aggregation
* [x] Daily and weekly JSON exports
* [x] Local Ollama AI recap generation
* [x] Conversational “Ask Chronicle” querying
* [x] FastAPI local backend
* [x] React + TypeScript frontend dashboard
* [x] GUI logger controls
* [x] Local AI query interface
* [x] Exportable summary and recap artifacts
* [x] Modular architecture foundation

## Current Capabilities

Chronicle currently tracks and reconstructs:

* active applications
* foreground window titles
* session durations
* timestamped work sessions
* inferred work topics
* context switching behavior
* lightweight project relationships
* daily operational summaries
* weekly behavioral aggregation
* local AI-generated activity recaps
* conversational querying over activity history
* structured JSON exports for downstream analytics
* local GUI-based interaction and control

All activity processing and AI inference currently run locally.

---

# Example Output

## Raw Activity Log

```text
2026-05-08T21:15:10 | Code.exe | activity_logger.py | 540s
2026-05-08T21:24:10 | chrome.exe | NOAA API documentation | 320s
2026-05-08T21:29:30 | OUTLOOK.EXE | Budget coordination email | 180s
```

## Sessionized Activity

```text
23:11-23:16 | Chronicle Development | 6.5 min
- activity_service.py - Chronicle
- activity_logger.py - Chronicle
- AI Work Monitoring Tools

18:59-19:01 | Music / Guitar | 5.2 min
- The Brudi Brothers, 26 chords & tabs found @ Ultimate-Guitar.com
- LAY A BURDEN ON ME CHORDS by The Brudi Brothers
```

## AI Recap Example

```text
Daily Recap:
Most activity centered around Chronicle development, specifically around
sessionization, categorization, and workflow reconstruction features.

The user also briefly switched into career research, workstation troubleshooting,
and entertainment-related browsing.

Possible Themes:
- AI workflow intelligence
- productivity analytics
- operational memory systems

Recommendation:
Continue improving Chronicle's semantic understanding before expanding into
vector databases or autonomous behaviors.
```

---

# Tech Stack

## Backend

* Python 3.12
* FastAPI
* SQLite
* psutil
* pywin32
* uvicorn

## Frontend

* React
* TypeScript
* Vite

## AI / Analytics

* Ollama
* Local LLM inference
* Rule-based semantic categorization
* Sessionization pipeline
* Conversational activity querying

## Planned

* Tauri
* ChromaDB or pgvector
* Docker
* Semantic embeddings
* Streaming inference

---

# Architecture

```text
Chronicle/
  agent/         # activity collection agents
  api/           # FastAPI backend
  db/            # database initialization + schemas
  frontend/      # React + TypeScript GUI
  services/      # business logic
  scripts/       # runnable entry points
  outputs/       # summaries, JSON exports, AI recaps
  data/          # local SQLite database
```

---

# Roadmap

## Phase 1 — Activity Tracking MVP

* [x] SQLite database
* [x] Active window monitoring
* [x] Session logging
* [x] Activity query utilities
* [x] Daily summary generation
* [x] Timeline reconstruction
* [x] Sessionization pipeline
* [x] Topic inference and categorization

## Phase 2 — Behavioral Analytics

* [x] Context switch detection
* [ ] Focus block estimation
* [ ] Time allocation analysis
* [ ] Productivity scoring
* [ ] Persistent project relationship mapping
* [ ] Deep work estimation

## Phase 3 — AI Summarization

* [x] Ollama integration
* [x] Local LLM summaries
* [x] Session recap generation
* [x] Conversational “Ask Chronicle” querying
* [ ] Open-loop extraction
* [ ] Suggested next actions
* [ ] Multi-day behavioral analysis

## Phase 4 — Semantic Memory

* [ ] Embedding generation
* [ ] Vector database integration
* [ ] Semantic session search
* [ ] Cross-session context retrieval
* [ ] Long-term project memory

## Phase 5 — Integrations

* [ ] Browser history integration
* [ ] Gmail integration
* [ ] Google Calendar integration
* [ ] Meeting transcription support
* [ ] Screenshot/OCR support

## Phase 6 — UI / Dashboard

* [x] FastAPI backend
* [x] React frontend
* [x] AI recap dashboard
* [x] Ask Chronicle interface
* [x] GUI logger controls
* [ ] Activity timeline visualization
* [ ] Search interface
* [ ] Live dashboard updates
* [ ] Tauri desktop application packaging

## Phase 7 — Advanced Agent Features

* [ ] Workflow forecasting
* [ ] Research continuation engine
* [ ] Autonomous task reminders
* [ ] Multi-agent orchestration
* [ ] Local-first autonomous assistant

---

# Setup

## Create Environment

```bash
conda env create -f environment.yml
conda activate chronicle
```

## Initialize Database

```bash
python -m scripts.init_db
```

## Run Activity Logger

```bash
python -m scripts.run_logger
```

## View Logged Activity

```bash
python -m scripts.view_today
```

## Generate Daily Summary

```bash
python -m scripts.summarize_day
```

## Generate Weekly Summary

```bash
python -m scripts.weekly_review
```

## Generate AI Recap

Install Ollama and pull a local model:

```bash
ollama pull qwen2.5:7b
```

Then run:

```bash
python -m scripts.ask_chronicle
```

---

# Running Chronicle GUI

## Start FastAPI Backend

```bash
uvicorn api.main:app --reload
```

## Start React Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will typically run at:

```text
http://localhost:5173
```

FastAPI backend will run at:

```text
http://127.0.0.1:8000
```

---

# Ask Chronicle

Chronicle includes a conversational local AI interface capable of answering questions about recent activity, behavioral patterns, and project focus.

Example questions:

```text
What did I focus on most today?
What projects recur together?
Was I context switching frequently?
What should I revisit tomorrow?
```

The system currently uses local Ollama inference and FastAPI endpoints to provide conversational retrieval over Chronicle summaries and behavioral data.

---

# Planned Desktop Application

Chronicle is being architected toward a local-first desktop application using:

```text
React + TypeScript
→ Tauri desktop shell
→ FastAPI backend
→ Local SQLite + Ollama
```

The long-term goal is to package Chronicle as a standalone executable desktop AI assistant capable of persistent workflow memory and operational reasoning.

---

# Current TODOs

* [ ] Automatic dashboard refresh after logger stop/start
* [ ] Live activity timeline visualization
* [ ] Browser history integration
* [ ] Embedding/vector memory system
* [ ] Streaming AI responses
* [ ] Semantic search
* [ ] Tauri desktop packaging
* [ ] Persistent conversational memory
* [ ] Focus and interruption scoring

---

# Recommended .gitignore

```gitignore
# Python
__pycache__/
*.pyc

# Virtual environments
.env
venv/
.venv/

# Conda
.envs/
conda-meta/

# Database
data/*.db

# Generated outputs
outputs/

# VS Code
.vscode/

# OS files
.DS_Store
Thumbs.db
```

---

# Design Philosophy

Chronicle is intentionally designed as:

* local-first
* privacy-conscious
* modular
* extensible
* AI-native
* explainable

The system is being developed incrementally:

1. reliable activity capture
2. structured operational memory
3. semantic understanding
4. AI-assisted summarization
5. long-term forecasting and reasoning

Chronicle prioritizes deterministic preprocessing and interpretable pipelines before introducing autonomous AI behavior.

---

# Future Vision

The long-term goal is to build a local-first operational intelligence system capable of:

* reconstructing complete workflows
* understanding long-term project context
* detecting unfinished/open-loop tasks
* surfacing forgotten research automatically
* forecasting likely future work
* identifying recurring behavioral patterns
* functioning as a persistent AI executive assistant

Chronicle is intended to evolve beyond time tracking into a continuously learning operational memory platform.

---

# Author

Jacob Ferreira

Biomedical Engineer | Army Engineer Officer | OMSCS Student

Interests:

* AI systems
* operational intelligence
* workflow automation
* distributed systems
* human-AI collaboration
