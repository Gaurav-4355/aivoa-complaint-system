from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models, schemas
from app.document_reader import extract_text_from_upload
from app.agents.graph import complaint_graph

router = APIRouter(prefix="/complaints", tags=["complaints"])


def _run_pipeline(raw_text: str, db: Session) -> dict:
    existing = db.query(models.Complaint).all()
    existing_payload = [
        {
            "id": c.id,
            "product_name": c.product_name,
            "batch_lot_number": c.batch_lot_number,
            "complaint_type": c.complaint_type,
            "detailed_description": c.detailed_description,
        }
        for c in existing
    ]
    result = complaint_graph.invoke(
        {"raw_text": raw_text, "existing_complaints": existing_payload}
    )
    return result


@router.post("/extract", response_model=schemas.ExtractResponse)
async def extract_complaint(
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Powers the right-hand 'AI Complaint Intake Assistant' panel: accepts
    either a document upload or pasted text, runs the full LangGraph
    pipeline, and returns everything needed to auto-populate the form.
    """
    if file is not None:
        content = await file.read()
        raw_text = extract_text_from_upload(file.filename, content)
    elif text:
        raw_text = text
    else:
        raise HTTPException(400, "Provide either a file or text")

    if not raw_text.strip():
        raise HTTPException(422, "Could not read any text from the input")

    result = _run_pipeline(raw_text, db)

    return schemas.ExtractResponse(
        extracted_fields=result.get("extracted_fields", {}),
        completeness_status=result.get("completeness_status", "incomplete"),
        missing_fields=result.get("missing_fields", []),
        initial_severity=result.get("initial_severity", "Minor"),
        priority=result.get("priority", "Low"),
        duplicate_of_ids=result.get("duplicate_of_ids", []),
        root_cause_suggestion=result.get("root_cause_suggestion", ""),
        capa_suggestion=result.get("capa_suggestion", ""),
        ai_summary=result.get("ai_summary", ""),
        risk_classification=result.get("risk_classification", "Low risk"),
    )


@router.post("", response_model=schemas.ComplaintOut)
def save_complaint(payload: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    complaint = models.Complaint(**payload.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.get("", response_model=list[schemas.ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    return db.query(models.Complaint).order_by(models.Complaint.id.desc()).all()


@router.get("/{complaint_id}", response_model=schemas.ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(models.Complaint).get(complaint_id)
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    return complaint
