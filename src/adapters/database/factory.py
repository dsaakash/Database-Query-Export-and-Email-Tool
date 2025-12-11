"""Database adapter factory following Factory pattern."""

from src.adapters.database import PostgreSQLAdapter
from src.core.interfaces import DatabaseAdapter


class DatabaseAdapterFactory:
    """Factory for creating database adapters."""

    @staticmethod
    def create(database_type: str, database_url: str) -> DatabaseAdapter:
        """Create PostgreSQL database adapter.

        Args:
            database_type: Type of database (must be 'postgresql' or 'postgres')
            database_url: PostgreSQL database connection URL

        Returns:
            PostgreSQLAdapter instance

        Raises:
            ValueError: If database type is not PostgreSQL
        """
        database_type = database_type.lower()

        if database_type in ["postgresql", "postgres"]:
            return PostgreSQLAdapter(database_url)
        else:
            raise ValueError(
                f"Unsupported database type: {database_type}. "
                "This application only supports PostgreSQL."
            )

