from fastapi import APIRouter,UploadFile,File,HTTPException
from .model import *
from utils.helpers import is_valid_document,sanitize_filename
from config import settings
from utils.logger import logger
import shutil
import os
from pathlib import Path


router = APIRouter()
rag_system = None

def set_rag_system(system):
    global rag_system
    rag_system = system



@router.post("/query",response_model=QueryResponse,responses={400: {"model": ErrorResponse}})
async def query(request:QueryRequest):
    """
    Query the RAG system with a question.
    
    The system will automatically determine whether to search documents,
    query the database, or provide a general response.
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400,detail="Question cannot be empty")
        result = rag_system.query(request.query)

        return QueryResponse(
            answer=result['answer'],
            query_type=result['query_type'],
            context=result.get('context', ''),
            sql_query=result.get('sql_query', ''),
            metadata=result.get('metadata', {})
        )
    except Exception as e:
        logger.info(f"Error processing query: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    


@router.post("/upload",response_model=UploadResponse,responses={400: {"model": ErrorResponse}})
async def upload(file:UploadFile = File(...)):
    """
    Upload a document to the RAG system.
    
    Supported formats: PDF, TXT, MD, CSV
    """
    try:
        # Vaildat File
        if not file.filename:
            raise HTTPException(status_code=400,detail="No File Selected!")
        if not is_valid_document(file.filename):
            raise HTTPException(status_code=400,detail="File Not Supported!, Only Supported(PDF,TXT,MD,CSV)")
        
        # Clean File name
        filename = sanitize_filename(file.filename)
        # Save File
        filepath = os.path.join(settings.DOCUMENTS_DIR,filename)
        with open(filepath,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer) # Save it chunk by chunk in size 16KB
        
        logger.info("Document Uploaded Successfully")

    except Exception as e:
        logger.error(f"Error Uploading Document:{e}")
        raise HTTPException(status_code=500,detail=str(e))
        
    return UploadResponse(message="Uploaded Successfully",filename=filename,status="success")

@router.get("/health",response_model=HealthResponse)
async def health():
    """
    Checking the rag system health
    """
    services = {
        "llm":"healthy" if rag_system.llm_service.get_llm() else "unavaiable",
        "vectorstore":"healthy" if rag_system.vectorstore_service.vectorestore else "unavaliable",
        "sql_db":"healthy" if rag_system.sql_service.db else "unavaliable"
    }
    return HealthResponse(status="healthy" if rag_system.initialized else "initializing",
                          services=services)

@router.get("/document")
async def document():
    """
    Getting the uploaded documents
    """
    try:
        docs_path = Path(settings.DOCUMENTS_DIR)
        docs = [f.name for f in docs_path.iterdir() if f.is_file()]
        return {"documents":docs,"count":len(docs)}
    except Exception as e:
        logger.error(f"Error listing documents {e}")
        raise HTTPException(status_code=500,detail=str(e))
    
