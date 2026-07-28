# AIVOA — AI-Powered Customer Complaint Management System



## Stack (matches the mandatory requirements)

| Requirement | Used |
|---|---|
| Frontend | React + Redux Toolkit (Vite) |
| Backend | Python + FastAPI |
| AI orchestration | LangGraph |
| LLMs | Groq — `gemma2-9b-it` for extraction/summary, `llama-3.3-70b-versatile` for reasoning steps |
| Database | MySQL|
| Font | Google Inter |

## How the AI pipeline works

`backend/app/agents/graph.py` builds a LangGraph `StateGraph`:

```
extract_fields → check_completeness ─(incomplete, <2 attempts)→ extract_fields (loop)
                       │(complete or attempts exhausted)
                       ▼
              classify_severity → classify_risk → detect_duplicates
                       → suggest_root_cause → suggest_capa → summarize → END
```

A single shared `ComplaintState` (see `agents/state.py`) carries data
through every node — raw text in, structured fields + severity +
duplicates + summary out. `check_completeness` is a **conditional edge**:
if required fields are missing it loops back into extraction (capped at
2 attempts so a bad document can't loop forever) before moving on.

## Bonus AI features implemented

All six suggested bonus features from the assignment are implemented as
LangGraph nodes, not bolted on separately:

- **Complaint Completeness Checker** — `check_completeness_node`, drives the conditional loop and surfaces missing fields in the UI
- **Root Cause Recommendation** — `root_cause_node`
- **Duplicate Complaint Detection** — `duplicate_detection_node`, compares against complaints already saved to the database
- **CAPA Recommendation** — `capa_node`, built on top of the root cause suggestion
- **Complaint Summary** — `summary_node`, shown as a banner above the form
- **AI Risk Classification** — `risk_classification_node`, derived from severity

## Project layout

```
backend/
  app/
    agents/        # LangGraph state, prompts, nodes, graph assembly
    routers/        # /complaints (extract + CRUD), /chat
    main.py, config.py, database.py, models.py, schemas.py
  requirements.txt
  .env.example
frontend/
  src/
    store/          # Redux slices: complaintForm, aiAssistant
    components/      # ComplaintForm, AIAssistantPanel, FileUpload, ChatBox
    api/client.js
sample-complaints/    # Two realistic pharma complaint texts (one is a
                       # near-duplicate of the other, for testing the
                       # duplicate-detection bonus feature)
```

## Running it

**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then add your GROQ_API_KEY
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000. Try dragging in
`sample-complaints/sample_complaint_1.txt`, saving it, then dragging in
`sample_complaint_2_duplicate.txt` to see the duplicate-detection bonus
feature flag it.

## What's a deliberate simplification (per the assignment's own notes)

- Document parsing is basic text extraction (pypdf/python-docx), not
  production-grade OCR — the assignment explicitly says this isn't required.
- No auth/user management — out of scope for the assignment.
- Extraction retry loop is capped at 2 attempts rather than unbounded,
  to keep the demo deterministic.

## For the demo video

Suggested walkthrough order (matches what the assignment asks you to
explain): frontend upload/paste → `POST /complaints/extract` →
`document_reader.py` text extraction → `complaint_graph.invoke()` →
walk the LangGraph nodes in `agents/graph.py` one by one → response
shape in `schemas.ExtractResponse` → `populatedFromExtraction` reducer
→ form and AI Copilot panel updating on screen.
