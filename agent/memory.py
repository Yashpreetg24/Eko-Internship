from typing import List, Dict

# In-memory store for session memory
# Key: employee_id, Value: List of messages (e.g. [{"role": "user", "content": "..."}, {"role": "ai", "content": "..."}])
session_memory: Dict[str, List[Dict[str, str]]] = {}

def get_history(employee_id: str) -> List[Dict[str, str]]:
    """Retrieve chat history for an employee."""
    return session_memory.get(employee_id, [])

def add_message(employee_id: str, role: str, content: str):
    """Append a message to the employee's history."""
    if employee_id not in session_memory:
        session_memory[employee_id] = []
    session_memory[employee_id].append({"role": role, "content": content})

def clear_history(employee_id: str):
    """Clear chat history for an employee."""
    if employee_id in session_memory:
        session_memory[employee_id] = []
