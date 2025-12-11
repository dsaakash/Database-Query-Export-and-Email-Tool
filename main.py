#!/usr/bin/env python3
"""
PostgreSQL Query, Export, and Email Tool

An interactive Python application for connecting to PostgreSQL databases,
querying tables, exporting to Excel/PDF, and sending email reports.
"""

import sys
from pathlib import Path

from src.core.config import Config
from src.core.prompts import PromptService
from src.services.query_service import QueryService


def main():
    """Main application entry point with interactive prompts."""
    try:
        # Load configuration
        config = Config()

        # Initialize services
        prompt_service = PromptService()
        query_service = QueryService(config)

        print("\n" + "="*60)
        print("PostgreSQL Query, Export, and Email Tool")
        print("="*60)

        # Database type is PostgreSQL only
        database_type = "postgresql"

        # Step 2: Get database URL (check .env first, then prompt)
        database_url = prompt_service.prompt_database_url(database_type, config)

        # Step 2.5: Test connection and check for tables
        from src.adapters.database.factory import DatabaseAdapterFactory
        
        print("\n" + "="*60)
        print("Testing Database Connection...")
        print("="*60)
        
        available_tables_list = []
        
        try:
            db_adapter = DatabaseAdapterFactory.create(database_type, database_url)
            db_adapter.connect()
            
            # List all tables in database
            print("\n📋 Checking for tables in database...")
            try:
                available_tables = db_adapter.list_tables()
        
                if available_tables:
                    print(f"✅ Found {len(available_tables)} table(s) in database:")
                    for i, table in enumerate(available_tables, 1):
                        print(f"   {i}. {table}")
                    print("\n✓ Database is ready. You can query any of these tables.")
                    available_tables_list = available_tables
                else:
                    print("⚠ No tables found in database.")
                    table_name = "dummy_examples"
                    create_table = prompt_service.prompt_create_sample_table(table_name)
                    
                    if create_table:
                        try:
                            db_adapter.create_sample_table(table_name)
                            print(f"✅ Sample table '{table_name}' created successfully!")
                            available_tables_list = [table_name]
                        except Exception as e:
                            print(f"✗ Failed to create sample table: {e}")
                            print("You can continue with your own queries.")
                    else:
                        print("Skipping table creation. You can use your own queries.")
            except Exception as e:
                print(f"⚠ Could not list tables: {e}")
                print("You can still continue with your queries.")
            
            db_adapter.disconnect()
            
        except Exception as e:
            print(f"\n❌ Connection test failed: {e}")
            print("Please check your database URL and try again.")
            return 1

        # Step 3: Get SQL query (with table selection if available)
        query = prompt_service.prompt_query(available_tables_list)

        # Step 4: Get export options
        export_options = prompt_service.prompt_export_options()
        export_excel = export_options["excel"]
        export_pdf = export_options["pdf"]

        # Step 5: Get output paths
        output_paths = prompt_service.prompt_output_paths(export_excel, export_pdf)
        excel_path = output_paths.get("excel", "report.xlsx")
        pdf_path = output_paths.get("pdf")

        # Step 6: Ask about email
        send_email = prompt_service.prompt_send_email()
        email_config = None
        email_recipients = None
        email_cc_recipients = None
        email_subject = "Database Report"

        if send_email:
            # Prompt for email configuration
            email_config = prompt_service.prompt_email_config()
            email_subject = prompt_service.prompt_email_subject()
            email_recipients = prompt_service.prompt_email_recipients()
            email_cc_recipients = prompt_service.prompt_email_cc_recipients()

        # Execute query and export
        result = query_service.execute_and_export(
            database_type=database_type,
            database_url=database_url,
            query=query,
            export_excel=export_excel,
            export_pdf=export_pdf,
            excel_path=excel_path,
            pdf_path=pdf_path,
            send_email=send_email,
            email_recipients=email_recipients,
            email_subject=email_subject,
            email_cc_recipients=email_cc_recipients,
            email_config=email_config,
        )

        if result["success"]:
        return 0
        else:
            return 1

    except KeyboardInterrupt:
        print("\n\n✗ Operation cancelled by user")
        return 1
    except ValueError as e:
        print(f"\n✗ Configuration error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"\n✗ Runtime error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
