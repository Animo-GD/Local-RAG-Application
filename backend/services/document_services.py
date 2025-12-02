from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader,TextLoader,CSVLoader
from langchain_classic.schema import Document
from typing import List
from config import settings
from utils.logger import logger
from pathlib import Path

class DocumentServices:
    """Services for document loading and processing"""
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )

    def load_document(self,file_path:str)->List[Document]:
        """Load a single document"""
        try:
            path = Path(file_path)
            logger.info(f"Loading Document {path.name}")
            if not path.exists():
                raise FileNotFoundError(f"File not found {file_path}")
            if path.suffix == ".pdf":
                loader = PyPDFLoader(str(path))
            elif path.suffix in [".txt",".md"]:
                loader = TextLoader(str(path))
            elif path.suffix == ".csv":
                loader = CSVLoader(str(path))
            else:
                raise ValueError(f"Unsupported file type: {path.suffix}")
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} pages/sections")
            return documents
        except Exception as e:
            logger.error(f"Error Loading Document {file_path}: {e}")
            raise
    
    def load_all_documents(self)->List[Document]:
        """Load all documents from documents directory"""
        all_documents=[]
        docs_path = Path(settings.DOCUMENTS_DIR)
        for file_path in docs_path.glob("*"):
            if file_path.is_file() and file_path.suffix in [".pdf",".txt",".md",".csv"]:
                try:
                    documents = self.load_document(str(file_path))
                    all_documents.extend(documents)
                except Exception as e:
                    logger.error(f"Filed to load {file_path}:{e}")
        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def split_documents(self,documents:List[Document])->List[Document]:
        """Split Documents into chunks"""
        try:
            logger.info("Splitting documents into chunks...")
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Erro splitting documents: {e}")
            raise