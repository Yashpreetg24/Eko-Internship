import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.utils.vector_db_manager import VectorDB

# Initialize DB once
vector_db = VectorDB()

def search_knowledge(query: str):
    results = vector_db.search(query, top_k=3)
    if not results:
        return {"error": "No relevant SOP found"}
    return results
