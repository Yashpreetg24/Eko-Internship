import os

sops = {
    "joining_process.md": "Joining Process",
    "document_verification.md": "Document Verification",
    "laptop_allocation.md": "Laptop Allocation",
    "company_email.md": "Company Email",
    "slack_setup.md": "Slack Setup",
    "vpn_setup.md": "VPN Setup",
    "leave_policy.md": "Leave Policy",
    "payroll.md": "Payroll",
    "insurance.md": "Insurance",
    "background_verification.md": "Background Verification",
    "attendance.md": "Attendance",
    "probation.md": "Probation",
    "exit_policy.md": "Exit Policy",
    "holiday_calendar.md": "Holiday Calendar",
    "security_policy.md": "Security Policy",
    "employee_benefits.md": "Employee Benefits",
    "travel_policy.md": "Travel Policy",
    "code_of_conduct.md": "Code of Conduct",
    "work_from_home_policy.md": "Work from Home Policy",
    "performance_review.md": "Performance Review"
}

template = """# {title}

## Purpose
This document outlines the standard operating procedure for {title}.

## Eligibility
All full-time employees are eligible for {title} subject to departmental approval.

## Step-by-step process
1. Initiate the {title} request via the employee portal.
2. Manager reviews and approves the request.
3. The relevant team processes the request.
4. Confirmation is sent to the employee.

## Expected timeline
The expected timeline for {title} is 3-5 business days.

## Escalation contact
For any issues regarding {title}, please contact the HR Helpdesk at hr@employeeclaw.com.
"""

os.makedirs("knowledge", exist_ok=True)

for filename, title in sops.items():
    path = os.path.join("knowledge", filename)
    with open(path, "w") as f:
        f.write(template.format(title=title))

print("Successfully generated 20 SOPs.")
