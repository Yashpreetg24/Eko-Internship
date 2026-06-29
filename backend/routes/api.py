from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.database.database import get_db
from backend.models.models import Employee, Checklist, Log, Escalation, Department
from sqlalchemy import func

router = APIRouter()

# --- Schemas ---
class EscalationUpdate(BaseModel):
    status: str

# --- Endpoints ---

@router.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/employees/{employee_id}")
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.get("/employees/{employee_id}/checklist")
def get_employee_checklist(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    checklists = db.query(Checklist).filter(Checklist.employee_id == employee_id).all()
    return checklists

@router.get("/employees/{employee_id}/progress")
def get_employee_progress(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"progress": emp.onboarding_progress}

@router.get("/employees/{employee_id}/logs")
def get_employee_logs(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    logs = db.query(Log).filter(Log.employee_id == employee_id).order_by(Log.timestamp.desc()).all()
    return logs

@router.get("/escalations")
def get_all_escalations(db: Session = Depends(get_db)):
    return db.query(Escalation).order_by(Escalation.created_at.desc()).all()

@router.get("/escalations/{escalation_id}")
def get_escalation(escalation_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escalation).filter(Escalation.id == escalation_id).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return esc

@router.patch("/escalations/{escalation_id}")
def update_escalation(escalation_id: int, payload: EscalationUpdate, db: Session = Depends(get_db)):
    esc = db.query(Escalation).filter(Escalation.id == escalation_id).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation not found")
    
    esc.status = payload.status
    if payload.status == "resolved":
        esc.resolved_at = datetime.utcnow().isoformat()
        
    db.commit()
    db.refresh(esc)
    return esc

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_employees = db.query(Employee).count()
    completed_onboarding = db.query(Employee).filter(Employee.onboarding_progress == 100).count()
    pending_onboarding = total_employees - completed_onboarding
    escalated_cases = db.query(Escalation).filter(Escalation.status == "open").count()
    
    avg_progress = db.query(func.avg(Employee.onboarding_progress)).scalar() or 0
    
    # Most common issue
    most_common_issue = db.query(Escalation.reason, func.count(Escalation.reason).label("count")).group_by(Escalation.reason).order_by(func.count(Escalation.reason).desc()).first()
    most_common_issue_name = most_common_issue[0] if most_common_issue else "N/A"
    
    # Average onboarding days (mocked as difference from joining_date to now if completed)
    # Since we need complex SQL, we'll return a static/simulated number for now or calculate in memory
    
    # Escalations by team
    escalations_by_team = db.query(Escalation.assigned_team, func.count(Escalation.assigned_team)).group_by(Escalation.assigned_team).all()
    team_data = {item[0]: item[1] for item in escalations_by_team}
    
    return {
        "total_employees": total_employees,
        "completed_onboarding": completed_onboarding,
        "pending_onboarding": pending_onboarding,
        "escalated_cases": escalated_cases,
        "average_completion_percentage": round(avg_progress, 2),
        "most_common_issue": most_common_issue_name,
        "average_onboarding_days": 12.5, # Placeholder for average completion days
        "escalations_by_team": team_data
    }
