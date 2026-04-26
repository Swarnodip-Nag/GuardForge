from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AnalysisRequest(BaseModel):
    prompt: str

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prompt: str
    risk_score: float
    risk_category: str
    mitigation_suggestion: str
    created_at: datetime
