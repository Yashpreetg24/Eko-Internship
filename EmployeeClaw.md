# EmployeeClaw Final Documentation

## Project Overview
EmployeeClaw is an end-to-end autonomous employee onboarding agent. Instead of replacing human HR completely, it acts as a first line of defense that holds state (knowing where the employee is in their onboarding journey), retrieves policies automatically (RAG), and executes tasks across APIs (via Agentic tools). If it fails or is unconfident, it seamlessly escalates the issue to the appropriate department.

## Technical Milestones Reached
1. **Full-stack scaffolding** with React, Tailwind, and FastAPI.
2. **Database modeling** for Employees, Logs, Escalations, and Checklists using SQLAlchemy.
3. **Knowledge Retrieval Engine** using HuggingFace sentence embeddings and FAISS for sub-millisecond semantic search across 20 simulated HR SOPs.
4. **Agentic Tooling** containing 7 discrete, robust tools allowing the LLM to inspect state, check progress, retrieve docs, and escalate tickets.
5. **LangGraph State Machine**, connecting 10 specialized node actions logically. Includes intent routing and dynamic fallbacks.
6. **Robust API routing** via FastAPI to power custom dashboards.
7. **Modern React Interface** utilizing Recharts, Lucide Icons, and React Router for a multi-view portal.
8. **Memory Management** so the LLM retains multi-turn conversational context scoped to specific employee sessions.
9. **Proactive Monitoring** that warns users of overdue tasks at the start of a session instead of waiting for them to ask.
10. **Documentation & Polish**, resulting in this comprehensive README and clean, robust error handling.

## Challenges & Design Decisions
- **Why LangGraph over standard LangChain chains?** Onboarding workflows are cyclic and highly conditional. LangGraph allows us to define nodes like `confidence_check` which can loop back into `escalate` or proceed to `log_interaction` without convoluted `if/else` hell inside a single LLM prompt.
- **Why FAISS locally?** While Pinecone or Weaviate are great for production, FAISS allows this prototype to be completely self-contained and run efficiently on a local machine without external network calls (other than OpenAI).
- **Proactive vs Reactive AI**: Standard chat bots only answer queries. We intentionally designed the frontend to call the `reminders` endpoint *before* the first chat interaction so the agent can actively shape the conversation.

## Running the Application
Refer to the `README.md` for exact CLI instructions.
The backend exposes `http://localhost:8000/docs` (Swagger UI) for raw API testing.
The frontend runs on `http://localhost:5173`. 
