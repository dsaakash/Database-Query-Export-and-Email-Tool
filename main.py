#!/usr/bin/env python3
"""
PostgreSQL Query, Export, and Email Tool

An interactive Python application for connecting to PostgreSQL databases,
querying tables, exporting to Excel/PDF, and sending email reports.
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

from src.core.config import Config
from src.core.prompts import PromptService
from src.services.query_service import QueryService


def is_scheduler_running():
    """Check if scheduler daemon is already running."""
    try:
        # Check lock file first (most reliable)
        lock_file = Path(__file__).parent / ".scheduler_daemon.lock"
        if lock_file.exists():
            try:
                with open(lock_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # Verify process is still alive
                if platform.system() == "Windows":
                    result = subprocess.run(
                        ['tasklist', '/FI', f'PID eq {pid}'],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    )
                    if str(pid) in result.stdout:
                        return True
                    else:
                        # Process dead, remove lock file
                        try:
                            lock_file.unlink()
                        except Exception:
                            pass
                        return False
                else:
                    # Linux/Mac: Check if process exists
                    try:
                        os.kill(pid, 0)  # Signal 0 just checks if process exists
                        return True
                    except OSError:
                        # Process doesn't exist, remove lock file
                        try:
                            lock_file.unlink()
                        except Exception:
                            pass
                        return False
            except (ValueError, FileNotFoundError):
                # Invalid lock file, remove it
                try:
                    lock_file.unlink()
                except Exception:
                    pass
                return False
        
        # Fallback: Check process list
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ['wmic', 'process', 'where', 'name="python.exe"', 'get', 'commandline'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                return 'scheduler_daemon.py' in result.stdout
            except Exception:
                return False
        else:
            result = subprocess.run(
                ['pgrep', '-f', 'scheduler_daemon.py'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
    except Exception:
        return False


def start_scheduler_daemon():
    """Start the scheduler daemon in the background."""
    try:
        # Check if already running
        if is_scheduler_running():
            print("   ℹ️  Scheduler daemon is already running.")
            return True
        
        # Get the script directory
        script_dir = Path(__file__).parent.absolute()
        scheduler_script = script_dir / "scheduler_daemon.py"
        
        if not scheduler_script.exists():
            print("   ⚠️  scheduler_daemon.py not found. Please start it manually.")
            return False
        
        print("   🔄 Starting scheduler daemon...")
        
        # Start the daemon in background
        if platform.system() == "Windows":
            # Windows: Use START command which is more reliable
            try:
                # Use cmd /c start to launch in new window (more reliable than Popen flags)
                cmd = f'cmd /c start "Database Scheduler Daemon" /MIN "{sys.executable}" "{scheduler_script}"'
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    cwd=str(script_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as e:
                # Fallback: Try pythonw.exe (runs without console)
                try:
                    pythonw_path = str(sys.executable).replace("python.exe", "pythonw.exe")
                    if Path(pythonw_path).exists():
                        process = subprocess.Popen(
                            [pythonw_path, str(scheduler_script)],
                            cwd=str(script_dir),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    else:
                        # Final fallback: Regular python with CREATE_NEW_CONSOLE
                        CREATE_NEW_CONSOLE = 0x00000010
                        process = subprocess.Popen(
                            [sys.executable, str(scheduler_script)],
                            cwd=str(script_dir),
                            creationflags=CREATE_NEW_CONSOLE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                except Exception as e2:
                    print(f"   ⚠️  Error starting daemon: {e2}")
                    raise
        else:
            # Linux/Mac: Use nohup or detach
            process = subprocess.Popen(
                [sys.executable, str(scheduler_script)],
                cwd=str(script_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
        
        # Give it a moment to start
        import time
        time.sleep(3)
        
        # Check if process is still alive
        if process.poll() is None:  # None means still running
            print("   ✅ Scheduler daemon started successfully!")
            print(f"   📋 Process ID: {process.pid}")
            return True
        else:
            # Process exited, check for errors
            stdout, stderr = process.communicate()
            error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Unknown error"
            print(f"   ⚠️  Scheduler daemon exited immediately.")
            print(f"   Error: {error_msg[:200]}")
            print(f"   💡 Please start it manually:")
            print(f"      python scheduler_daemon.py")
            return False
            
    except Exception as e:
        print(f"   ⚠️  Failed to start scheduler daemon automatically: {e}")
        import traceback
        traceback.print_exc()
        print(f"   💡 Please start it manually:")
        print(f"      python scheduler_daemon.py")
        return False


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
            except Exception as e:
                print(f"⚠ Could not list tables: {e}")
                print("You can still continue with your queries.")
            
            # Offer table creation/modification options
            print("\n" + "="*60)
            print("Table Management Options:")
            print("="*60)
            table_options = prompt_service.prompt_table_creation_options()
            
            if table_options["action"] == "create_users":
                try:
                    table_name = table_options.get("table_name", "users")
                    db_adapter.create_users_table(table_name)
                    # Refresh table list
                    try:
                        available_tables = db_adapter.list_tables()
                        available_tables_list = available_tables
                    except Exception:
                        if table_name not in available_tables_list:
                            available_tables_list.append(table_name)
                except Exception as e:
                    print(f"✗ Failed to create users table: {e}")
            elif table_options["action"] == "create_custom":
                try:
                    ddl_query = table_options["ddl_query"]
                    db_adapter.execute_ddl_query(ddl_query)
                    # Refresh table list
                    try:
                        available_tables = db_adapter.list_tables()
                        available_tables_list = available_tables
                    except Exception:
                        pass
                except Exception as e:
                    print(f"✗ Failed to execute DDL query: {e}")
            elif table_options["action"] == "add_column":
                try:
                    db_adapter.add_column(
                        table_options["table_name"],
                        table_options["column_name"],
                        table_options["column_definition"]
                    )
                except Exception as e:
                    print(f"✗ Failed to add column: {e}")
            
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
        scheduled_task = None  # Store scheduled task info

        if send_email:
            # Prompt for email configuration
            email_config = prompt_service.prompt_email_config()
            email_subject = prompt_service.prompt_email_subject()
            email_recipients = prompt_service.prompt_email_recipients()
            email_cc_recipients = prompt_service.prompt_email_cc_recipients()
            
            # Ask if user wants to schedule this task BEFORE sending email
            print("\n" + "="*60)
            print("Schedule Task (Before Sending Email):")
            print("="*60)
            save_as_task = prompt_service.prompt_save_as_scheduled_task()
            
            if save_as_task:
                try:
                    from src.core.task_model import ScheduledTask
                    from src.services.task_storage import TaskStorage
                    import uuid
                    
                    print("\n" + "="*60)
                    print("Creating Scheduled Task")
                    print("="*60)
                    
                    # Get task name
                    task_name = input("Enter task name: ").strip()
                    if not task_name:
                        task_name = f"Scheduled Query - {email_subject}"
                    
                    task_description = input("Task description (optional): ").strip()
                    
                    # Get schedule configuration
                    schedule_info = prompt_service.prompt_schedule_for_task()
                    
                    # Create scheduled task with current settings
                    scheduled_task = ScheduledTask(
                        task_id=str(uuid.uuid4()),
                        name=task_name,
                        description=task_description,
                        database_type=database_type,
                        database_url=database_url,
                        query=query,
                        schedule_type=schedule_info["schedule_type"],
                        schedule_config=schedule_info["schedule_config"],
                        email_recipients=email_recipients or [],
                        email_cc_recipients=email_cc_recipients,
                        email_subject=email_subject,
                        export_excel=export_excel,
                        export_pdf=export_pdf,
                        excel_path=excel_path if excel_path != "report.xlsx" else None,
                        pdf_path=pdf_path,
                        is_active=True,
                    )
                    
                    # Save task
                    storage = TaskStorage()
                    task_id = storage.add_task(scheduled_task)
                    
                    print(f"\n✅ Task scheduled successfully!")
                    print(f"   Task ID: {task_id}")
                    print(f"   Name: {scheduled_task.name}")
                    print(f"   Schedule: {scheduled_task.schedule_type}")
                    print(f"\n📧 Now sending email...")
                    print("="*60)
                except Exception as e:
                    print(f"\n⚠ Failed to save task: {e}")
                    print("Continuing with email send...")
                    scheduled_task = None

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
            # Show scheduler instructions if task was scheduled
            if scheduled_task:
                print("\n" + "="*60)
                print("Scheduled Task Created!")
                print("="*60)
                print(f"✅ Task '{scheduled_task.name}' has been scheduled.")
                print(f"\n📅 The task will run automatically at the scheduled time.")
                
                # Automatically start scheduler daemon
                print(f"\n🚀 Starting scheduler daemon automatically...")
                print("="*60)
                daemon_started = start_scheduler_daemon()
                print("="*60)
                
                if daemon_started:
                    print(f"\n✅ Scheduler is now running! Your task will execute automatically.")
                    print(f"   The daemon is running in the background and will continue")
                    print(f"   until you stop it (or restart your computer).")
                    print(f"\n   📝 Note: You may see a new window/console for the scheduler.")
                    print(f"   This is normal - the scheduler is running there.")
                else:
                    print(f"\n⚠️  Automatic startup failed. Please start manually:")
                    print(f"\n   1. Start Scheduler Daemon manually (runs 24/7):")
                    print(f"      python scheduler_daemon.py")
                    print(f"\n   2. Use Windows Task Scheduler:")
                    print(f"      - Configure Windows Task Scheduler to run:")
                    print(f"        python run_scheduled_tasks.py")
                    print(f"      - Set it to run at your desired frequency")
                    print(f"      - See: docs/WINDOWS_TASK_SCHEDULER_SETUP.md")
                
                print(f"\n📋 View all scheduled tasks:")
                print(f"   python manage_tasks.py list")
                print(f"\n🛑 To stop the scheduler daemon:")
                print(f"   - Close the scheduler window, or")
                print(f"   - Use Task Manager to end the python.exe process running scheduler_daemon.py")
            
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
