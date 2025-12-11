"""SQLite database adapter."""

from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text

from src.core.interfaces import DatabaseAdapter


class SQLiteAdapter(DatabaseAdapter):
    """Adapter for SQLite database operations."""

    def __init__(self, database_url: str):
        """Initialize SQLite adapter.

        Args:
            database_url: SQLite connection string in format:
                sqlite:///path/to/database.db
        """
        self.database_url = database_url
        self.engine: Optional[object] = None

    def connect(self) -> None:
        """Establish SQLite database connection."""
        try:
            print(f"\n🔄 Attempting to connect to SQLite database...")
            
            if not self.database_url.startswith("sqlite:///"):
                raise ValueError("SQLite URL must start with 'sqlite:///'")

            db_path = self.database_url.replace("sqlite:///", "")
            print(f"   Database: {db_path}")

            # Check if database file exists or can be created
            from pathlib import Path
            db_file = Path(db_path)
            if db_file.exists():
                print(f"   ✓ Database file exists")
            else:
                print(f"   ℹ Database file will be created")
                # Check if directory exists and is writable
                db_dir = db_file.parent
                if db_dir and not db_dir.exists():
                    try:
                        db_dir.mkdir(parents=True, exist_ok=True)
                        print(f"   ✓ Created directory: {db_dir}")
                    except Exception as dir_error:
                        print(f"   ❌ Cannot create directory: {dir_error}")
                        raise RuntimeError(f"Cannot create database directory: {str(dir_error)}") from dir_error

            print(f"   🔗 Establishing database connection...")
            self.engine = create_engine(self.database_url)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print(f"✅ Connection Status: SUCCESS")
            print(f"✓ Connected to SQLite database: {db_path}")

        except RuntimeError:
            # Re-raise our custom errors
            raise
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Connection Status: FAILED")
            print(f"✗ Error: {str(e)}")
            
            # Provide specific troubleshooting
            if "no such file" in error_msg or "cannot open" in error_msg:
                print(f"\n💡 File Access Issue Detected:")
                print(f"   - Check if the database file path is correct")
                print(f"   - Verify file permissions")
                print(f"   - Ensure the directory exists and is writable")
            elif "permission denied" in error_msg:
                print(f"\n💡 Permission Issue Detected:")
                print(f"   - Check file/directory permissions")
                print(f"   - Ensure you have read/write access")
            
            raise RuntimeError(f"Failed to connect to SQLite database: {str(e)}") from e

    def disconnect(self) -> None:
        """Close SQLite database connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        Args:
            query: SQL query string

        Returns:
            pandas DataFrame with query results

        Raises:
            RuntimeError: If not connected or query fails
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}") from e

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def list_tables(self) -> list:
        """List all tables in the database.

        Returns:
            List of table names
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            query = text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            with self.engine.connect() as conn:
                result = conn.execute(query)
                return [row[0] for row in result.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Failed to list tables: {str(e)}") from e

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database.

        Args:
            table_name: Name of the table to check

        Returns:
            True if table exists, False otherwise
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            query = text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=:table_name
            """)
            with self.engine.connect() as conn:
                result = conn.execute(query, {"table_name": table_name})
                return result.fetchone() is not None
        except Exception as e:
            raise RuntimeError(f"Failed to check table existence: {str(e)}") from e

    def create_sample_table(self, table_name: str = "dummy_examples") -> None:
        """Create sample table with dummy data.

        Args:
            table_name: Name of the table to create (default: dummy_examples)
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            with self.engine.begin() as conn:
                # Create table
                create_table_sql = text(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT,
                        age INTEGER,
                        city TEXT,
                        salary REAL,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.execute(create_table_sql)

                # Insert sample data
                sample_data = [
                    ("John Doe", "john.doe@example.com", 30, "New York", 75000.00),
                    ("Jane Smith", "jane.smith@example.com", 28, "Los Angeles", 80000.00),
                    ("Bob Johnson", "bob.johnson@example.com", 35, "Chicago", 90000.00),
                    ("Alice Williams", "alice.williams@example.com", 32, "Houston", 85000.00),
                    ("Charlie Brown", "charlie.brown@example.com", 27, "Phoenix", 70000.00),
                ]

                insert_sql = text(f"""
                    INSERT INTO {table_name} (name, email, age, city, salary)
                    VALUES (:name, :email, :age, :city, :salary)
                """)

                for name, email, age, city, salary in sample_data:
                    conn.execute(insert_sql, {
                        "name": name,
                        "email": email,
                        "age": age,
                        "city": city,
                        "salary": salary
                    })

            print(f"✓ Created table '{table_name}' with {len(sample_data)} sample records")

        except Exception as e:
            raise RuntimeError(f"Failed to create sample table: {str(e)}") from e

