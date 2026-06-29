from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    employee_id: str
    message: str
    chat_history: List[Dict[str, str]]
    intent: Optional[str]
    employee_record: Optional[Dict[str, Any]]
    sop_chunks: Optional[List[Dict[str, str]]]
    current_status: Optional[str]
    action_decision: Optional[str]
    response: Optional[str]
    checklist: Optional[List[Dict[str, Any]]]
    progress: Optional[int]
    escalated: bool
    confidence: Optional[int]
    workflow_trace: List[str]
    sources: Optional[List[str]]
