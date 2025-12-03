import os
import dspy
from langchain_community.utilities import SQLDatabase
from sqlalchemy import text, inspect
from utils.logger import logger
from config import settings

class SQLService:
    def __init__(self) -> None:
        self.db = None
        self.lm = None
        self.avaliable_tables = []

    def initialize(self):
        """Initialize Database"""
        try:
            # Initialize DSPy LM
            self.lm = dspy.LM(
                model=f"ollama/{settings.LLM_MODEL}",
                api_base=settings.OLLAMA_BASE_URL,
                max_tokens=512
            )
            dspy.configure(lm=self.lm)
            
            if os.path.exists(settings.DATABASE_PATH):
                logger.info(f"Connecting to database: {settings.DATABASE_PATH}")
                self.db = SQLDatabase.from_uri(f"sqlite:///{settings.DATABASE_PATH}")
                self.avaliable_tables = self.db.get_usable_table_names()
                logger.info("Database connected successfully")
                logger.info(f"Available tables: {self.avaliable_tables}")
            else:
                logger.warning("No database file found.")
        except Exception as e:
            logger.error(f"Failed to initialize database {e}")
    
    def get_avaliable_tables(self):
        return self.avaliable_tables if self.db else []
    
    def get_table_schema(self, table_name: str) -> dict:
        """Get schema information for a specific table"""
        try:
            if not self.db:
                return {}
            
            inspector = inspect(self.db._engine)
            columns = inspector.get_columns(table_name)
            
            return {
                "columns": [
                    {
                        "name": col["name"],
                        "type": str(col["type"])
                    }
                    for col in columns
                ]
            }
        except Exception as e:
            logger.error(f"Error getting schema for table {table_name}: {e}")
            return {}
    
    class Text2SQL(dspy.Signature):
        """Converting natural language questions to SQL queries."""
        schema_db = dspy.InputField(desc="Database Schema Information.")
        question = dspy.InputField(desc="Natural Language question.")
        sql_query = dspy.OutputField(desc="SQL Query only, no explanation")

    class SQLGenerator(dspy.Module):
        def __init__(self, db, selected_tables=None):
            super().__init__()
            self.db = db
            self.selected_tables = selected_tables
            self.generate_sql = dspy.ChainOfThought(SQLService.Text2SQL)
        
        def forward(self, question):
            """Generate SQL from natural language question"""
            # Get schema - filter by selected tables if specified
            if self.selected_tables:
                schema_parts = []
                for table in self.selected_tables:
                    try:
                        table_info = self.db.get_table_info_no_throw([table])
                        if table_info:
                            schema_parts.append(table_info)
                    except:
                        pass
                schema = "\n\n".join(schema_parts) if schema_parts else self.db.get_table_info()
            else:
                schema = self.db.get_table_info()
            
            prediction = self.generate_sql(schema_db=schema, question=question)
            return prediction.sql_query
    
    def generate_sql(self, question: str, selected_tables: list = []) -> str:
        """Generate SQL query from natural language question"""
        if self.db is None:
            raise ValueError("Database not initialized. Call initialize() first.")
        
        sql_gen = self.SQLGenerator(self.db, selected_tables)
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
        except Exception as e:
            logger.error(f"Failed to execute SQL: {e}")
            raise