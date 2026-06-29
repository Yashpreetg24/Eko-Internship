import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal
from backend.models.models import Log

def log_interaction(employee_id: str, action: str, status: str, confidence: int, resolved: bool):
    db = SessionLocal()
    try:
        new_log = Log(
            employee_id=employee_id,
            action=action,
            status=status,
            confidence=confidence,
            resolved=resolved,
            timestamp=datetime.utcnow().isoformat()
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {"log_id": new_log.id, "status": "success"}
    finally:
        db.close()
