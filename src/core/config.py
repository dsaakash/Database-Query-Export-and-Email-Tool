"""Configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Application configuration manager."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration.

        Args:
            env_file: Path to .env file (default: .env in project root)
        """
        if env_file is None:
            env_file = Path(__file__).parent.parent.parent / ".env"

        load_dotenv(env_file)
        self.env_file = env_file

    def get_email_config(self) -> dict:
        """Get email configuration from environment.

        Returns:
            Dictionary with email configuration

        Raises:
            ValueError: If required configuration is missing
        """
        smtp_user = os.getenv("SMTP_USER") or os.getenv("EMAIL_USER")
        smtp_password = os.getenv("SMTP_PASSWORD") or os.getenv("EMAIL_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))

        if not all([smtp_user, smtp_password]):
            raise ValueError(
                "Missing email configuration. Please set in .env file:\n"
                "SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT"
            )

        return {
            "smtp_user": smtp_user,
            "smtp_password": smtp_password,
            "smtp_host": smtp_host,
            "smtp_port": smtp_port,
        }

    def get_database_url(self, database_type: str = "postgresql") -> Optional[str]:
        """Get PostgreSQL database URL from environment.

        Args:
            database_type: Type of database (default: 'postgresql')

        Returns:
            Database URL if found in .env, None otherwise
        """
        # Try PostgreSQL-specific key first
        database_url = os.getenv("POSTGRESQL_DATABASE_URL") or os.getenv("POSTGRES_DATABASE_URL")
        
        if database_url:
            return database_url
        
        # Try generic DATABASE_URL (must be PostgreSQL format)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Check if URL is PostgreSQL format
            if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
                return database_url
        
        return None

    def has_database_url(self, database_type: str = "postgresql") -> bool:
        """Check if PostgreSQL database URL exists in .env.

        Args:
            database_type: Type of database (default: 'postgresql')

        Returns:
            True if database URL exists in .env, False otherwise
        """
        return self.get_database_url(database_type) is not None

