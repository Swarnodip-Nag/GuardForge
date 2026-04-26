from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    risk_score = Column(Float)
    risk_category = Column(String)
    mitigation_suggestion = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
