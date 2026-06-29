import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")

os.makedirs(VECTOR_DB_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index.bin")
DOCS_PATH = os.path.join(VECTOR_DB_DIR, "docs.pkl")

# Load model
# all-MiniLM-L6-v2 is a lightweight model
model = SentenceTransformer('all-MiniLM-L6-v2')

def build_index():
    print("Building FAISS index...")
    documents = []
    
    # Read all markdown files
    for filename in os.listdir(KNOWLEDGE_DIR):
        if filename.endswith(".md"):
            path = os.path.join(KNOWLEDGE_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # For simplicity, we use the whole file as a chunk.
                # In production, we'd chunk this by paragraphs or sections.
                documents.append({
                    "filename": filename,
                    "content": content
                })
    
    if not documents:
        print("No documents found in knowledge directory.")
        return

    # Create embeddings
    texts = [doc["content"] for doc in documents]
    embeddings = model.encode(texts)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save index and docs mapping
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(documents, f)
        
    print(f"Index built with {len(documents)} documents.")

class VectorDB:
    def __init__(self):
        if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
            build_index()
        self.index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            self.documents = pickle.load(f)
            
    def search(self, query: str, top_k: int = 3):
        query_embedding = np.array(model.encode([query])).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx])
        return results

if __name__ == "__main__":
    build_index()
