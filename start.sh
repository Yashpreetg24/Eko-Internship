#!/bin/bash
echo "Starting deployment setup..."

# 1. Build FAISS Vector Database
echo "Building FAISS Index..."
python backend/utils/vector_db_manager.py

# 2. Seed SQLite Database
echo "Seeding Database..."
python backend/seed.py

# 3. Start Backend Server
echo "Starting Uvicorn..."
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
