import os
import json
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .database import engine
from .llm_parser import parse_message_with_llm, client
from .triage_logic import calculate_rescue_score
from .notifications import send_slack_alert

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="CrisisTriage AI API")

origins = ["http://localhost:5173", "http://127.0.0.1:5173", "https://crisis-triage-ai.netlify.app" ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

VOLUNTEER_TEAMS = {"Team Alpha (Medical)": {}, "Team Bravo (Logistics)": {}, "Team Charlie (S&R)": {}}

def find_closest_team(lat, lon): # Note: This is a simplified placeholder
    return "Team Charlie (S&R)"

def process_and_save_message(message: str, db: Session):
    if not message or not message.strip(): return None
    extracted_data = parse_message_with_llm(message)
    result = calculate_rescue_score(extracted_data, original_message=message)
    new_incident = models.Incident(
        message=message,
        priority_score=result['priority_score'],
        details=json.loads(extracted_data.model_dump_json())
    )
    db.add(new_incident); db.commit(); db.refresh(new_incident)
    if new_incident.priority_score >= 75:
        send_slack_alert(priority_score=new_incident.priority_score, message=new_incident.message, needs=new_incident.details.get('resource_needs', []), incident_id=new_incident.id)
    return new_incident

class TriageRequest(BaseModel): message: str
class AppealRequest(BaseModel): incident_ids: List[int]
class TelegramMessage(BaseModel): text: Optional[str] = None
class TelegramUpdate(BaseModel): update_id: int; message: Optional[TelegramMessage] = None

@app.get("/incidents/", summary="Get all incidents")
def get_all_incidents(db: Session = Depends(database.get_db)):
    return db.query(models.Incident).order_by(models.Incident.priority_score.desc()).all()

@app.post("/triage/", summary="Triage a new incident")
def triage_web_message(request: TriageRequest, db: Session = Depends(database.get_db)):
    return process_and_save_message(request.message, db)

@app.post("/telegram-webhook/", summary="Receive messages from Telegram")
def telegram_webhook(update: TelegramUpdate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    if update.message and update.message.text:
        background_tasks.add_task(process_and_save_message, update.message.text, db)
    return {"status": "ok"}

@app.post("/incidents/{incident_id}/acknowledge", summary="Acknowledge an incident")
def acknowledge_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if incident and incident.status == "Needs Dispatch":
        incident.status = "Acknowledged"
        db.commit(); return {"status": "success", "new_status": "Acknowledged"}
    return {"status": "failed"}

@app.post("/incidents/{incident_id}/dispatch", summary="Simulate dispatching a team")
def dispatch_team(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident or incident.status != "Acknowledged":
        return {"status": "failed", "reason": "Incident must be acknowledged first."}
    
    details = json.loads(incident.details) if isinstance(incident.details, str) else incident.details
    team_to_dispatch = find_closest_team(details.get('latitude'), details.get('longitude'))
    
    incident.status = f"Dispatched: {team_to_dispatch}"
    db.commit()
    return {"status": "success", "new_status": incident.status}

@app.post("/generate-appeal/", summary="Generate a fundraising appeal")
def generate_appeal(request: AppealRequest, db: Session = Depends(database.get_db)):
    incidents = db.query(models.Incident).filter(models.Incident.id.in_(request.incident_ids)).all()
    if not incidents: return {"error": "No incidents selected."}
    summary = ". ".join([i.message for i in incidents])
    prompt = f"Based on these real crisis reports: '{summary}', write a short, compelling fundraising appeal for social media."
    try:
        if not client: return {"error": "LLM Client not available."}
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama3-8b-8192", temperature=0.7)
        return {"appeal": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}