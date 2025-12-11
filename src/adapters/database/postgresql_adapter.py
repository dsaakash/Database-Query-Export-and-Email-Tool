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

    def create_users_table(self, table_name: str = "users") -> None:
        """Create users table with dummy data.

        Args:
            table_name: Name of the table to create (default: users)
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            # Check if table already exists
            if self.table_exists(table_name):
                print(f"⚠ Table '{table_name}' already exists. Skipping creation.")
                return

            with self.engine.begin() as conn:
                # Create users table
                create_table_sql = text(f"""
                    CREATE TABLE {table_name} (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        age INTEGER,
                        phone VARCHAR(20),
                        address VARCHAR(200),
                        city VARCHAR(50),
                        country VARCHAR(50) DEFAULT 'USA',
                        is_active BOOLEAN DEFAULT TRUE,
                        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                """)
                conn.execute(create_table_sql)

                # Insert sample user data
                users_data = [
                    ("johndoe", "john.doe@example.com", "John", "Doe", 30, "+1-555-0101", "123 Main St", "New York", "USA", True),
                    ("janesmith", "jane.smith@example.com", "Jane", "Smith", 28, "+1-555-0102", "456 Oak Ave", "Los Angeles", "USA", True),
                    ("bobjohnson", "bob.johnson@example.com", "Bob", "Johnson", 35, "+1-555-0103", "789 Pine Rd", "Chicago", "USA", True),
                    ("alicewilliams", "alice.williams@example.com", "Alice", "Williams", 32, "+1-555-0104", "321 Elm St", "Houston", "USA", True),
                    ("charliebrown", "charlie.brown@example.com", "Charlie", "Brown", 27, "+1-555-0105", "654 Maple Dr", "Phoenix", "USA", True),
                    ("dianawilson", "diana.wilson@example.com", "Diana", "Wilson", 29, "+1-555-0106", "987 Cedar Ln", "Philadelphia", "USA", True),
                    ("edwarddavis", "edward.davis@example.com", "Edward", "Davis", 41, "+1-555-0107", "147 Birch Way", "San Antonio", "USA", True),
                    ("frankmiller", "frank.miller@example.com", "Frank", "Miller", 33, "+1-555-0108", "258 Spruce Ct", "San Diego", "USA", False),
                    ("gracelee", "grace.lee@example.com", "Grace", "Lee", 26, "+1-555-0109", "369 Willow Pl", "Dallas", "USA", True),
                    ("henrygarcia", "henry.garcia@example.com", "Henry", "Garcia", 38, "+1-555-0110", "741 Ash Blvd", "San Jose", "USA", True),
                ]

                insert_sql = text(f"""
                    INSERT INTO {table_name} (username, email, first_name, last_name, age, phone, address, city, country, is_active)
                    VALUES (:username, :email, :first_name, :last_name, :age, :phone, :address, :city, :country, :is_active)
                """)

                for user_data in users_data:
                    conn.execute(insert_sql, {
                        "username": user_data[0],
                        "email": user_data[1],
                        "first_name": user_data[2],
                        "last_name": user_data[3],
                        "age": user_data[4],
                        "phone": user_data[5],
                        "address": user_data[6],
                        "city": user_data[7],
                        "country": user_data[8],
                        "is_active": user_data[9]
                    })

            print(f"✓ Created table '{table_name}' with {len(users_data)} user records")

        except Exception as e:
            raise RuntimeError(f"Failed to create users table: {str(e)}") from e

    def execute_ddl_query(self, ddl_query: str) -> None:
        """Execute DDL (Data Definition Language) queries like CREATE TABLE, ALTER TABLE.

        Args:
            ddl_query: DDL SQL query string (CREATE TABLE, ALTER TABLE, etc.)

        Raises:
            RuntimeError: If not connected or DDL query fails
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        # Validate that it's a DDL query (basic check)
        ddl_query_upper = ddl_query.strip().upper()
        valid_ddl_keywords = ["CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME"]
        
        if not any(ddl_query_upper.startswith(keyword) for keyword in valid_ddl_keywords):
            raise ValueError(
                f"Invalid DDL query. Must start with one of: {', '.join(valid_ddl_keywords)}"
            )

        try:
            with self.engine.begin() as conn:
                conn.execute(text(ddl_query))
            print(f"✓ DDL query executed successfully")
        except Exception as e:
            raise RuntimeError(f"DDL query execution failed: {str(e)}") from e

    def add_column(self, table_name: str, column_name: str, column_definition: str) -> None:
        """Add a column to an existing table.

        Args:
            table_name: Name of the table
            column_name: Name of the column to add
            column_definition: Column definition (e.g., 'VARCHAR(100)', 'INTEGER', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')

        Raises:
            RuntimeError: If table doesn't exist or column addition fails
        """
        if not self.engine:
            raise RuntimeError("Database not connected. Call connect() first.")

        # Check if table exists
        if not self.table_exists(table_name):
            raise RuntimeError(f"Table '{table_name}' does not exist.")

        try:
            ddl_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
            self.execute_ddl_query(ddl_query)
            print(f"✓ Added column '{column_name}' to table '{table_name}'")
        except Exception as e:
            raise RuntimeError(f"Failed to add column: {str(e)}") from e

