from core.graph import Graph
from services import LLMServices,VectorestoreService,DocumentServices,SQLService
from utils.logger import logger

class RAG:
    """Main RAG Sysetm"""
    def __init__(self) -> None:
        self.llm_service = LLMServices()
        self.vectorstore_service = VectorestoreService()
        self.document_service = DocumentServices()
        self.sql_service = SQLService()
        self.graph = None
        self.initialized = False

    def setup(self):
        """Initialize all services and build the graph"""
        try:
            logger.info("="*50)
            logger.info("Starting RAG System Setup")
            logger.info("="*50)

            self.llm_service.intialize()
            self.vectorstore_service.initialize()
            self.sql_service.initialize()

            self._load_initial_documents()
            self.graph = Graph(
                self.llm_service,
                self.vectorstore_service,
                self.sql_service,
                self.document_service
            )
            self.graph.build()
            self.initialized = True
            logger.info("="*50)
            logger.info("RAG System Setup Completed")
            logger.info("="*50)
        except Exception as e:
            logger.error(f"Failed to setup RAG System: {e}")
            raise

    def _load_initial_documents(self):
        """load and index any existing documents"""
        try:
            documents = self.document_service.load_all_documents()
            if documents:
                chunks = self.document_service.split_documents(documents)
                self.vectorstore_service.add_documents(chunks)
                logger.info(f"Indexed {len(chunks)} document chunks")
        except Exception as e:
            logger.warning(f"Couldn't load initial documents: {e}")

    def add_document(self,file_path:str):
        """Add new document to the system"""
        try:
            documents = self.document_service.load_document(file_path)
            chunks = self.document_service.split_documents(documents=documents)
            self.vectorstore_service.add_documents(chunks)
            logger.info(f"Document Added {file_path}")
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise

    def query(self,question:str)->dict:
        """Query The RAG System"""
        if not self.initialized:
            raise RuntimeError("RAG System not initialized. Call Setup() first")
        logger.info(f"Processing query: {question}")
        result = self.graph.invoke(question) if self.graph else {}
        return {
            "answer":result["answer"],
            "query_type":result["query_type"],
            "context":result.get("context",""),
            "sql_query":result.get("sql_query",""),
            "metadata":result.get("metadata",{})
        }
