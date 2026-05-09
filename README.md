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
* [x] Modular architecture foundation

## Current Capabilities

Chronicle currently tracks:

* active applications
* foreground window titles
* session durations
* timestamped work sessions

All activity is stored locally in SQLite.

---

# Example Output

```text
2026-05-08T21:15:10 | Code.exe | activity_logger.py | 540s
2026-05-08T21:24:10 | chrome.exe | NOAA API documentation | 320s
2026-05-08T21:29:30 | OUTLOOK.EXE | Budget coordination email | 180s
```

---

# Tech Stack

## Backend

* Python 3.12
* SQLite
* psutil
* pywin32

## Planned

* FastAPI
* React / TypeScript
* Ollama
* ChromaDB or pgvector
* Docker

---

# Architecture

```text
Chronicle/
  agent/         # activity collection agents
  db/            # database initialization + schemas
  services/      # business logic
  scripts/       # runnable entry points
  data/          # local SQLite database
```

---

# Project Goals

## Near-Term Goals

* Build reliable local activity tracking
* Create searchable work history
* Generate daily summaries
* Detect focus blocks and context switching
* Create lightweight productivity analytics

## Long-Term Goals

* AI-generated work recaps
* Forecast upcoming tasks/schedules
* Semantic memory retrieval
* Browser research continuation
* Open-loop/task detection
* Multi-project awareness
* Calendar/email integration
* Local-first LLM reasoning
* Persistent operational memory

---

# Roadmap

## Phase 1 — Activity Tracking MVP

* [x] SQLite database
* [x] Active window monitoring
* [x] Session logging
* [ ] Activity query utilities
* [ ] Daily summary generation
* [ ] Timeline reconstruction

## Phase 2 — Behavioral Analytics

* [ ] Context switch detection
* [ ] Focus block estimation
* [ ] Time allocation analysis
* [ ] Productivity scoring
* [ ] Application categorization

## Phase 3 — AI Summarization

* [ ] Ollama integration
* [ ] Local LLM summaries
* [ ] Session recap generation
* [ ] Open-loop extraction
* [ ] Suggested next actions

## Phase 4 — Semantic Memory

* [ ] Embedding generation
* [ ] Vector database integration
* [ ] Semantic session search
* [ ] Cross-session context retrieval

## Phase 5 — Integrations

* [ ] Browser history integration
* [ ] Gmail integration
* [ ] Google Calendar integration
* [ ] Meeting transcription support
* [ ] Screenshot/OCR support

## Phase 6 — UI / Dashboard

* [ ] FastAPI backend
* [ ] React frontend
* [ ] Activity timeline visualization
* [ ] AI insight dashboard
* [ ] Search interface

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

---

# .gitignore

Recommended `.gitignore`:

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

The system is being developed incrementally:

1. reliable data collection
2. structured memory
3. intelligent summarization
4. forecasting and operational reasoning

---

# Inspiration

Chronicle is inspired by:

* operational intelligence systems
* workflow analytics platforms
* AI memory architectures
* context-aware assistants
* digital executive assistants

---

# Future Vision

The eventual goal is to build a system capable of:

* reconstructing complete work sessions
* identifying unfinished work automatically
* understanding long-term project context
* forecasting likely next actions
* surfacing forgotten research/topics
* functioning as a persistent AI operational assistant

Chronicle is intended to evolve into a local-first AI memory platform rather than simply a time-tracking application.

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
