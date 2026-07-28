EXTRACTION_PROMPT = """You are a pharmaceutical quality assurance assistant. Read the customer
complaint text below and extract the following fields as strict JSON. Use
null for any field you cannot find - never invent data.

Fields:
- complaint_source (Email, Phone, Portal, Distributor, or other)
- customer_name
- product_name
- product_strength_grade
- batch_lot_number
- manufacturing_date (YYYY-MM-DD if possible)
- expiry_date (YYYY-MM-DD if possible)
- quantity_affected (include unit, e.g. "12 kg" or "500 units")
- complaint_type (Packaging defect, Efficacy issue, Contamination,
  Labeling error, Adverse reaction, or other)
- complaint_date (YYYY-MM-DD if possible)
- detailed_description (2-4 sentence neutral summary of what went wrong)

Respond with ONLY a JSON object with exactly these keys. No preamble, no
markdown fences.

Complaint text:
---
{raw_text}
---
"""

SEVERITY_PROMPT = """You are classifying a pharmaceutical customer complaint for a QMS
(Quality Management System) intake workflow.

Complaint details (JSON):
{fields_json}

Classify:
- severity: one of "Critical", "Major", "Minor"
  (Critical = patient safety risk / contamination / wrong product;
   Major = product does not meet quality spec but no direct safety risk;
   Minor = cosmetic, labeling, or documentation issue)
- priority: one of "High", "Medium", "Low"

Respond with ONLY JSON: {{"severity": "...", "priority": "..."}}
"""

COMPLETENESS_CHECK_FIELDS = [
    "customer_name",
    "product_name",
    "batch_lot_number",
    "complaint_type",
    "detailed_description",
]

DUPLICATE_DETECTION_PROMPT = """Compare the NEW complaint below against a list of EXISTING complaints.
Return the ids of any existing complaints that plausibly describe the same
underlying incident (same product, same batch/lot, and a similar issue
description). Be conservative - only flag genuine likely duplicates.

NEW complaint:
{new_complaint_json}

EXISTING complaints:
{existing_complaints_json}

Respond with ONLY JSON: {{"duplicate_of_ids": [list of integers, possibly empty]}}
"""

ROOT_CAUSE_PROMPT = """You are a pharmaceutical QA engineer. Based on the complaint details
below, suggest the most likely root cause category and a one-sentence
rationale. This is a preliminary AI suggestion for a human investigator,
not a final determination.

Complaint details (JSON):
{fields_json}

Respond with ONLY JSON: {{"root_cause_suggestion": "..."}}
Keep it to 2-3 sentences.
"""

CAPA_PROMPT = """You are a pharmaceutical QA engineer drafting a preliminary CAPA
(Corrective and Preventive Action) recommendation for the complaint below.
This is a starting point for the investigator, not a final CAPA.

Complaint details (JSON):
{fields_json}

Root cause suggestion:
{root_cause}

Respond with ONLY JSON: {{"capa_suggestion": "..."}}
Keep the corrective + preventive action to 3-4 sentences total.
"""

SUMMARY_PROMPT = """Summarize this pharmaceutical complaint in 2 sentences for a QA manager
who needs to triage it quickly. Be factual and neutral.

Complaint details (JSON):
{fields_json}

Respond with ONLY JSON: {{"ai_summary": "..."}}
"""

CHAT_SYSTEM_PROMPT = """You are the AI Complaint Intake Assistant embedded in a pharmaceutical
QMS complaint form. Answer the user's question using only the complaint
context provided. If the context does not contain the answer, say so
plainly instead of guessing. Keep answers concise (2-4 sentences) and use
a professional QA tone. Always note that AI responses may contain errors
and should be verified by the user.

Complaint context (JSON):
{context_json}
"""
