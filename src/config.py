"""
Configuration centralisée pour VIGIL
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuration globale de l'application"""

    # Base
    APP_NAME: str = "VIGIL"
    APP_VERSION: str = "1.0.0-POC"
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/vigil_db",
        description="URL de connexion PostgreSQL"
    )

    # API Keys - Competitor Identification
    CRUNCHBASE_API_KEY: Optional[str] = Field(default=None)
    LINKEDIN_API_KEY: Optional[str] = Field(default=None)

    # API Keys - Financial Data
    PAPPERS_API_KEY: Optional[str] = Field(default=None)
    FINANCIAL_MODELING_PREP_API_KEY: Optional[str] = Field(default=None)
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None)

    # API Keys - Marketing & SEO
    SIMILARWEB_API_KEY: Optional[str] = Field(default=None)
    SEMRUSH_API_KEY: Optional[str] = Field(default=None)
    AHREFS_API_KEY: Optional[str] = Field(default=None)

    # Scraping Configuration
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    SCRAPING_DELAY: float = Field(default=2.0, description="Délai entre requêtes (secondes)")
    MAX_RETRIES: int = Field(default=3)

    # Cache Configuration
    CACHE_TTL_DAYS: int = Field(default=90, description="Durée de validité du cache")
    ENABLE_CACHE: bool = Field(default=True)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="vigil.log")

    # Zero Hallucination - Confidence Thresholds
    MIN_CONFIDENCE_THRESHOLD: float = Field(default=0.70, ge=0.0, le=1.0)
    MIN_DATA_SOURCES: int = Field(default=2, ge=1)

    # Rate Limiting
    API_RATE_LIMIT_PER_MINUTE: int = Field(default=30)
    SCRAPING_RATE_LIMIT_PER_MINUTE: int = Field(default=10)

    # Module 1 - Identification
    MAX_COMPETITORS_TO_IDENTIFY: int = Field(default=10, description="Nombre max de concurrents")
    MIN_SIMILARITY_SCORE: float = Field(default=0.60, description="Score minimum de pertinence")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instance globale des settings
settings = Settings()


def get_settings() -> Settings:
    """Retourne l'instance des settings"""
    return settings
