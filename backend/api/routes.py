from fastapi import APIRouter,UploadFile,File,HTTPException
from .model import *
from utils.helpers import is_valid_document,sanitize_filename
from config import settings
from utils.logger import logger
import shutil
import os
from pathlib import Path


router = APIRouter()

@router.post("/query",response_model=QueryResponse)
async def query(request:QueryRequest):
    """
    Query the RAG system with a question.
    
    The system will automatically determine whether to search documents,
    query the database, or provide a general response.
    """
    return QueryResponse(
        response="answer",
        query_type="type"
    )

@router.post("/upload",response_model=UploadResponse)
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
    return HealthResponse(status="",services={"":""})

@router.get("/document",response_model=DocumentResponse)
async def document():
    """
    Getting the uploaded documents
    """
    return DocumentResponse(details="")
