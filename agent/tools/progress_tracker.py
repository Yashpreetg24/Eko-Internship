import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal
from backend.models.models import Employee

def get_progress(employee_id: str):
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            return {"progress": employee.onboarding_progress}
        return {"error": "Employee not found"}
    finally:
        db.close()
