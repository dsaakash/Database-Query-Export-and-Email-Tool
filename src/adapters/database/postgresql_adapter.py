"""PostgreSQL database adapter."""

from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text

from src.core.interfaces import DatabaseAdapter


class PostgreSQLAdapter(DatabaseAdapter):
    """Adapter for PostgreSQL database operations."""

    def __init__(self, database_url: str):
        """Initialize PostgreSQL adapter.

        Args:
            database_url: PostgreSQL connection string (standard PostgreSQL URL format)
        """
        self.database_url = database_url
        self.engine: Optional[object] = None

    def connect(self) -> None:
        """Establish PostgreSQL database connection."""
        try:
            print(f"\n🔄 Attempting to connect to PostgreSQL database...")
            
            # Validate URL format
            if not (self.database_url.startswith("postgresql://") or 
                    self.database_url.startswith("postgres://")):
                raise ValueError("PostgreSQL URL must start with 'postgresql://' or 'postgres://'")

            # Extract database name and host for display
            db_name = self.database_url.split("/")[-1].split("?")[0] if "/" in self.database_url else "unknown"
            # Extract host from URL
            try:
                from urllib.parse import urlparse
                parsed = urlparse(self.database_url)
                host = parsed.hostname or "unknown"
                port = parsed.port or 5432
                print(f"   Host: {host}:{port}")
                print(f"   Database: {db_name}")
            except Exception:
                print(f"   Database: {db_name}")

            # Check network connectivity first (basic check)
            import socket
            try:
                if host and host != "unknown":
                    print(f"   🔍 Checking network connectivity...")
                    socket.gethostbyname(host)
                    print(f"   ✓ Hostname resolved successfully")
            except socket.gaierror as dns_error:
                print(f"   ❌ DNS Resolution Failed")
                print(f"\n❌ Connection Status: FAILED")
                print(f"✗ Error: Cannot resolve hostname '{host}'")
                print(f"\n💡 Troubleshooting:")
                print(f"   1. Check your internet connection")
                print(f"   2. Verify the hostname is correct: {host}")
                print(f"   3. Check if the database server is accessible")
                print(f"   4. For cloud databases (Neon, Supabase, etc.), verify:")
                print(f"      - The database URL is correct")
                print(f"      - Your IP is whitelisted (if required)")
                print(f"      - The database instance is running")
                raise RuntimeError(f"DNS resolution failed for host '{host}': {str(dns_error)}") from dns_error
            except Exception as net_error:
                # Network check failed but continue with connection attempt
                print(f"   ⚠ Network check inconclusive, continuing...")

            self.engine = create_engine(self.database_url)
            
            # Test connection
            print(f"   🔗 Establishing database connection...")
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print(f"✅ Connection Status: SUCCESS")
            print(f"✓ Connected to PostgreSQL database")

        except RuntimeError:
            # Re-raise our custom errors
            raise
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Connection Status: FAILED")
            print(f"✗ Error: {str(e)}")
            
            # Provide specific troubleshooting based on error type
            if "could not translate host name" in error_msg or "nodename nor servname" in error_msg:
                print(f"\n💡 DNS Resolution Issue Detected:")
                print(f"   - The hostname cannot be resolved")
                print(f"   - Check your internet connection")
                print(f"   - Verify the database URL is correct")
                print(f"   - For cloud databases, ensure the hostname is accessible")
            elif "connection refused" in error_msg or "connection timed out" in error_msg:
                print(f"\n💡 Connection Issue Detected:")
                print(f"   - The database server is not responding")
                print(f"   - Check if the database is running")
                print(f"   - Verify the port number is correct")
                print(f"   - Check firewall settings")
            elif "authentication failed" in error_msg or "password" in error_msg:
                print(f"\n💡 Authentication Issue Detected:")
                print(f"   - Check username and password")
                print(f"   - Verify credentials in database URL")
            elif "database" in error_msg and "does not exist" in error_msg:
                print(f"\n💡 Database Issue Detected:")
                print(f"   - The specified database does not exist")
                print(f"   - Verify the database name in the URL")
            
            raise RuntimeError(f"Failed to connect to PostgreSQL database: {str(e)}") from e

    def disconnect(self) -> None:
        """Close PostgreSQL database connection."""
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
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
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
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = :table_name
                )
            """)
            with self.engine.connect() as conn:
                result = conn.execute(query, {"table_name": table_name.lower()})
                return result.scalar()
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
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100),
                        age INTEGER,
                        city VARCHAR(50),
                        salary DECIMAL(10, 2),
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

