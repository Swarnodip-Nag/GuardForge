from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database
from .engines import detection, scoring, mitigation

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="GuardForge AI V1", description="Compliance Copilot for LLM Systems")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In V2, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze_prompt(request: schemas.AnalysisRequest, db: Session = Depends(database.get_db)):
    # 1. Detect
    detect_res = detection.detect_risks(request.prompt)
    
    # 2. Score
    score_res = scoring.calculate_score(detect_res)
    
    # 3. Mitigate
    mitigation_res = mitigation.generate_mitigation(score_res, detect_res)
    
    # 4. Save to DB
    db_record = models.AnalysisRecord(
        prompt=request.prompt,
        risk_score=score_res["score"],
        risk_category=score_res["category"],
        mitigation_suggestion=mitigation_res
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record

@app.get("/history", response_model=List[schemas.AnalysisResponse])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    records = db.query(models.AnalysisRecord).order_by(models.AnalysisRecord.id.desc()).offset(skip).limit(limit).all()
    return records
