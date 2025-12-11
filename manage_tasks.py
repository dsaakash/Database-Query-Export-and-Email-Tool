#!/usr/bin/env python3
"""
Task Management CLI - Add, list, update, and delete scheduled tasks.

Usage:
    python manage_tasks.py add          # Add a new scheduled task
    python manage_tasks.py list          # List all tasks
    python manage_tasks.py show <id>     # Show task details
    python manage_tasks.py delete <id>   # Delete a task
    python manage_tasks.py enable <id>   # Enable a task
    python manage_tasks.py disable <id>  # Disable a task
"""

import sys
import uuid
from datetime import datetime
from typing import Optional

from src.core.config import Config
from src.core.task_model import ScheduledTask
from src.core.prompts import PromptService
from src.services.task_storage import TaskStorage


def prompt_schedule_type() -> dict:
    """Wrapper for PromptService.prompt_schedule_type() for backward compatibility."""
    return PromptService.prompt_schedule_type()


def prompt_cron_schedule() -> dict:
    """Wrapper for PromptService.prompt_cron_schedule() for backward compatibility."""
    return PromptService.prompt_cron_schedule()


def prompt_interval_schedule() -> dict:
    """Wrapper for PromptService.prompt_interval_schedule() for backward compatibility."""
    return PromptService.prompt_interval_schedule()


def prompt_once_schedule() -> dict:
    """Wrapper for PromptService.prompt_once_schedule() for backward compatibility."""
    return PromptService.prompt_once_schedule()



def add_task():
    """Add a new scheduled task."""
    print("\n" + "="*60)
    print("Add New Scheduled Task")
    print("="*60)

    storage = TaskStorage()
    config = Config()

    # Get task details
    name = input("Task name: ").strip()
    if not name:
        print("❌ Task name is required")
        return 1

    description = input("Task description (optional): ").strip()

    # Database configuration
    print("\nDatabase Configuration:")
    database_type = "postgresql"  # Currently only PostgreSQL supported
    database_url = config.get_database_url(database_type)
    
    if not database_url:
        print("Database URL not found in .env file.")
        database_url = input("Enter PostgreSQL database URL: ").strip()
        if not database_url:
            print("❌ Database URL is required")
            return 1
    else:
        print(f"Using database URL from .env file")
        use_env = input("Use this URL? (yes/no, default: yes): ").strip().lower()
        if use_env in ["no", "n"]:
            database_url = input("Enter PostgreSQL database URL: ").strip()
            if not database_url:
                print("❌ Database URL is required")
                return 1

    # SQL Query
    print("\nSQL Query:")
    print("(Enter your SQL query. Type 'END' on a new line to finish)")
    print("Example:")
    print("  SELECT * FROM users;")
    print("  END")
    print("")
    query_lines = []
    first_line = True
    while True:
        if first_line:
            prompt = "Enter SQL query (or 'END' to finish): "
            first_line = False
        else:
            prompt = "  (continue query or 'END' to finish): "
        
        line = input(prompt)
        if line.strip().upper() == "END":
            break
        query_lines.append(line)
    
    query = "\n".join(query_lines).strip()
    if not query:
        print("❌ SQL query is required")
        return 1
    
    print(f"\n✓ Query captured ({len(query_lines)} line(s))")

    # Schedule configuration
    schedule_info = prompt_schedule_type()
    schedule_type = schedule_info["schedule_type"]
    schedule_config = schedule_info["schedule_config"]

    # Email configuration
    print("\nEmail Configuration:")
    email_recipients_str = input("Recipients (comma-separated): ").strip()
    email_recipients = [e.strip() for e in email_recipients_str.split(",") if e.strip()]
    if not email_recipients:
        print("❌ At least one email recipient is required")
        return 1

    email_cc_str = input("CC recipients (comma-separated, optional): ").strip()
    email_cc_recipients = [e.strip() for e in email_cc_str.split(",") if e.strip()] if email_cc_str else None

    email_subject = input("Email subject (default: Scheduled Database Report): ").strip()
    if not email_subject:
        email_subject = "Scheduled Database Report"

    # Export options
    print("\nExport Options:")
    export_excel = input("Export to Excel? (yes/no, default: yes): ").strip().lower() in ["yes", "y", ""]
    export_pdf = input("Export to PDF? (yes/no, default: no): ").strip().lower() in ["yes", "y"]

    excel_path = None
    if export_excel:
        excel_path = input("Excel file path (default: auto-generated): ").strip() or None

    pdf_path = None
    if export_pdf:
        pdf_path = input("PDF file path (default: auto-generated): ").strip() or None

    # Create task
    task = ScheduledTask(
        task_id=str(uuid.uuid4()),
        name=name,
        description=description,
        database_type=database_type,
        database_url=database_url,
        query=query,
        schedule_type=schedule_type,
        schedule_config=schedule_config,
        email_recipients=email_recipients,
        email_cc_recipients=email_cc_recipients,
        email_subject=email_subject,
        export_excel=export_excel,
        export_pdf=export_pdf,
        excel_path=excel_path,
        pdf_path=pdf_path,
        is_active=True,
    )

    try:
        task_id = storage.add_task(task)
        print(f"\n✅ Task added successfully!")
        print(f"   Task ID: {task_id}")
        print(f"   Name: {task.name}")
        print(f"\n💡 To activate this task, restart the scheduler daemon:")
        print(f"   python scheduler_daemon.py")
        return 0
    except Exception as e:
        print(f"\n❌ Failed to add task: {e}")
        return 1


def list_tasks():
    """List all tasks."""
    storage = TaskStorage()
    tasks = storage.get_all_tasks()

    if not tasks:
        print("\n📋 No tasks found. Add a task using: python manage_tasks.py add")
        return 0

    print("\n" + "="*60)
    print(f"Scheduled Tasks ({len(tasks)})")
    print("="*60)

    for i, task in enumerate(tasks, 1):
        status = "✅ Active" if task.is_active else "⏸️  Inactive"
        print(f"\n{i}. {task.name} [{status}]")
        print(f"   ID: {task.task_id}")
        print(f"   Schedule: {task.schedule_type}")
        if task.last_run:
            print(f"   Last run: {task.last_run}")
        if task.next_run:
            print(f"   Next run: {task.next_run}")
        print(f"   Run count: {task.run_count}")
        if task.error_count > 0:
            print(f"   ⚠ Errors: {task.error_count}")


def show_task(task_id: str):
    """Show detailed information about a task."""
    storage = TaskStorage()
    task = storage.get_task(task_id)

    if not task:
        print(f"❌ Task not found: {task_id}")
        return 1

    print("\n" + "="*60)
    print(f"Task Details: {task.name}")
    print("="*60)
    print(f"ID: {task.task_id}")
    print(f"Description: {task.description or '(none)'}")
    print(f"Status: {'✅ Active' if task.is_active else '⏸️  Inactive'}")
    print(f"\nDatabase:")
    print(f"  Type: {task.database_type}")
    print(f"  URL: {task.database_url[:50]}...")
    print(f"\nQuery:")
    print(f"  {task.query[:100]}..." if len(task.query) > 100 else f"  {task.query}")
    print(f"\nSchedule:")
    print(f"  Type: {task.schedule_type}")
    print(f"  Config: {task.schedule_config}")
    print(f"\nEmail:")
    print(f"  Recipients: {', '.join(task.email_recipients)}")
    if task.email_cc_recipients:
        print(f"  CC: {', '.join(task.email_cc_recipients)}")
    print(f"  Subject: {task.email_subject}")
    print(f"\nExport:")
    print(f"  Excel: {'Yes' if task.export_excel else 'No'}")
    print(f"  PDF: {'Yes' if task.export_pdf else 'No'}")
    print(f"\nStatistics:")
    print(f"  Created: {task.created_at}")
    print(f"  Last run: {task.last_run or 'Never'}")
    print(f"  Next run: {task.next_run or 'N/A'}")
    print(f"  Run count: {task.run_count}")
    print(f"  Error count: {task.error_count}")
    if task.last_error:
        print(f"  Last error: {task.last_error}")

    return 0


def delete_task(task_id: str):
    """Delete a task."""
    storage = TaskStorage()
    
    task = storage.get_task(task_id)
    if not task:
        print(f"❌ Task not found: {task_id}")
        return 1

    confirm = input(f"Are you sure you want to delete task '{task.name}'? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Cancelled.")
        return 0

    try:
        storage.delete_task(task_id)
        print(f"✅ Task '{task.name}' deleted successfully")
        print("💡 Restart the scheduler daemon for changes to take effect.")
        return 0
    except Exception as e:
        print(f"❌ Failed to delete task: {e}")
        return 1


def enable_task(task_id: str):
    """Enable a task."""
    storage = TaskStorage()
    task = storage.get_task(task_id)
    
    if not task:
        print(f"❌ Task not found: {task_id}")
        return 1

    task.is_active = True
    storage.update_task(task)
    print(f"✅ Task '{task.name}' enabled")
    print("💡 Restart the scheduler daemon for changes to take effect.")
    return 0


def disable_task(task_id: str):
    """Disable a task."""
    storage = TaskStorage()
    task = storage.get_task(task_id)
    
    if not task:
        print(f"❌ Task not found: {task_id}")
        return 1

    task.is_active = False
    storage.update_task(task)
    print(f"✅ Task '{task.name}' disabled")
    print("💡 Restart the scheduler daemon for changes to take effect.")
    return 0


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command = sys.argv[1].lower()

    if command == "add":
        return add_task()
    elif command == "list":
        return list_tasks()
    elif command == "show":
        if len(sys.argv) < 3:
            print("❌ Task ID required. Usage: python manage_tasks.py show <task_id>")
            return 1
        return show_task(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Task ID required. Usage: python manage_tasks.py delete <task_id>")
            return 1
        return delete_task(sys.argv[2])
    elif command == "enable":
        if len(sys.argv) < 3:
            print("❌ Task ID required. Usage: python manage_tasks.py enable <task_id>")
            return 1
        return enable_task(sys.argv[2])
    elif command == "disable":
        if len(sys.argv) < 3:
            print("❌ Task ID required. Usage: python manage_tasks.py disable <task_id>")
            return 1
        return disable_task(sys.argv[2])
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())

