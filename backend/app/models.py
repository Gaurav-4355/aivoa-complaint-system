from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    # 1. Origin & customer details
    complaint_source = Column(String(100))
    customer_name = Column(String(200))

    # 2. Product & batch identification
    product_name = Column(String(200))
    product_strength_grade = Column(String(100))
    batch_lot_number = Column(String(100))
    manufacturing_date = Column(String(50))
    expiry_date = Column(String(50))
    quantity_affected = Column(String(50))

    # 3. Complaint details
    complaint_type = Column(String(100))
    complaint_date = Column(String(50))
    detailed_description = Column(Text)

    # 4. Initial assessment & priority
    initial_severity = Column(String(50))
    priority = Column(String(50))

    # AI-generated bonus fields
    completeness_status = Column(String(50), default="unknown")
    missing_fields = Column(JSON, default=list)
    duplicate_of_ids = Column(JSON, default=list)
    root_cause_suggestion = Column(Text)
    capa_suggestion = Column(Text)
    ai_summary = Column(Text)
    risk_classification = Column(String(50))

    raw_source_text = Column(Text)
    status = Column(String(50), default="pending_triage")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
