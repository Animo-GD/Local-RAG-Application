from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from utils.logger import logger
from config import settings
class VectorestoreService:
    """Service for vector store operations."""
    def __init__(self) -> None:
        self.embedding = None
        self.vectorestore = None

    def initialize(self):
        """Initialize vectore store and embedding model"""
        try:
            logger.info(f"Initialize embedding...")
            self.embedding = OllamaEmbeddings(model=settings.EMBEDDING_MODEL)
            logger.info(f"Loading vectore store...")
            self.vectorestore = Chroma(
                persist_directory=settings.VECTORSTORE_DIR,
                embedding_function=self.embedding
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vectore store {e}")
            raise
    def add_documents(self,documents):
        """Add documents to the vector store"""
        try:
            if not documents:
                logger.warning("No documents to add")
                return
            logger.info(f"Adding {len(documents)} to vector store...")
            self.vectorestore.add_documents(documents=documents) if self.vectorestore else None
            logger.info("Documents added successfully")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def similarity_search(self,query:str,k:int=None):
        """Performe Similarity Search"""
        try:
            k = k or settings.TOP_K_RESULTS
            logger.info(f"Performing similarity search for the provided query...")
            results = self.vectorestore.similarity_search(query,k=k) if self.vectorestore else []
            logger.info(f"Found {len(results)} results") 
            return results
        except Exception as e:
            logger.error(f"Error in similarity search {e}")
            return []
        
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            self.vectorestore.delete_collection() if self.vectorestore else None
            logger.info("Collection deleted")
        except Exception as e:
            logger.error(f"Error deleting collection {e}")
