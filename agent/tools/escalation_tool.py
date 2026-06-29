import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal
from backend.models.models import Escalation

def create_escalation(employee_id: str, reason: str, priority: str, assigned_team: str):
    db = SessionLocal()
    try:
        escalation = Escalation(
            employee_id=employee_id,
            reason=reason,
            priority=priority,
            assigned_team=assigned_team,
            status="open",
            created_at=datetime.utcnow().isoformat()
        )
        db.add(escalation)
        db.commit()
        db.refresh(escalation)
        return {"escalation_id": escalation.id, "status": "success"}
    finally:
        db.close()
