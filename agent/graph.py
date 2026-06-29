import sys
import os
import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.state import AgentState
from agent.tools.employee_lookup import get_employee
from agent.tools.knowledge_search import search_knowledge
from agent.tools.checklist_generator import get_checklist
from agent.tools.progress_tracker import get_progress
from agent.tools.escalation_tool import create_escalation
from agent.tools.logger import log_interaction

# Setup LLM
# In production, ensure OPENAI_API_KEY is in environment
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def classify_intent(state: AgentState):
    prompt = f"""
    Classify the following employee message into one of these intents:
    ONBOARDING_QUERY, ASSET_REQUEST, POLICY_QUESTION, PAYROLL_ISSUE, ACCESS_ISSUE, ESCALATION_REQUIRED, GENERAL_GREETING, UNKNOWN.
    
    Message: {state['message']}
    
    Return ONLY the exact intent string.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.strip()
    state["intent"] = intent
    state["workflow_trace"] = [f"✓ Intent classified: {intent}"]
    return state

def retrieve_employee(state: AgentState):
    emp = get_employee(state["employee_id"])
    if "error" in emp:
        state["escalated"] = True
        state["workflow_trace"].append("✗ Employee record not found")
    else:
        state["employee_record"] = emp
        state["workflow_trace"].append(f"✓ Employee record retrieved: {emp['name']}")
    return state

def retrieve_sop(state: AgentState):
    sops = search_knowledge(state["message"])
    if isinstance(sops, dict) and "error" in sops:
        state["escalated"] = True
        state["workflow_trace"].append("✗ SOP not found")
        state["sources"] = []
    else:
        state["sop_chunks"] = sops
        state["sources"] = [s["filename"] for s in sops]
        state["workflow_trace"].append(f"✓ SOP retrieved: {', '.join(state['sources'])}")
    return state

def check_status(state: AgentState):
    if state["escalated"]:
        return state
    
    intent = state["intent"]
    emp = state["employee_record"]
    status_str = "Checked general status."
    
    if intent == "ASSET_REQUEST":
        status_str = f"Laptop allocated: {emp['laptop_allocated']}"
    elif intent == "ACCESS_ISSUE":
        status_str = f"Slack access: {emp['slack_access']}, VPN: {emp['vpn_setup']}"
    elif intent == "PAYROLL_ISSUE":
        status_str = f"Payroll enabled: {emp['payroll_enabled']}"
        
    state["current_status"] = status_str
    state["workflow_trace"].append(f"✓ Status checked: {status_str}")
    return state

def determine_action(state: AgentState):
    if state["escalated"]:
        return state
        
    intent = state["intent"]
    emp = state["employee_record"]
    action = "No specific action required."
    
    if intent == "PAYROLL_ISSUE":
        state["escalated"] = True
        action = "Escalated to Finance due to payroll issue."
    elif intent == "ASSET_REQUEST" and not emp.get("laptop_allocated"):
        state["escalated"] = True
        action = "Escalated to IT for laptop allocation."
        
    state["action_decision"] = action
    state["workflow_trace"].append(f"✓ Action: {action}")
    return state

def generate_response(state: AgentState):
    if state["escalated"]:
        state["response"] = "I need to escalate this issue to our human team. A ticket has been created."
        return state
        
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in state.get('chat_history', [])])
    
    prompt = f"""
    You are an autonomous HR onboarding AI for EmployeeClaw.
    Employee Name: {state['employee_record']['name']}
    Intent: {state['intent']}
    SOP Context: {state['sop_chunks']}
    Current Status: {state['current_status']}
    
    Conversation History:
    {history_text}
    
    Employee Message: {state['message']}
    
    Generate a helpful, professional, personalized response addressing their query using the SOP context.
    """
    response = llm.invoke([SystemMessage(content="You are EmployeeClaw HR Assistant."), HumanMessage(content=prompt)])
    state["response"] = response.content.strip()
    return state

def update_checklist(state: AgentState):
    if state.get("employee_record"):
        checklist = get_checklist(state["employee_id"])
        progress = get_progress(state["employee_id"])
        state["checklist"] = checklist
        state["progress"] = progress.get("progress", 0)
    else:
        state["checklist"] = []
        state["progress"] = 0
    return state

def confidence_check(state: AgentState):
    if state["escalated"]:
        state["confidence"] = 100
        return state
        
    prompt = f"""
    Score your confidence in the response you generated for the employee from 0 to 100.
    Just return the integer number.
    Response: {state['response']}
    SOP Context: {state['sop_chunks']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        conf = int(response.content.strip())
    except:
        conf = 85
        
    state["confidence"] = conf
    state["workflow_trace"].append(f"✓ Confidence: {conf}%")
    
    if conf < 70:
        state["escalated"] = True
        state["workflow_trace"].append("✗ Confidence below 70%, escalating")
    else:
        state["workflow_trace"].append("✓ No escalation required")
        
    return state

def escalate(state: AgentState):
    if state["escalated"]:
        intent = state.get("intent", "UNKNOWN")
        reason = state.get("message", "Unknown reason")
        team = "HR"
        if intent == "PAYROLL_ISSUE":
            team = "Finance"
        elif intent == "ASSET_REQUEST" or intent == "ACCESS_ISSUE":
            team = "IT"
            
        esc = create_escalation(
            employee_id=state["employee_id"],
            reason=reason,
            priority="high",
            assigned_team=team
        )
        state["response"] = f"Your request has been escalated to the {team} team (Ticket #{esc['escalation_id']}). They will get back to you shortly."
    return state

def log_interaction_node(state: AgentState):
    log_interaction(
        employee_id=state["employee_id"],
        action=state.get("intent", "UNKNOWN"),
        status="Escalated" if state.get("escalated") else "Resolved",
        confidence=state.get("confidence", 0),
        resolved=not state.get("escalated")
    )
    state["workflow_trace"].append("✓ Interaction logged")
    return state

# Routing logic
def should_escalate_early(state: AgentState):
    if state.get("escalated"):
        return "escalate"
    return "retrieve_sop"

def should_escalate_after_action(state: AgentState):
    if state.get("escalated"):
        return "escalate"
    return "generate_response"

def should_escalate_after_confidence(state: AgentState):
    if state.get("escalated"):
        return "escalate"
    return "log_interaction"

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_employee", retrieve_employee)
workflow.add_node("retrieve_sop", retrieve_sop)
workflow.add_node("check_status", check_status)
workflow.add_node("determine_action", determine_action)
workflow.add_node("generate_response", generate_response)
workflow.add_node("update_checklist", update_checklist)
workflow.add_node("confidence_check", confidence_check)
workflow.add_node("escalate", escalate)
workflow.add_node("log_interaction", log_interaction_node)

workflow.set_entry_point("classify_intent")
workflow.add_edge("classify_intent", "retrieve_employee")

workflow.add_conditional_edges("retrieve_employee", should_escalate_early, {
    "escalate": "escalate",
    "retrieve_sop": "retrieve_sop"
})

workflow.add_edge("retrieve_sop", "check_status")
workflow.add_edge("check_status", "determine_action")

workflow.add_conditional_edges("determine_action", should_escalate_after_action, {
    "escalate": "escalate",
    "generate_response": "generate_response"
})

workflow.add_edge("generate_response", "update_checklist")
workflow.add_edge("update_checklist", "confidence_check")

workflow.add_conditional_edges("confidence_check", should_escalate_after_confidence, {
    "escalate": "escalate",
    "log_interaction": "log_interaction"
})

workflow.add_edge("escalate", "log_interaction")
workflow.add_edge("log_interaction", END)

agent_app = workflow.compile()
