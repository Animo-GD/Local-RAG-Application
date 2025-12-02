import os
import dspy
from langchain_community.utilities import SQLDatabase
from sqlalchemy import text
from utils.logger import logger
from config import settings
class SQLService:
    def __init__(self) -> None:
        self.db = None
        self.lm = dspy.LM(
            model=f"ollama/{settings.LLM_MODEL}",
            api_base="http://localhost:11434",  
            max_tokens=512
        )
        dspy.configure(lm=self.lm)
        self.avaliable_tables = []

    def initialize(self):
        """Initialize Database"""
        try:
            if os.path.exists(settings.DATABASE_PATH):
                logger.info(f"Connecting to database: {settings.DATABASE_PATH}")
                self.db = SQLDatabase.from_uri(f"sqlite:///{settings.DATABASE_PATH}")
                logger.info("Database connected successfully")
                logger.info(f"Available tables: {self.db.get_usable_table_names()}")
            else:
                logger.warning("No database file found.")
        except Exception as e:
            logger.error(f"Failed to initialize database {e}")
    def get_avaliable_tables(self):
        return self.db.get_usable_table_names() if self.db else []
    class Text2SQL(dspy.Signature):
        """Converting natural language questions to SQL queries."""
        schema_db = dspy.InputField(desc="Database Schema Information.")
        question = dspy.InputField(desc="Natural Language question.")
        sql_query = dspy.OutputField(desc="SQL Query only, no explanation")

    class SQLGenerator(dspy.Module):
        def __init__(self, db):
            super().__init__()
            self.db = db
            self.generate_sql = dspy.ChainOfThought(SQLService.Text2SQL)
        
        def forward(self, question):
            """Generate SQL from natural language question"""
            schema = self.db.get_table_info()
            prediction = self.generate_sql(schema_db=schema, question=question)
            return prediction.sql_query
    
    def generate_sql(self, question: str) -> str:
        """Generate SQL query from natural language question"""
        if self.db is None:
            raise ValueError("Database not initialized. Call initialize() first.")
        
        sql_gen = self.SQLGenerator(self.db)
        sql_query = sql_gen(question)
        return str(sql_query)
    
    def execute_sql_as_dict(self, sql_query: str) -> list[dict]:
        """Execute SQL and return results as list of dictionaries"""
        if self.db is None:
            raise ValueError("Database not initialized. Call initialize() first.")
        try:
            with self.db._engine.connect() as conn:
                result = conn.execute(text(sql_query))
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Failed to execute SQL: {e}")
            raise

