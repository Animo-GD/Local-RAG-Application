from langgraph.graph import StateGraph,END
from core.state import GraphState
from services import LLMServices,SQLService,VectorestoreService
from utils.logger import logger
import dspy
from typing import Literal

class Graph:
    """Graph Flow for The RAG System"""
    def __init__(
            self,
            llm_services:LLMServices,
            vectorstore_services:VectorestoreService,
            sql_services:SQLService
            ):
        self.llm_services = llm_services
        self.vectorstore_services = vectorstore_services
        self.sql_services = sql_services
        self.graph = None

    def classify_query(self,state:GraphState)->GraphState:
        """Classify type of query (document, sql, general)"""
        question = state["question"]


    
    def build(self):
        """Build langgraph workflow"""
        workflow = StateGraph(GraphState)

    