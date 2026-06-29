import sys
from agent.graph import agent_app

initial_state = {
    "employee_id": "EMP1001",
    "message": "What is the attendance policy",
    "chat_history": [],
    "intent": None,
    "employee_record": None,
    "sop_chunks": None,
    "current_status": None,
    "action_decision": None,
    "response": None,
    "checklist": None,
    "progress": None,
    "escalated": False,
    "confidence": None,
    "workflow_trace": [],
    "sources": []
}

try:
    result = agent_app.invoke(initial_state)
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
