from pydantic_settings import BaseSettings
from typing import List,Union

class Settings(BaseSettings):
    app_name: str = "Personal Finance Tracker"
    debug: bool = False
    database_url: str = "sqlite:///personalfinance.db"
    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"

    class Config:
        env_file = ".env"

settings = Settings()