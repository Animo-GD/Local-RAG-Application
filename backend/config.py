from pydantic_settings import BaseSettings
from typing import List
class Settings(BaseSettings):
    API_HOST:str = "0.0.0.0"
    API_PORT:int = 5000


    CORS_ORIGINS:List[str] = ["http://localhost:5173"]

    class Config:
        env_file=".env"