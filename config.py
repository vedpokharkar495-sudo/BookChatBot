

import os

# Create folders if not exist
UPLOAD_FOLDER = "uploads"
VECTOR_DB_FOLDER = "vector_db"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

# Model settings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "google/flan-t5-base"  # Small, fast model

# Chunk settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# How many chunks to retrieve
TOP_K_RESULTS = 4
