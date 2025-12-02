from langchain_ollama import OllamaLLM
from utils.logger import logger
from langchain_core.prompts import PromptTemplate
from config import settings


class LLMServices:
    """Services for llm operations"""
    def __init__(self) -> None:
        self.llm = None

    def intialize(self):
        """Call the LLM"""
        try:
            logger.info(f"Initlizing LLM: {settings.LLM_MODEL}")
            self.llm = OllamaLLM(model=settings.LLM_MODEL,temperature=settings.LLM_TEMPERATURE)
            logger.info("LLM Initilized Successfully.")
        except Exception as e:
            logger.error(f"Failed To Initilize LLM {e}")
            raise

    def generate_response(self,prompt:str,context:str="")->str:
        """Generate a response from the LLM"""
        try:
            template = PromptTemplate.from_template(
                """
                # System
                Answer the user query from the context below with out adding any explaination, make it a direct answer.
                If you can't answer from the context, Say You don't have information to answer this query.

                ## Context:
                {context}
                ## Question:
                {question}
                ## Answer:
                ...
                """
            )
            formatted_prompt = template.format(
                context = context if context else "There is no available context",
                question=prompt
            )
            response = self.llm.invoke(formatted_prompt) if self.llm else ""
            return response
        except Exception as e:
            logger.error(f"Error Generating Response {e}")
            return f"Error generate reponse: {str(e)}"
        
    def get_llm(self):
        """Get the LLM instance"""
        return self.llm