from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question to ask RAG System")
    model: Optional[str] = "llama3.1:8b"
    selected_files: Optional[List[str]] = None
    selected_tables: Optional[List[str]] = None  # Add this

class QueryResponse(BaseModel):
    answer: str
    query_type: str
    context: Optional[str] = ""
    sql_query: Optional[str] = ""
    metadata: Optional[Dict] = {}

class UploadResponse(BaseModel):
    message: str
    filename: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str] = {}

class ErrorResponse(BaseModel):
    details: str
    error_code: Optional[str] = None
    
class DeleteFileRequest(BaseModel):
    filename: str