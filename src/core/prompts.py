"""Interactive prompt system for user inputs."""

from typing import List, Optional


class PromptService:
    """Service for interactive user prompts."""

    @staticmethod
    def prompt_database_type() -> str:
        """Prompt user to select database type.

        Returns:
            Selected database type (always PostgreSQL)
        """
        print("\n" + "="*60)
        print("Database Type: PostgreSQL")
        print("="*60)
        print("This application supports PostgreSQL database connections.")
        print("="*60)
        
        return "postgresql"

    @staticmethod
    def prompt_database_url(database_type: str, config=None) -> str:
        """Prompt user to enter database URL or use from .env.

        Args:
            database_type: Type of database
            config: Optional Config instance to check for .env database URL

        Returns:
            Database connection URL
        """
        # Check if database URL exists in .env
        use_env = False
        env_database_url = None
        
        if config:
            env_database_url = config.get_database_url(database_type)
            if env_database_url:
                print("\n" + "="*60)
                print(f"Database URL found in .env file")
                print("="*60)
                # Show URL with masked password for security
                if "@" in env_database_url and ":" in env_database_url.split("@")[0]:
                    # Mask password: postgresql://user:***@host:port/database
                    url_parts = env_database_url.split("@")
                    auth_part = url_parts[0]
                    if ":" in auth_part:
                        scheme_user = auth_part.rsplit(":", 1)[0]
                        masked_url = f"{scheme_user}:***@{url_parts[1]}"
                        print(f"Database URL: {masked_url}")
                    else:
                        print(f"Database URL: {env_database_url[:60]}..." if len(env_database_url) > 60 else f"Database URL: {env_database_url}")
                else:
                    print(f"Database URL: {env_database_url[:60]}..." if len(env_database_url) > 60 else f"Database URL: {env_database_url}")
                print("="*60)
                
                while True:
                    choice = input("Use database URL from .env file? (yes/no, default: yes): ").strip().lower()
                    if choice in ["yes", "y", ""]:
                        use_env = True
                        break
                    elif choice in ["no", "n"]:
                        use_env = False
                        break
                    else:
                        print("Please enter 'yes' or 'no'.")
        
        if use_env and env_database_url:
            print(f"✓ Using database URL from .env file")
            return env_database_url
        
        # Prompt for manual entry
        print("\n" + "="*60)
        print(f"Enter {database_type.upper()} Database URL:")
        print("="*60)

        # Only PostgreSQL is supported
        print("Format: postgresql://username:password@host:port/database")
        print("Example: postgresql://user:pass@localhost:5432/mydb")
        print("\nAlternative formats:")
        print("  - postgres://username:password@host:port/database")
        print("  - postgresql://user:pass@host:5432/dbname")

        print("="*60)

        while True:
            database_url = input("Database URL: ").strip()
            if database_url:
                return database_url
            print("Database URL cannot be empty. Please try again.")

    @staticmethod
    def prompt_query(available_tables: list = None) -> str:
        """Prompt user to enter SQL query with option to select from available tables.

        Args:
            available_tables: List of available table names in database

        Returns:
            SQL query string
        """
        print("\n" + "="*60)
        print("Enter SQL Query:")
        print("="*60)
        
        if available_tables and len(available_tables) > 0:
            print(f"📋 Available tables in database ({len(available_tables)}):")
            for i, table in enumerate(available_tables, 1):
                print(f"   {i}. {table}")
            print("\nYou can:")
            print("  - Enter table number to query (e.g., '1' for SELECT * FROM table_name)")
            print("  - Enter custom SQL query")
            print("  - Type 'END' on a new line to finish multi-line queries")
        else:
            print("(You can enter multi-line queries. Type 'END' on a new line to finish)")
        
        print("="*60)

        # First input - check if it's a table number
        first_input = input("Enter table number or SQL query: ").strip()
        
        # Check if user entered a table number
        if available_tables and first_input.isdigit():
            table_index = int(first_input) - 1
            if 0 <= table_index < len(available_tables):
                selected_table = available_tables[table_index]
                print(f"\n✓ Selected table: {selected_table}")
                query = f"SELECT * FROM {selected_table}"
                print(f"Generated query: {query}")
                
                # Ask if user wants to modify the query
                modify = input("\nModify query? (yes/no, default: no): ").strip().lower()
                if modify in ["yes", "y"]:
                    print("\nEnter your custom query (Type 'END' on a new line to finish):")
                    query_lines = [query]  # Start with the generated query
                    while True:
                        line = input()
                        if line.strip().upper() == "END":
                            break
                        query_lines.append(line)
                    query = "\n".join(query_lines).strip()
                return query
        
        # User entered custom query
        query_lines = [first_input]
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            query_lines.append(line)

        query = "\n".join(query_lines).strip()
        if not query:
            print("Query cannot be empty. Please try again.")
            return PromptService.prompt_query(available_tables)
        return query

    @staticmethod
    def prompt_export_options() -> dict:
        """Prompt user for export options.

        Returns:
            Dictionary with export options (excel, pdf)
        """
        print("\n" + "="*60)
        print("Export Options:")
        print("="*60)
        print("1. Export to Excel (.xlsx) only")
        print("2. Export to PDF only")
        print("3. Export to both Excel and PDF")
        print("="*60)

        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                return {"excel": True, "pdf": False}
            elif choice == "2":
                return {"excel": False, "pdf": True}
            elif choice == "3":
                return {"excel": True, "pdf": True}
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    @staticmethod
    def prompt_email_config() -> dict:
        """Prompt user for email configuration.

        Returns:
            Dictionary with email configuration (smtp_user, smtp_password, smtp_host, smtp_port)
        """
        print("\n" + "="*60)
        print("Email Configuration:")
        print("="*60)
        print("Enter your SMTP email settings")
        print("="*60)

        smtp_user = input("SMTP Email (e.g., your_email@gmail.com): ").strip()
        if not smtp_user:
            raise ValueError("SMTP email is required")

        smtp_password = input("SMTP Password (App Password for Gmail/Outlook): ").strip()
        if not smtp_password:
            raise ValueError("SMTP password is required")

        smtp_host = input("SMTP Host (default: smtp.gmail.com): ").strip()
        if not smtp_host:
            smtp_host = "smtp.gmail.com"

        smtp_port_input = input("SMTP Port (default: 587): ").strip()
        smtp_port = int(smtp_port_input) if smtp_port_input else 587

        return {
            "smtp_user": smtp_user,
            "smtp_password": smtp_password,
            "smtp_host": smtp_host,
            "smtp_port": smtp_port,
        }

    @staticmethod
    def prompt_send_email() -> bool:
        """Prompt user if they want to send email.

        Returns:
            True if user wants to send email, False otherwise
        """
        print("\n" + "="*60)
        print("Email Options:")
        print("="*60)

        while True:
            choice = input("Do you want to send email? (yes/no): ").strip().lower()
            if choice in ["yes", "y"]:
                return True
            elif choice in ["no", "n"]:
                return False
            else:
                print("Please enter 'yes' or 'no'.")

    @staticmethod
    def prompt_email_subject() -> str:
        """Prompt user for email subject.

        Returns:
            Email subject string
        """
        print("\n" + "="*60)
        print("Email Subject:")
        print("="*60)

        subject = input("Enter email subject (default: Database Report): ").strip()
        return subject if subject else "Database Report"

    @staticmethod
    def prompt_email_recipients() -> List[str]:
        """Prompt user for email recipients.

        Returns:
            List of recipient email addresses
        """
        print("\n" + "="*60)
        print("Email Recipients:")
        print("="*60)
        print("Enter recipient email addresses separated by commas")
        print("Example: user1@example.com, user2@example.com, user3@example.com")
        print("(Press Enter to finish, or type 'DONE')")
        print("="*60)

        recipients = []
        first_input = True
        
        while True:
            if first_input:
                line = input("Recipient emails (comma-separated): ").strip()
                first_input = False
            else:
                line = input("Add more recipients (comma-separated, or press Enter/DONE to finish): ").strip()
            
            # Check for DONE or empty line (finish input)
            if not line or line.upper() == "DONE":
                break
            
            # Handle comma-separated emails
            emails = [e.strip() for e in line.split(",") if e.strip()]
            recipients.extend(emails)
            
            # Show confirmation
            if len(emails) > 1:
                print(f"  ✓ Added {len(emails)} recipients")
            elif len(emails) == 1:
                print(f"  ✓ Added: {emails[0]}")

        if not recipients:
            print("No recipients provided. Please try again.")
            return PromptService.prompt_email_recipients()

        # Remove duplicates and validate
        unique_recipients = []
        invalid_emails = []
        
        for email in recipients:
            email = email.strip()
            # Basic email validation (must have @ and domain with dot)
            if "@" in email and "." in email.split("@")[1]:
                if email not in unique_recipients:
                    unique_recipients.append(email)
            else:
                invalid_emails.append(email)
        
        if invalid_emails:
            print(f"\n⚠ Warning: Invalid email addresses ignored: {', '.join(invalid_emails)}")
        
        if not unique_recipients:
            print("No valid recipients found. Please try again.")
            return PromptService.prompt_email_recipients()
        
        print(f"\n✓ Total recipients: {len(unique_recipients)}")
        print(f"  Recipients: {', '.join(unique_recipients)}")
        
        return unique_recipients

    @staticmethod
    def prompt_email_cc_recipients() -> List[str]:
        """Prompt user for CC (carbon copy) email recipients.

        Returns:
            List of CC recipient email addresses (empty list if none)
        """
        print("\n" + "="*60)
        print("CC Recipients (Optional):")
        print("="*60)
        print("Enter CC recipient email addresses separated by commas")
        print("Example: cc1@example.com, cc2@example.com")
        print("(Press Enter to skip, or type 'DONE' to finish)")
        print("="*60)

        recipients = []
        first_input = True
        
        while True:
            if first_input:
                line = input("CC emails (comma-separated, or press Enter to skip): ").strip()
                first_input = False
            else:
                line = input("Add more CC recipients (comma-separated, or press Enter/DONE to finish): ").strip()
            
            # Check for DONE or empty line (finish input)
            if not line or line.upper() == "DONE":
                break
            
            # Handle comma-separated emails
            emails = [e.strip() for e in line.split(",") if e.strip()]
            recipients.extend(emails)
            
            # Show confirmation
            if len(emails) > 1:
                print(f"  ✓ Added {len(emails)} CC recipients")
            elif len(emails) == 1:
                print(f"  ✓ Added CC: {emails[0]}")

        # If no recipients provided, return empty list (CC is optional)
        if not recipients:
            return []

        # Remove duplicates and validate
        unique_recipients = []
        invalid_emails = []
        
        for email in recipients:
            email = email.strip()
            # Basic email validation (must have @ and domain with dot)
            if "@" in email and "." in email.split("@")[1]:
                if email not in unique_recipients:
                    unique_recipients.append(email)
            else:
                invalid_emails.append(email)
        
        if invalid_emails:
            print(f"\n⚠ Warning: Invalid CC email addresses ignored: {', '.join(invalid_emails)}")
        
        if unique_recipients:
            print(f"\n✓ Total CC recipients: {len(unique_recipients)}")
            print(f"  CC Recipients: {', '.join(unique_recipients)}")
        
        return unique_recipients

    @staticmethod
    def prompt_output_paths(export_excel: bool, export_pdf: bool) -> dict:
        """Prompt user for output file paths.

        Args:
            export_excel: Whether to export Excel
            export_pdf: Whether to export PDF

        Returns:
            Dictionary with output paths
        """
        paths = {}
        
        if export_excel:
            excel_path = input(
                "\nEnter Excel output path (default: report.xlsx): "
            ).strip()
            paths["excel"] = excel_path if excel_path else "report.xlsx"

        if export_pdf:
            pdf_path = input(
                "\nEnter PDF output path (default: report.pdf): "
            ).strip()
            paths["pdf"] = pdf_path if pdf_path else "report.pdf"

        return paths

    @staticmethod
    def prompt_create_sample_table(table_name: str = "dummy_examples") -> bool:
        """Prompt user if they want to create a sample table.

        Args:
            table_name: Name of the table to create

        Returns:
            True if user wants to create table, False otherwise
        """
        print("\n" + "="*60)
        print("Sample Table Creation:")
        print("="*60)
        print(f"No tables found in the database.")
        print(f"Would you like to create a sample table '{table_name}' with dummy data?")
        print("="*60)

        while True:
            choice = input("Create sample table? (yes/no, default: yes): ").strip().lower()
            if choice in ["yes", "y", ""]:
                return True
            elif choice in ["no", "n"]:
                return False
            else:
                print("Please enter 'yes' or 'no'.")

