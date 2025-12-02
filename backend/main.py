from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils.logger import logger
from config import settings
from api.routes import router,set_rag_system
from core.rag_system import RAG

rag_system = RAG()


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("RAG System Started...")
    rag_system.setup()
    set_rag_system(rag_system)
    yield
    logger.info("RAG System Closed!")



app = FastAPI(
    title="RAG System",
    version="1.0.0",
    description="Local RAG to query documents and sql",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add Routers
app.include_router(router=router,prefix="/api",tags=["RAG"])

@app.get("/")
def root():
    """Root endpoint with API information"""
    return JSONResponse({
        "name":"Local RAG Application",
        "version":"1.0.0",
        "endpoints":{
            "query":"/api/query",
            "upload":"/api/upload",
            "health":"/api/health",
            "documents":"/api/documents"
        }
    })

