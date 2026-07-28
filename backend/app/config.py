import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central app configuration. All values are read from environment
    variables (or a .env file) so no secrets live in code.
    """
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_EXTRACTION_MODEL: str = "gemma2-9b-it"
    GROQ_REASONING_MODEL: str = "llama-3.3-70b-versatile"

    # Falls back to a local SQLite file if no DATABASE_URL is set, so the
    # project runs out of the box without a MySQL/Postgres server. Point
    # DATABASE_URL at MySQL/Postgres for the real assignment stack, e.g.
    # "mysql+pymysql://user:password@localhost:3306/aivoa_complaints"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./complaints.db")

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
