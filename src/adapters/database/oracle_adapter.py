"""Oracle database adapter."""

from typing import Optional

import oracledb
import pandas as pd

from src.core.interfaces import DatabaseAdapter


class OracleAdapter(DatabaseAdapter):
    """Adapter for Oracle database operations."""

    def __init__(self, database_url: str):
        """Initialize Oracle adapter.

        Args:
            database_url: Oracle connection string in format:
                oracle://username:password@host:port/service_name
        """
        self.database_url = database_url
        self.connection: Optional[oracledb.Connection] = None
        self._parse_url()

    def _parse_url(self) -> None:
        """Parse database URL into connection components."""
        if not self.database_url.startswith("oracle://"):
            raise ValueError("Oracle URL must start with 'oracle://'")

        url_part = self.database_url.replace("oracle://", "")
        if "@" not in url_part:
            raise ValueError("Invalid Oracle URL format")

        auth_part, host_part = url_part.split("@", 1)
        if ":" not in auth_part:
            raise ValueError("Oracle URL must include username:password")

        self.username, self.password = auth_part.split(":", 1)

        if ":" in host_part:
            host_port, service_name = host_part.rsplit("/", 1)
            if ":" in host_port:
                host, port = host_port.split(":", 1)
                self.port = int(port)
            else:
                host = host_port
                self.port = 1521
            self.host = host
            self.service_name = service_name
        else:
            raise ValueError("Oracle URL must include host/service_name")

    def connect(self) -> None:
        """Establish Oracle database connection."""
        try:
            print(f"\n🔄 Attempting to connect to Oracle database...")
            print(f"   Host: {self.host}:{self.port}")
            print(f"   Service: {self.service_name}")
            
            # Check network connectivity first
            import socket
            try:
                print(f"   🔍 Checking network connectivity...")
                socket.gethostbyname(self.host)
                print(f"   ✓ Hostname resolved successfully")
            except socket.gaierror as dns_error:
                print(f"   ❌ DNS Resolution Failed")
                print(f"\n❌ Connection Status: FAILED")
                print(f"✗ Error: Cannot resolve hostname '{self.host}'")
                print(f"\n💡 Troubleshooting:")
                print(f"   1. Check your internet connection")
                print(f"   2. Verify the hostname is correct: {self.host}")
                print(f"   3. Check if the database server is accessible")
                raise RuntimeError(f"DNS resolution failed for host '{self.host}': {str(dns_error)}") from dns_error
            except Exception as net_error:
                print(f"   ⚠ Network check inconclusive, continuing...")
            
            print(f"   🔗 Establishing database connection...")
            dsn = oracledb.makedsn(
                host=self.host,
                port=self.port,
                service_name=self.service_name
            )

            self.connection = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )

            print(f"✅ Connection Status: SUCCESS")
            print(f"✓ Connected to Oracle database: {self.host}:{self.port}/{self.service_name}")

        except RuntimeError:
            # Re-raise our custom errors
            raise
        except oracledb.Error as e:
            error_msg = str(e).lower()
            print(f"❌ Connection Status: FAILED")
            print(f"✗ Error: {str(e)}")
            
            # Provide specific troubleshooting
            if "connection refused" in error_msg or "timeout" in error_msg:
                print(f"\n💡 Connection Issue Detected:")
                print(f"   - The database server is not responding")
                print(f"   - Check if the database is running")
                print(f"   - Verify the port number is correct: {self.port}")
                print(f"   - Check firewall settings")
            elif "authentication" in error_msg or "invalid" in error_msg:
                print(f"\n💡 Authentication Issue Detected:")
                print(f"   - Check username and password")
                print(f"   - Verify credentials in database URL")
            
            raise RuntimeError(f"Failed to connect to Oracle database: {str(e)}") from e

    def disconnect(self) -> None:
        """Close Oracle database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        Args:
            query: SQL query string

        Returns:
            pandas DataFrame with query results

        Raises:
            RuntimeError: If not connected or query fails
        """
        if not self.connection:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            df = pd.read_sql(query, self.connection)
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
        if not self.connection:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            query = "SELECT table_name FROM user_tables ORDER BY table_name"
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except Exception as e:
            raise RuntimeError(f"Failed to list tables: {str(e)}") from e

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database.

        Args:
            table_name: Name of the table to check

        Returns:
            True if table exists, False otherwise
        """
        if not self.connection:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            query = """
                SELECT COUNT(*) 
                FROM user_tables 
                WHERE UPPER(table_name) = UPPER(:table_name)
            """
            cursor = self.connection.cursor()
            cursor.execute(query, {"table_name": table_name})
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except Exception as e:
            raise RuntimeError(f"Failed to check table existence: {str(e)}") from e

    def create_sample_table(self, table_name: str = "DUMMY_EXAMPLES") -> None:
        """Create sample table with dummy data.

        Args:
            table_name: Name of the table to create (default: DUMMY_EXAMPLES)
        """
        if not self.connection:
            raise RuntimeError("Database not connected. Call connect() first.")

        try:
            cursor = self.connection.cursor()

            # Create table
            create_table_sql = f"""
                CREATE TABLE {table_name} (
                    ID NUMBER PRIMARY KEY,
                    NAME VARCHAR2(100) NOT NULL,
                    EMAIL VARCHAR2(100),
                    AGE NUMBER,
                    CITY VARCHAR2(50),
                    SALARY NUMBER(10, 2),
                    CREATED_DATE DATE DEFAULT SYSDATE
                )
            """
            cursor.execute(create_table_sql)

            # Create sequence
            sequence_name = f"{table_name}_SEQ"
            try:
                cursor.execute(f"DROP SEQUENCE {sequence_name}")
            except Exception:
                pass  # Sequence doesn't exist
            cursor.execute(f"""
                CREATE SEQUENCE {sequence_name}
                START WITH 1
                INCREMENT BY 1
                NOCACHE
            """)

            # Insert sample data
            sample_data = [
                ("John Doe", "john.doe@example.com", 30, "New York", 75000.00),
                ("Jane Smith", "jane.smith@example.com", 28, "Los Angeles", 80000.00),
                ("Bob Johnson", "bob.johnson@example.com", 35, "Chicago", 90000.00),
                ("Alice Williams", "alice.williams@example.com", 32, "Houston", 85000.00),
                ("Charlie Brown", "charlie.brown@example.com", 27, "Phoenix", 70000.00),
            ]

            insert_sql = f"""
                INSERT INTO {table_name} (ID, NAME, EMAIL, AGE, CITY, SALARY)
                VALUES ({sequence_name}.NEXTVAL, :name, :email, :age, :city, :salary)
            """

            for name, email, age, city, salary in sample_data:
                cursor.execute(insert_sql, {
                    "name": name,
                    "email": email,
                    "age": age,
                    "city": city,
                    "salary": salary
                })

            self.connection.commit()
            cursor.close()
            print(f"✓ Created table '{table_name}' with {len(sample_data)} sample records")

        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to create sample table: {str(e)}") from e

