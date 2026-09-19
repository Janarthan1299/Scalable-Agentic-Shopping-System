"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings(BaseModel):
    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "Scalable Agentic Shopping System"))
    top_k: int = Field(default_factory=lambda: int(os.getenv("TOP_K", "5")), ge=1)
    max_retries: int = Field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "2")), ge=0)
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./shopping_agent.db"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    data_dir: Path = ROOT_DIR / "data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
