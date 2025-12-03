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
        if not rag_system:
            raise HTTPException(status_code=503,detail="RAG system not initialized")
        request_config = {
        "model": request.model,
        "selected_files": request.selected_files,
        "selected_tables": request.selected_tables,  
        }
        result = rag_system.query(request.query, config=request_config)

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
    

@router.delete("/document")
async def delete_document(request: DeleteFileRequest):
    """Delete a document"""
    try:
        filename = sanitize_filename(request.filename)
        filepath = os.path.join(settings.DOCUMENTS_DIR, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Deleted file: {filename}")
            
            # Delete from vectorstore
            if rag_system:
                try:
                    rag_system.vectorstore_service.delete_documents_by_filename(filename)
                    logger.info(f"Deleted embeddings for: {filename}")
                except Exception as e:
                    logger.warning(f"Could not delete embeddings: {e}")
            
            return {"message": f"File {filename} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload",response_model=UploadResponse,responses={400: {"model": ErrorResponse}})
async def upload(file:UploadFile = File(...)):
    """
    Upload a document to the RAG system.
    
    Supported formats: PDF, TXT, MD, CSV
    """
    try:
        # Validate File
        if not file.filename:
            raise HTTPException(status_code=400,detail="No File Selected!")
        if not is_valid_document(file.filename):
            raise HTTPException(status_code=400,detail="File Not Supported!, Only Supported(PDF,TXT,MD,CSV)")
        
        # Clean File name
        filename = sanitize_filename(file.filename)
        # Save File
        filepath = os.path.join(settings.DOCUMENTS_DIR,filename)
        with open(filepath,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        
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
    if not rag_system:
        raise HTTPException(status_code=503,detail="RAG system not initialized")
    
    services = {
        "llm":"healthy" if rag_system.llm_service.get_llm() else "unavaiable",
        "vectorstore":"healthy" if rag_system.vectorstore_service.vectorstore else "unavaliable",
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

@router.get("/tables")
async def get_tables():
    """
    Get available database tables with schema information
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        tables = rag_system.sql_service.get_avaliable_tables()
        
        # Get schema info for each table
        tables_info = []
        for table in tables:
            try:
                schema = rag_system.sql_service.get_table_schema(table)
                tables_info.append({
                    "name": table,
                    "schema": schema
                })
            except Exception as e:
                logger.warning(f"Could not get schema for table {table}: {e}")
                tables_info.append({
                    "name": table,
                    "schema": None
                })
        
        return {
            "tables": tables_info,
            "count": len(tables_info)
        }
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))