from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.utils.vector_db_manager import VectorDB
from agent.graph import agent_app

app = FastAPI(title="EmployeeClaw", description="Autonomous Employee Onboarding AI Agent")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Vector DB instance
vector_db = VectorDB()

class SearchQuery(BaseModel):
    query: str

class ChatRequest(BaseModel):
    employee_id: str
    message: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "EmployeeClaw API is running."}

@app.post("/knowledge/search")
def knowledge_search(request: SearchQuery):
    results = vector_db.search(request.query)
    return {"results": results}

@app.post("/agent/chat")
def agent_chat(request: ChatRequest):
    initial_state = {
        "employee_id": request.employee_id,
        "message": request.message,
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
    
    result = agent_app.invoke(initial_state)
    
    return {
        "response": result.get("response", "No response generated"),
        "workflow_trace": result.get("workflow_trace", []),
        "checklist": result.get("checklist", []),
        "progress": result.get("progress", 0),
        "escalated": result.get("escalated", False),
        "confidence": result.get("confidence", 0),
        "sources": result.get("sources", [])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
