from pydantic_settings import BaseSettings
from typing import List,Union
import secrets

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

    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cookie_domain: str = "localhost"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"

    class Config:
        env_file = ".env"

settings = Settings()