import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal
from backend.models.models import Employee

def get_employee(employee_id: str):
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            return {
                "employee_id": employee.employee_id,
                "name": employee.name,
                "department": employee.department,
                "role": employee.role,
                "joining_date": employee.joining_date,
                "email": employee.email,
                "laptop_allocated": employee.laptop_allocated,
                "slack_access": employee.slack_access,
                "vpn_setup": employee.vpn_setup,
                "payroll_enabled": employee.payroll_enabled,
                "status": employee.status,
                "onboarding_progress": employee.onboarding_progress
            }
        return {"error": "Employee not found"}
    finally:
        db.close()
