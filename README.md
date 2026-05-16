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
* [x] Local Ollama AI recap generation
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
* local AI-generated activity recaps

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
* SQLite
* psutil
* pywin32

## AI / Analytics

* Ollama
* Local LLM inference
* Rule-based semantic categorization
* Sessionization pipeline

## Planned

* FastAPI
* React / TypeScript
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
  outputs/       # generated summaries + AI recaps
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

* [ ] FastAPI backend
* [ ] React frontend
* [ ] Activity timeline visualization
* [ ] AI insight dashboard
* [ ] Search interface
* [ ] Conversational “Ask Chronicle” interface

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

'''bash
python -m scripts.weekly_review
'''

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
