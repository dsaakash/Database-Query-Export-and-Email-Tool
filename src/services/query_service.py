"""Service for orchestrating query execution and exports."""

from typing import List, Optional

import pandas as pd

from src.adapters.database.factory import DatabaseAdapterFactory
from src.core.config import Config
from src.core.interfaces import DatabaseAdapter
from src.services.email_service import EmailService
from src.services.export_service import ExcelExportService, PDFExportService


class QueryService:
    """Service for executing queries and managing exports."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize query service.

        Args:
            config: Configuration instance (creates new if not provided)
        """
        self.config = config or Config()
        self.excel_service = ExcelExportService()
        self.pdf_service = PDFExportService()

    def execute_and_export(
        self,
        database_type: str,
        database_url: str,
        query: str,
        export_excel: bool = True,
        export_pdf: bool = False,
        excel_path: str = "report.xlsx",
        pdf_path: Optional[str] = None,
        send_email: bool = False,
        email_recipients: Optional[List[str]] = None,
        email_subject: str = "Database Report",
        email_cc_recipients: Optional[List[str]] = None,
        email_config: Optional[dict] = None,
    ) -> dict:
        """Execute query and export results.

        Args:
            database_type: Type of database (postgresql)
            database_url: Database connection URL
            query: SQL query to execute
            export_excel: Whether to export to Excel
            export_pdf: Whether to export to PDF
            excel_path: Excel output file path
            pdf_path: PDF output file path
            send_email: Whether to send email
            email_recipients: List of email recipients (TO)
            email_subject: Email subject
            email_cc_recipients: Optional list of CC email recipients
            email_config: Optional email configuration dict (smtp_user, smtp_password, smtp_host, smtp_port)

        Returns:
            Dictionary with execution results and file paths

        Raises:
            RuntimeError: If query execution or export fails
        """
        # Create database adapter
        db_adapter = DatabaseAdapterFactory.create(database_type, database_url)

        # Execute query
        with db_adapter:
            print(f"✓ Executing query...")
            df = db_adapter.execute_query(query)

            if df.empty:
                print("⚠ Warning: Query returned no results")
                return {"success": False, "message": "Query returned no results"}

            print(f"✓ Query returned {len(df)} rows")

        # Export to Excel
        excel_file = None
        if export_excel:
            excel_file = self.excel_service.export(df, excel_path)

        # Export to PDF
        pdf_file = None
        if export_pdf:
            pdf_file = self.pdf_service.export(df, pdf_path or "report.pdf")

        # Send email if requested
        if send_email:
            if not email_recipients:
                raise ValueError("Email recipients are required when sending email")

            # Use provided email_config or fall back to .env
            if not email_config:
                email_config = self.config.get_email_config()
            
            email_service = EmailService(**email_config)
            email_service.send_email(
                df=df,
                recipients=email_recipients,
                subject=email_subject,
                excel_file=excel_file or excel_path,
                pdf_file=pdf_file,
                cc_recipients=email_cc_recipients if email_cc_recipients else [],
            )

        result = {
            "success": True,
            "rows": len(df),
            "excel_file": excel_file,
            "pdf_file": pdf_file,
        }

        print("\n✓ Process completed successfully!")
        return result

