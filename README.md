# EmployeeClaw

**EmployeeClaw** is an Autonomous Employee Onboarding AI Agent designed to streamline the HR onboarding process. It leverages an advanced LangGraph workflow to intelligently assist new hires, resolve issues, and proactively escalate blockers.

## Features
- **Conversational AI Interface**: Employees can chat to resolve queries about laptops, payroll, policies, etc.
- **Proactive Monitoring**: Automatically detects and surfaces overdue tasks before the employee even asks.
- **Workflow Tracing**: Transparently displays the agent's internal thought process, database checks, and confidence scores.
- **HR Analytics Dashboard**: Real-time insights into company-wide onboarding progress and escalation bottlenecks.
- **Automated Escalation Routing**: Intelligently routes unsolved or high-risk issues to IT, HR, or Finance.

## Architecture Description
EmployeeClaw is split into a modern React frontend and a robust FastAPI backend. The core intelligence resides in a LangGraph-powered AI workflow. It uses Sentence Transformers and FAISS for fast RAG (Retrieval-Augmented Generation) against HR SOPs. A local SQLite database tracks state across the onboarding lifecycle.

## Tech Stack
| Component       | Technology                               |
|-----------------|------------------------------------------|
| **Frontend**    | React, Tailwind CSS, Vite, Recharts      |
| **Backend**     | FastAPI, Uvicorn                         |
| **Agent Core**  | LangGraph, LangChain                     |
| **LLM Engine**  | OpenAI (gpt-4o-mini)                     |
| **Retrieval**   | FAISS (Vector DB), Sentence Transformers |
| **Database**    | SQLite, SQLAlchemy                       |

## Installation Steps

### 1. Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database (creates dummy data)
python backend/seed.py

# Build the FAISS Vector Index
python backend/utils/vector_db_manager.py

# Run the FastAPI server
uvicorn backend.main:app --reload
```

### 2. Frontend Setup
```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Run Vite dev server
npm run dev
```

### 3. Environment Variables
Make sure to create a `.env` file in the root directory and add your OpenAI API Key:
```
OPENAI_API_KEY=your_api_key_here
```

## Screenshots
*(Insert placeholders here)*
- `[Screenshot 1: Chat Portal UI with Workflow Trace]`
- `[Screenshot 2: HR Analytics Dashboard]`
- `[Screenshot 3: Employee Profile View]`

## Demo Video
[Link to Demo Video](#) *(Coming Soon)*

## Future Improvements
- **Integration with Slack/Teams**: Move the chat interface directly into corporate messaging apps.
- **Multi-modal Support**: Allow employees to upload PDFs (e.g., IDs) directly in the chat for verification.
- **Cloud Migration**: Move from SQLite/FAISS to Postgres/pgvector for scale.
