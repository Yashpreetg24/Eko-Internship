import os
import sys
import random
from datetime import datetime, timedelta

# Add the project root to sys.path so we can import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.database import engine, Base, SessionLocal
from backend.models.models import Employee, Checklist, Log, Escalation, Asset, Department

def seed_data():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Clear existing data (optional, but good for idempotency)
    db.query(Employee).delete()
    db.query(Checklist).delete()
    db.query(Log).delete()
    db.query(Escalation).delete()
    db.query(Asset).delete()
    db.query(Department).delete()
    db.commit()

    print("Seeding departments...")
    departments = [
        Department(name="Engineering", head="Amit Singh", email="engineering@employeeclaw.com"),
        Department(name="HR", head="Priya Sharma", email="hr@employeeclaw.com"),
        Department(name="Finance", head="Ravi Patel", email="finance@employeeclaw.com"),
        Department(name="Sales", head="Neha Gupta", email="sales@employeeclaw.com")
    ]
    db.add_all(departments)
    db.commit()

    print("Seeding employees...")
    names = ["Rahul Sharma", "Sneha Kapoor", "Vikram Desai", "Anjali Verma", "Rohit Kumar", 
             "Pooja Joshi", "Suresh Nair", "Kavita Reddy", "Arjun Rao", "Divya Menon", 
             "Manish Tiwari", "Ritu Singh", "Akash Gupta", "Swati Patil", "Vishal Sharma", 
             "Aarti Patel", "Karan Malhotra", "Riya Das", "Sanjay Mehta", "Nidhi Agarwal"]
    
    depts = ["Engineering", "HR", "Finance", "Sales"]
    roles = {"Engineering": ["Software Engineer", "DevOps Engineer", "QA Engineer"],
             "HR": ["HR Executive", "Recruiter"],
             "Finance": ["Financial Analyst", "Accountant"],
             "Sales": ["Sales Manager", "Account Executive"]}

    employees = []
    for i, name in enumerate(names):
        dept = random.choice(depts)
        role = random.choice(roles[dept])
        emp = Employee(
            employee_id=f"EMP10{i:02d}",
            name=name,
            department=dept,
            joining_date=(datetime.utcnow() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            email=f"{name.split()[0].lower()}@employeeclaw.com",
            phone=f"+91 9876543{i:03d}",
            role=role,
            manager="Manager Name",
            documents=[{"type": "ID", "verified": True}, {"type": "Degree", "verified": random.choice([True, False])}],
            laptop_allocated=random.choice([True, False]),
            email_created=True,
            slack_access=random.choice([True, False]),
            vpn_setup=random.choice([True, False]),
            payroll_enabled=random.choice([True, False]),
            insurance_active=random.choice([True, False]),
            status=random.choice(["active", "pending", "escalated"]),
            onboarding_progress=random.choice([30, 70, 100])
        )
        employees.append(emp)
    
    db.add_all(employees)
    db.commit()

    print("Seeding checklists...")
    tasks = ["Submit Documents", "Laptop Allocation", "Email Creation", "Slack Setup", "VPN Setup", "Payroll Onboarding", "Insurance Form"]
    checklists = []
    for emp in employees:
        num_completed = int(emp.onboarding_progress / 100 * len(tasks)) # type: ignore
        for i, task in enumerate(tasks):
            completed = i < num_completed
            checklists.append(Checklist(
                employee_id=emp.employee_id,
                task_name=task,
                completed=completed,
                due_date=(datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d"),
                completed_date=datetime.utcnow().strftime("%Y-%m-%d") if completed else None
            ))
    db.add_all(checklists)
    db.commit()

    print("Seeding logs...")
    logs = []
    for _ in range(50):
        emp = random.choice(employees)
        logs.append(Log(
            employee_id=emp.employee_id,
            action=random.choice(["Document Upload", "Laptop Request", "Slack Access Check", "VPN Login Attempt"]),
            status=random.choice(["Success", "Failed"]),
            confidence=random.randint(60, 99),
            resolved=random.choice([True, False])
        ))
    db.add_all(logs)
    db.commit()

    print("Seeding escalations...")
    escalations = []
    for _ in range(15):
        emp = random.choice(employees)
        status = random.choice(["open", "resolved"])
        escalations.append(Escalation(
            employee_id=emp.employee_id,
            reason=random.choice(["Laptop not delivered", "Background check failed", "Payroll issue", "VPN access denied"]),
            priority=random.choice(["low", "medium", "high"]),
            assigned_team=random.choice(["HR", "IT", "Finance", "Payroll"]),
            status=status,
            resolved_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") if status == "resolved" else None
        ))
    db.add_all(escalations)
    db.commit()

    print("Seeding assets...")
    assets = []
    for _ in range(15):
        emp = random.choice(employees)
        assets.append(Asset(
            employee_id=emp.employee_id,
            asset_type=random.choice(["laptop", "phone", "access_card"]),
            serial_number=f"SN-{random.randint(1000, 9999)}",
            allocated=True,
            allocated_date=(datetime.utcnow() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
        ))
    db.add_all(assets)
    db.commit()

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_data()
