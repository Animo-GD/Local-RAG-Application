from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Paths
    DOCUMENTS_DIR: str = "./data/documents"
    VECTORSTORE_DIR: str = "./data/chroma_db"
    DATABASE_PATH: str = "./data/database.db"
    
    # LLM Settings
    LLM_MODEL: str = "llama3.1:8b"
    LLM_TEMPERATURE: float = 0.0
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 20
    
    # Retrieval
    TOP_K_RESULTS: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create necessary directories
os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
os.makedirs(settings.VECTORSTORE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.DATABASE_PATH), exist_ok=True)