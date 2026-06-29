from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    joining_date = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String)
    manager = Column(String)
    documents = Column(JSON, default=[])
    laptop_allocated = Column(Boolean, default=False)
    email_created = Column(Boolean, default=False)
    slack_access = Column(Boolean, default=False)
    vpn_setup = Column(Boolean, default=False)
    payroll_enabled = Column(Boolean, default=False)
    insurance_active = Column(Boolean, default=False)
    onboarding_progress = Column(Integer, default=0)
    status = Column(String, default="pending") # active/pending/escalated

    checklists = relationship("Checklist", back_populates="employee")
    logs = relationship("Log", back_populates="employee")
    escalations = relationship("Escalation", back_populates="employee")
    assets = relationship("Asset", back_populates="employee")

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"))
    task_name = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(String)
    completed_date = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="checklists")

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"))
    action = Column(String)
    status = Column(String)
    confidence = Column(Integer)
    resolved = Column(Boolean, default=False)
    timestamp = Column(String, default=lambda: datetime.utcnow().isoformat())

    employee = relationship("Employee", back_populates="logs")

class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"))
    reason = Column(String)
    priority = Column(String) # low/medium/high
    assigned_team = Column(String) # HR/IT/Finance/Payroll
    status = Column(String, default="open") # open/resolved
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    resolved_at = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="escalations")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"))
    asset_type = Column(String) # laptop/phone/access_card
    serial_number = Column(String)
    allocated = Column(Boolean, default=False)
    allocated_date = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="assets")

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    head = Column(String)
    email = Column(String)
