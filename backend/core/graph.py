from langgraph.graph import StateGraph,END
from core.state import GraphState
from services import LLMServices,SQLService,VectorestoreService,DocumentServices
from utils.logger import logger
from core import SmartQueryClassifier

class Graph:
    """Graph Flow for The RAG System"""
    def __init__(
            self,
            llm_services:LLMServices,
            vectorstore_services:VectorestoreService,
            sql_services:SQLService,
            document_services:DocumentServices
            ):
        self.llm_services = llm_services
        self.vectorstore_services = vectorstore_services
        self.sql_services = sql_services
        self.document_services = document_services
        self.graph = None

    def classify_query(self, state: GraphState) -> GraphState:
        """Classify type of query (document, sql, general)"""
        question = state["question"]
        config = state.get("config", {})
        selected_tables = config.get("selected_tables", [])
        
        logger.info("Start Classify User's Query...")
        classifier = SmartQueryClassifier()
        documents = self.document_services.load_all_documents()
        doc_titles = [doc.metadata.get('source', 'Unknown') for doc in documents if hasattr(doc, 'metadata')]
        
        # Use selected tables if specified, otherwise all tables
        tables = selected_tables if selected_tables else self.sql_services.get_avaliable_tables()
        
        result = classifier(
            question=question,
            tables=tables,
            documents=doc_titles
        )
        logger.info(f"Classification Finished, Result: {result}")
        state["query_type"] = result['query_type']
        state["metadata"] = {"confidence": result['confidence'], "reasoning": result['reasoning']}
        return state
    
    def route_query(self,state:GraphState)->str:
        """Route to appropriate node based on query type."""
        return state["query_type"]
    
    def retrieve_documents(self,state:GraphState)->GraphState:
        """retrieve relevant documents"""
        try:
            logger.info("Retrieving documents...")
            config = state.get("config", {})
            filter_files = config.get("selected_files", [])
            docs = self.vectorstore_services.similarity_search(state["question"],filter_files=filter_files)
            if docs:
                state["context"]="\n\n".join([doc.page_content for doc in docs])
                state["metadata"]["retrieved_docs"] = len(docs)
                logger.info(f"Retrieved {len(docs)} documents")
            else:
                state["context"] = "No relevant documents found."
                logger.warning("No documents found")
        except Exception as e:
            state["error"] = f"Document retrieval error {str(e)}"
            state["context"]=""
            logger.error(f"Error retrieving documents {e}")
        return state
    
    def query_sql(self, state: GraphState) -> GraphState:
        """Execute SQL query"""
        try:
            logger.info("Generating and executing sql query...")
            config = state.get("config", {})
            selected_tables = config.get("selected_tables", [])
            
            sql_query = self.sql_services.generate_sql(
                state["question"], 
                selected_tables=selected_tables
            )
            
            if sql_query:
                state["sql_query"] = sql_query
                result = self.sql_services.execute_sql_as_dict(sql_query=sql_query)
                state["sql_result"] = result
                state["context"] = f"\nSQL query: {sql_query}\n\nSQL Result: {result}"
                logger.info("SQL query executed successfully.")
            else:
                state["error"] = "Could not generate SQL Query"
                logger.warning("Failed to generate SQL Query")
        except Exception as e:
            state["error"] = f"SQL error {str(e)}"
            logger.error(f"SQL Error {e}")
        return state
    
    def generate_answer(self,state:GraphState)->GraphState:
        """Generate Final Answer"""
        try:
            if state.get("error"):
                state["answer"] = f"I encountered an error: {state['error']}"
                logger.warning(f"Generating error response: {state['error']}")
                return state
            logger.info("Generating answer...")
            question = state["question"]
            documents = self.document_services.load_all_documents()
            config = state.get("config", {})
            context = "\n\n".join([doc.page_content for doc in documents])
            response = self.llm_services.generate_response(
                prompt=question ,
                context=context,
                config=config
            )
            state["answer"] = response
            logger.info("Answer generated successfully.")
        except Exception as e:
            state["answer"] = f"Error generating answer: {str(e)}"
            logger.error(f"Error generating answer: {e}")
        return state

    def invoke(self,question:str,config:dict)->dict:
        """Invoke the graph with a question"""
        initial_state:GraphState={
            "question":question,
            "query_type":"general",
            "context":"",
            "sql_query":"",
            "sql_result":[],
            "answer":"",
            "error":"",
            "config":config,
            "metadata":{}
        }
        result = self.graph.invoke(initial_state) if self.graph else {}
        return result
    
    def build(self):
        """Build langgraph workflow"""
        workflow = StateGraph(GraphState)

        workflow.add_node("classify_query",self.classify_query)
        workflow.add_node("retrieve_documents",self.retrieve_documents)
        workflow.add_node("query_sql",self.query_sql)
        workflow.add_node("generate_answer",self.generate_answer)

        workflow.set_entry_point("classify_query")

        workflow.add_conditional_edges("classify_query",
            self.route_query,
            {
                "document":"retrieve_documents",
                "sql":"query_sql",
                "general":"generate_answer"
            }
            )
        workflow.add_edge("retrieve_documents","generate_answer")
        workflow.add_edge("query_sql","generate_answer")
        workflow.add_edge("generate_answer",END)
        
        self.graph = workflow.compile()
        logger.info("LangGraph workflow built successfully.")


    