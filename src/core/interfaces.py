"""Core interfaces following Dependency Inversion Principle."""

from abc import ABC, abstractmethod
from typing import Protocol

import pandas as pd


class DatabaseAdapter(ABC):
    """Abstract interface for database adapters."""

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        Args:
            query: SQL query string

        Returns:
            pandas DataFrame with query results
        """
        pass

    @abstractmethod
    def __enter__(self):
        """Context manager entry."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass


class ExportService(Protocol):
    """Protocol for export services."""

    def export(self, df: pd.DataFrame, output_path: str) -> str:
        """Export DataFrame to file.

        Args:
            df: pandas DataFrame to export
            output_path: Output file path

        Returns:
            Path to created file
        """
        ...

