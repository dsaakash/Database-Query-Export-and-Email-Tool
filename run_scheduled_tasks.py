#!/usr/bin/env python3
"""
Run Scheduled Tasks - Execute all active scheduled tasks.

This script is designed to be triggered by Windows Task Scheduler or cron services.
It loads all active tasks and executes any that are due to run.

Usage:
    python run_scheduled_tasks.py [--task-id TASK_ID]
    
    --task-id: Optional. Execute only a specific task by ID
"""

import argparse
import sys
from datetime import datetime

from src.core.config import Config
from src.services.scheduler_service import SchedulerService
from src.services.task_storage import TaskStorage


def execute_all_tasks():
    """Execute all active tasks that are due to run."""
    print(f"\n{'='*60}")
    print(f"Scheduled Task Executor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        config = Config()
        storage = TaskStorage()
        scheduler_service = SchedulerService(config=config, storage=storage)

        # Load all active tasks
        active_tasks = storage.get_active_tasks()
        
        if not active_tasks:
            print("⚠ No active tasks found.")
            print("💡 Add tasks using: python manage_tasks.py add")
            return 0

        print(f"📋 Found {len(active_tasks)} active task(s)\n")

        executed_count = 0
        error_count = 0

        for task in active_tasks:
            try:
                print(f"{'='*60}")
                print(f"Executing: {task.name} (ID: {task.task_id[:8]}...)")
                print(f"{'='*60}")
                
                # Execute task directly
                scheduler_service._execute_task(task)
                executed_count += 1
                print(f"✅ Task '{task.name}' executed successfully\n")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Task '{task.name}' failed: {e}\n")

        print(f"{'='*60}")
        print(f"Execution Summary:")
        print(f"  ✅ Successful: {executed_count}")
        print(f"  ❌ Failed: {error_count}")
        print(f"  📊 Total: {len(active_tasks)}")
        print(f"{'='*60}\n")

        # Shutdown scheduler
        scheduler_service.shutdown()

        return 0 if error_count == 0 else 1

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def execute_specific_task(task_id: str):
    """Execute a specific task by ID."""
    print(f"\n{'='*60}")
    print(f"Executing Task: {task_id}")
    print(f"{'='*60}\n")

    try:
        config = Config()
        storage = TaskStorage()
        scheduler_service = SchedulerService(config=config, storage=storage)

        task = storage.get_task(task_id)
        if not task:
            print(f"❌ Task not found: {task_id}")
            return 1

        if not task.is_active:
            print(f"⚠ Task '{task.name}' is inactive. Skipping.")
            return 0

        print(f"Executing: {task.name}\n")
        scheduler_service._execute_task(task)
        
        scheduler_service.shutdown()
        print(f"\n✅ Task '{task.name}' executed successfully")
        return 0

    except Exception as e:
        print(f"\n❌ Error executing task: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Execute scheduled database query tasks"
    )
    parser.add_argument(
        "--task-id",
        type=str,
        help="Execute only a specific task by ID"
    )

    args = parser.parse_args()

    if args.task_id:
        return execute_specific_task(args.task_id)
    else:
        return execute_all_tasks()


if __name__ == "__main__":
    sys.exit(main())

