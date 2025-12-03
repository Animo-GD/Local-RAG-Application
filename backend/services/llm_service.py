from langchain_ollama import OllamaLLM
from utils.logger import logger
from langchain_core.prompts import PromptTemplate
from config import settings
import dspy

class LLMServices:
    """Services for llm operations"""
    def __init__(self) -> None:
        self.llm = None

    def intialize(self):
        """Initialize default Local LLM"""
        self._set_llm(settings.LLM_MODEL)
        try:
            dspy_lm = dspy.LM(
                model=f"ollama/{settings.LLM_MODEL}",
                api_base=settings.OLLAMA_BASE_URL,
                max_tokens=512
            )
            dspy.configure(lm=dspy_lm)
            logger.info("DSPy configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure DSPy: {e}")


    def _set_llm(self, model_name: str):
        """Helper to initialize/update LLM instance"""
        try:
            logger.info(f"Initializing Local LLM: {model_name}")
            self.llm = OllamaLLM(
                model=model_name, 
                temperature=settings.LLM_TEMPERATURE,
                base_url=settings.OLLAMA_BASE_URL
            )
            self.current_model = model_name
            logger.info("Local LLM Initialized Successfully.")
        except Exception as e:
            logger.error(f"Failed To Initialize LLM {e}")
    def generate_response(self,prompt:str,context:str="",config: dict = {"model":"llama3.1:8b"})->str:
        """Generate a response from the LLM"""
        try:
            requested_model = config.get('model', settings.LLM_MODEL)
            if requested_model != self.current_model:
                self._set_llm(requested_model)
            template = PromptTemplate.from_template(
                """
                # System
                Answer the user query from the context below with out adding any explaination, make it a direct answer.
                If you can't answer from the context, Answer the question by your knowledge.

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
            