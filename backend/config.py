"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os

# Add parent path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str

    # AI Configuration
    gemini_api_key: str
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-2.0-flash"

    # Groq AI Configuration (FREE)
    groq_api_key: str = ""
    groq_model: str = "llama-3.2-90b-text-preview"

    # Ollama AI Configuration (100% FREE LOCAL)
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_tickets: str = "fte.tickets.incoming"
    kafka_topic_metrics: str = "fte.metrics"

    # Email Configuration
    gmail_email: str = ""
    gmail_app_password: str = ""

    # Application
    app_env: str = "development"
    debug: bool = True
    cors_origins: str = "http://localhost:3000,http://localhost:8000,http://localhost:5173,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:5173"  # Added common frontend ports

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


def get_cors_origins() -> List[str]:
    """Parse CORS origins from comma-separated string"""
    return [origin.strip() for origin in settings.cors_origins.split(",")]
