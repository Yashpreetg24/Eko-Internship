from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.utils.vector_db_manager import VectorDB

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

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "EmployeeClaw API is running."}

@app.post("/knowledge/search")
def knowledge_search(request: SearchQuery):
    results = vector_db.search(request.query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
