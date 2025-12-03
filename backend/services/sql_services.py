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
            
            # Dynamic Database Detection
            db_dir = os.path.dirname(settings.DATABASE_PATH)
            real_db_path = None
            
            if os.path.exists(db_dir):
                # Find any file ending with .db
                db_files = [f for f in os.listdir(db_dir) if f.endswith('.db')]
                
                if db_files:
                    # Prefer 'database.db' if it exists, otherwise take the first one found
                    if "database.db" in db_files:
                        target_db = "database.db"
                    else:
                        target_db = db_files[0]
                    
                    real_db_path = os.path.join(db_dir, target_db)
                    logger.info(f"Detected database file: {real_db_path}")
                else:
                    logger.warning(f"No .db files found in {db_dir}")
            
            if real_db_path and os.path.exists(real_db_path):
                logger.info(f"Connecting to database: {real_db_path}")
                self.db = SQLDatabase.from_uri(f"sqlite:///{real_db_path}")
                self.avaliable_tables = self.db.get_usable_table_names()
                logger.info("Database connected successfully")
                logger.info(f"Available tables: {self.avaliable_tables}")
            else:
                logger.warning("No database file found or connection failed.")
                
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
            # Try to re-initialize if not connected (lazy load attempt)
            self.initialize()
            if self.db is None:
                raise ValueError("Database not initialized. Please upload a .db file.")
        
        sql_gen = self.SQLGenerator(self.db, selected_tables)
        sql_query = sql_gen(question)
        return str(sql_query)
    
    def execute_sql_as_dict(self, sql_query: str) -> list[dict]:
        """Execute SQL and return results as list of dictionaries"""
        if self.db is None:
             raise ValueError("Database not initialized.")
        try:
            with self.db._engine.connect() as conn:
                result = conn.execute(text(sql_query))
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Failed to execute SQL: {e}")
            raise