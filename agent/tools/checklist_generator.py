import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal
from backend.models.models import Checklist

def get_checklist(employee_id: str):
    db = SessionLocal()
    try:
        checklists = db.query(Checklist).filter(Checklist.employee_id == employee_id).all()
        if checklists:
            return [{"task_name": c.task_name, "completed": c.completed, "due_date": c.due_date, "completed_date": c.completed_date} for c in checklists]
        return []
    finally:
        db.close()
