from pydantic_settings import BaseSettings
from typing import List
import os

from pathlib import Path

BASE_DIR = Path(__file__).parent

class Settings(BaseSettings):

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://localhost:5174"  # Backup Vite port
    ]
    
    # Paths
    DOCUMENTS_DIR: str = "./data/documents"
    VECTORSTORE_DIR: str = "./data/chroma_db"
    DATABASE_PATH:str = str(BASE_DIR / "data" / "database.db")
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    # LLM Settings
    LLM_MODEL: str = "llama3.1:8b"
    LLM_TEMPERATURE: float = 0.0
    EMBEDDING_MODEL: str = "nomic-embed-text:latest"
    
    # Chunking
    CHUNK_SIZE: int = 500
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