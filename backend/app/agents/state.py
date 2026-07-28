from typing import TypedDict, Optional


class ComplaintState(TypedDict, total=False):
    """
    The shared object that flows through every node in the LangGraph
    pipeline. Each node reads what it needs and returns a partial dict
    that LangGraph merges back into this state.
    """
    raw_text: str                       # cleaned text pulled from upload/paste
    extracted_fields: dict               # structured fields from the LLM
    missing_fields: list[str]
    completeness_status: str             # "complete" | "incomplete"
    extraction_attempts: int             # guards against infinite re-extraction loops

    initial_severity: str
    priority: str

    existing_complaints: list[dict]      # loaded once for duplicate comparison
    duplicate_of_ids: list[int]

    root_cause_suggestion: str
    capa_suggestion: str
    ai_summary: str
    risk_classification: str
