import json
import re
from groq import Groq
from app.config import settings
from app.agents.state import ComplaintState
from app.agents import prompts

_client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None


def _call_groq(prompt: str, model: str) -> str:
    if _client is None:
        raise RuntimeError("GROQ_API_KEY is not set - add it to backend/.env")
    resp = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return resp.choices[0].message.content


def _safe_json(text: str) -> dict:
    """LLMs sometimes wrap JSON in markdown fences or add stray text -
    this strips that so json.loads doesn't blow up the graph."""
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------------
# Core pipeline nodes
# ---------------------------------------------------------------------

def extract_fields_node(state: ComplaintState) -> dict:
    prompt = prompts.EXTRACTION_PROMPT.format(raw_text=state["raw_text"])
    raw = _call_groq(prompt, settings.GROQ_EXTRACTION_MODEL)
    fields = _safe_json(raw)
    attempts = state.get("extraction_attempts", 0) + 1
    return {"extracted_fields": fields, "extraction_attempts": attempts}


def check_completeness_node(state: ComplaintState) -> dict:
    fields = state.get("extracted_fields", {})
    missing = [f for f in prompts.COMPLETENESS_CHECK_FIELDS if not fields.get(f)]
    status = "complete" if not missing else "incomplete"
    return {"missing_fields": missing, "completeness_status": status}


def route_after_completeness(state: ComplaintState) -> str:
    # Cap retries so an unresponsive document can't loop forever.
    if state.get("completeness_status") == "complete" or state.get("extraction_attempts", 0) >= 2:
        return "classify_severity"
    return "extract_fields"


def classify_severity_node(state: ComplaintState) -> dict:
    prompt = prompts.SEVERITY_PROMPT.format(
        fields_json=json.dumps(state.get("extracted_fields", {}))
    )
    raw = _call_groq(prompt, settings.GROQ_REASONING_MODEL)
    result = _safe_json(raw)
    return {
        "initial_severity": result.get("severity", "Minor"),
        "priority": result.get("priority", "Low"),
    }


# ---------------------------------------------------------------------
# Bonus AI feature nodes
# ---------------------------------------------------------------------

def duplicate_detection_node(state: ComplaintState) -> dict:
    existing = state.get("existing_complaints", [])
    if not existing:
        return {"duplicate_of_ids": []}
    prompt = prompts.DUPLICATE_DETECTION_PROMPT.format(
        new_complaint_json=json.dumps(state.get("extracted_fields", {})),
        existing_complaints_json=json.dumps(existing),
    )
    raw = _call_groq(prompt, settings.GROQ_REASONING_MODEL)
    result = _safe_json(raw)
    return {"duplicate_of_ids": result.get("duplicate_of_ids", [])}


def root_cause_node(state: ComplaintState) -> dict:
    prompt = prompts.ROOT_CAUSE_PROMPT.format(
        fields_json=json.dumps(state.get("extracted_fields", {}))
    )
    raw = _call_groq(prompt, settings.GROQ_REASONING_MODEL)
    result = _safe_json(raw)
    return {"root_cause_suggestion": result.get("root_cause_suggestion", "")}


def capa_node(state: ComplaintState) -> dict:
    prompt = prompts.CAPA_PROMPT.format(
        fields_json=json.dumps(state.get("extracted_fields", {})),
        root_cause=state.get("root_cause_suggestion", ""),
    )
    raw = _call_groq(prompt, settings.GROQ_REASONING_MODEL)
    result = _safe_json(raw)
    return {"capa_suggestion": result.get("capa_suggestion", "")}


def summary_node(state: ComplaintState) -> dict:
    prompt = prompts.SUMMARY_PROMPT.format(
        fields_json=json.dumps(state.get("extracted_fields", {}))
    )
    raw = _call_groq(prompt, settings.GROQ_EXTRACTION_MODEL)
    result = _safe_json(raw)
    return {"ai_summary": result.get("ai_summary", "")}


def risk_classification_node(state: ComplaintState) -> dict:
    # Deterministic mapping keeps this fast and free of an extra LLM call -
    # severity/priority already carry the AI judgement.
    severity = state.get("initial_severity", "Minor")
    mapping = {"Critical": "High risk", "Major": "Moderate risk", "Minor": "Low risk"}
    return {"risk_classification": mapping.get(severity, "Low risk")}
