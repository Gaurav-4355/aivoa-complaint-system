from pydantic import BaseModel, Field
from typing import Optional


class ExtractedFields(BaseModel):
    """
    The structured schema the LLM is asked to fill in. This is passed to
    Groq as a JSON-schema instruction so field extraction is consistent.
    """
    complaint_source: Optional[str] = Field(None, description="e.g. Email, Phone, Portal, Distributor")
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_strength_grade: Optional[str] = None
    batch_lot_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None
    complaint_type: Optional[str] = Field(None, description="e.g. Packaging defect, Efficacy issue, Contamination, Labeling error")
    complaint_date: Optional[str] = None
    detailed_description: Optional[str] = None


class ExtractTextRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    extracted_fields: ExtractedFields
    completeness_status: str
    missing_fields: list[str]
    initial_severity: str
    priority: str
    duplicate_of_ids: list[int]
    root_cause_suggestion: str
    capa_suggestion: str
    ai_summary: str
    risk_classification: str


class ComplaintCreate(ExtractedFields):
    initial_severity: Optional[str] = None
    priority: Optional[str] = None
    completeness_status: Optional[str] = None
    missing_fields: Optional[list[str]] = None
    duplicate_of_ids: Optional[list[int]] = None
    root_cause_suggestion: Optional[str] = None
    capa_suggestion: Optional[str] = None
    ai_summary: Optional[str] = None
    risk_classification: Optional[str] = None
    raw_source_text: Optional[str] = None


class ComplaintOut(ComplaintCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    complaint_id: Optional[int] = None
    context: Optional[ExtractedFields] = None
    question: str


class ChatResponse(BaseModel):
    answer: str
