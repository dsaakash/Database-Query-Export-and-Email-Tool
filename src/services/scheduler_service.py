"""Scheduler service for running scheduled database queries."""

import logging
import os
import subprocess
import sys
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

from src.core.config import Config
from src.core.task_model import ScheduledTask
from src.services.query_service import QueryService
from src.services.task_storage import TaskStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for scheduling and executing database query tasks."""

    def __init__(self, config: Optional[Config] = None, storage: Optional[TaskStorage] = None):
        """Initialize scheduler service.

        Args:
            config: Configuration instance
            storage: TaskStorage instance
        """
        self.config = config or Config()
        self.storage = storage or TaskStorage()
        self.query_service = QueryService(self.config)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Scheduler service initialized")

    def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a scheduled task.

        Args:
            task: ScheduledTask to execute
        """
        logger.info(f"Executing task: {task.name} (ID: {task.task_id})")
        
        try:
            # Execute query and export
            result = self.query_service.execute_and_export(
                database_type=task.database_type,
                database_url=task.database_url,
                query=task.query,
                export_excel=task.export_excel,
                export_pdf=task.export_pdf,
                excel_path=task.excel_path or f"report_{task.task_id}.xlsx",
                pdf_path=task.pdf_path,
                send_email=True,
                email_recipients=task.email_recipients,
                email_subject=task.email_subject,
                email_cc_recipients=task.email_cc_recipients,
                email_config=None,  # Will use .env config
            )

            if result["success"]:
                logger.info(f"Task '{task.name}' executed successfully. Rows: {result.get('rows', 0)}")
                print(f"\n{'='*60}")
                print(f"✅ Scheduled Task Executed Successfully!")
                print(f"{'='*60}")
                print(f"Task: {task.name}")
                print(f"Email sent to: {', '.join(task.email_recipients)}")
                print(f"Rows processed: {result.get('rows', 0)}")
                print(f"{'='*60}\n")
                
                # Update task run info
                self.storage.update_task_run_info(
                    task_id=task.task_id,
                    last_run=datetime.now().isoformat(),
                    next_run=self._calculate_next_run(task),
                )
                
                # Prompt user if they want to go back to main menu
                self._prompt_main_menu_after_task()
            else:
                error_msg = result.get("message", "Unknown error")
                logger.error(f"Task '{task.name}' failed: {error_msg}")
                self.storage.update_task_run_info(
                    task_id=task.task_id,
                    last_run=datetime.now().isoformat(),
                    error=error_msg,
                )

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Task '{task.name}' execution error: {error_msg}", exc_info=True)
            self.storage.update_task_run_info(
                task_id=task.task_id,
                last_run=datetime.now().isoformat(),
                error=error_msg,
            )

    def _calculate_next_run(self, task: ScheduledTask) -> Optional[str]:
        """Calculate next run time for a task.

        Args:
            task: ScheduledTask instance

        Returns:
            Next run timestamp in ISO format or None
        """
        try:
            if task.schedule_type == "cron":
                # Get next run from scheduler
                job = self.scheduler.get_job(task.task_id)
                if job and job.next_run_time:
                    return job.next_run_time.isoformat()
            elif task.schedule_type == "interval":
                # Calculate next run based on interval
                if task.last_run:
                    from datetime import timedelta
                    last_run = datetime.fromisoformat(task.last_run)
                    interval_seconds = task.schedule_config.get("seconds", 3600)
                    next_run = last_run + timedelta(seconds=interval_seconds)
                    return next_run.isoformat()
            # For 'once' type, next_run is None
            return None
        except Exception as e:
            logger.warning(f"Could not calculate next run for task {task.task_id}: {e}")
            return None

    def _create_trigger(self, task: ScheduledTask):
        """Create APScheduler trigger from task configuration.

        Args:
            task: ScheduledTask instance

        Returns:
            APScheduler trigger instance
        """
        if task.schedule_type == "cron":
            cron_config = task.schedule_config
            return CronTrigger(
                year=cron_config.get("year"),
                month=cron_config.get("month"),
                day=cron_config.get("day"),
                week=cron_config.get("week"),
                day_of_week=cron_config.get("day_of_week"),
                hour=cron_config.get("hour"),
                minute=cron_config.get("minute"),
                second=cron_config.get("second", 0),
            )
        elif task.schedule_type == "interval":
            interval_config = task.schedule_config
            return IntervalTrigger(
                weeks=interval_config.get("weeks", 0),
                days=interval_config.get("days", 0),
                hours=interval_config.get("hours", 0),
                minutes=interval_config.get("minutes", 0),
                seconds=interval_config.get("seconds", 0),
            )
        elif task.schedule_type == "once":
            run_date = datetime.fromisoformat(task.schedule_config["run_date"])
            return DateTrigger(run_date=run_date)
        else:
            raise ValueError(f"Unknown schedule type: {task.schedule_type}")

    def add_task(self, task: ScheduledTask) -> None:
        """Add a task to the scheduler.

        Args:
            task: ScheduledTask to add
        """
        if not task.is_active:
            logger.info(f"Task '{task.name}' is inactive, not scheduling")
            return

        try:
            # Save task to storage
            self.storage.add_task(task)

            # Create trigger
            trigger = self._create_trigger(task)

            # Add job to scheduler
            self.scheduler.add_job(
                func=self._execute_task,
                trigger=trigger,
                args=[task],
                id=task.task_id,
                name=task.name,
                replace_existing=True,
            )

            # Calculate and save next run time
            next_run = self._calculate_next_run(task)
            if next_run:
                task.next_run = next_run
                self.storage.update_task(task)

            logger.info(f"Task '{task.name}' scheduled successfully (ID: {task.task_id})")
            if task.next_run:
                logger.info(f"Next run: {task.next_run}")

        except Exception as e:
            logger.error(f"Failed to add task '{task.name}': {e}", exc_info=True)
            raise

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the scheduler.

        Args:
            task_id: Task ID to remove
        """
        try:
            self.scheduler.remove_job(task_id)
            self.storage.delete_task(task_id)
            logger.info(f"Task removed: {task_id}")
        except Exception as e:
            logger.error(f"Failed to remove task {task_id}: {e}", exc_info=True)
            raise

    def update_task(self, task: ScheduledTask) -> None:
        """Update an existing task in the scheduler.

        Args:
            task: Updated ScheduledTask
        """
        try:
            # Remove old job if exists
            try:
                self.scheduler.remove_job(task.task_id)
            except Exception:
                pass  # Job might not exist

            # Update storage
            self.storage.update_task(task)

            # Re-add job if active
            if task.is_active:
                trigger = self._create_trigger(task)
                self.scheduler.add_job(
                    func=self._execute_task,
                    trigger=trigger,
                    args=[task],
                    id=task.task_id,
                    name=task.name,
                    replace_existing=True,
                )
                logger.info(f"Task '{task.name}' updated and rescheduled")
            else:
                logger.info(f"Task '{task.name}' updated (inactive)")

        except Exception as e:
            logger.error(f"Failed to update task '{task.name}': {e}", exc_info=True)
            raise

    def load_all_tasks(self) -> None:
        """Load all active tasks from storage and schedule them."""
        tasks = self.storage.get_active_tasks()
        logger.info(f"Loading {len(tasks)} active task(s) from storage")

        for task in tasks:
            try:
                trigger = self._create_trigger(task)
                self.scheduler.add_job(
                    func=self._execute_task,
                    trigger=trigger,
                    args=[task],
                    id=task.task_id,
                    name=task.name,
                    replace_existing=True,
                )
                logger.info(f"Loaded task: {task.name} (ID: {task.task_id})")
            except Exception as e:
                logger.error(f"Failed to load task '{task.name}': {e}", exc_info=True)

    def get_scheduled_jobs(self) -> list:
        """Get list of all scheduled jobs.

        Returns:
            List of job information dictionaries
        """
        jobs = []
        for job in self.scheduler.get_jobs():
            task = self.storage.get_task(job.id)
            jobs.append({
                "job_id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "task": task.to_dict() if task else None,
            })
        return jobs

    def _prompt_main_menu_after_task(self) -> None:
        """Prompt user if they want to go back to main menu after successful task execution.
        
        This will launch main.py in a new interactive session if user says yes.
        The scheduler daemon continues running 24/7 in the background.
        """
        try:
            # Get the main.py path
            script_dir = Path(__file__).parent.parent.parent
            main_script = script_dir / "main.py"
            
            if not main_script.exists():
                logger.warning("main.py not found. Cannot launch main menu.")
                return
            
            # Show prompt in scheduler daemon console (if visible)
            # Since daemon runs in background, we'll launch main.py in a new window
            # and it will show the prompt there
            print("\n" + "="*60)
            print("📧 Email Sent Successfully!")
            print("="*60)
            print("Would you like to run another query/export/email task?")
            print("This will open the main menu in a new window.")
            print("="*60)
            
            # For background daemon, we'll use a simple approach:
            # Launch main.py in a new window that the user can interact with
            # The scheduler continues running in the background
            
            # Create a simple prompt script that will ask and launch main.py
            prompt_script = script_dir / "_prompt_main_menu.py"
            prompt_code = f'''#!/usr/bin/env python3
"""Temporary script to prompt user and launch main menu."""
import sys
from pathlib import Path

script_dir = Path(__file__).parent
main_script = script_dir / "main.py"

print("\\n{'='*60}")
print("Return to Main Menu?")
print("={'='*60}")
print("A scheduled task just completed successfully!")
print("Would you like to run another query/export/email task?")
print("={'='*60}")

response = input("\\nGo back to main menu? (yes/no, default: no): ").strip().lower()

if response in ["yes", "y"]:
    print("\\n🚀 Launching main menu...")
    import subprocess
    import platform
    
    if platform.system() == "Windows":
        subprocess.Popen(
            [sys.executable, str(main_script)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        subprocess.Popen([sys.executable, str(main_script)], cwd=str(script_dir))
    print("✅ Main menu launched! The scheduler continues running in the background.")
else:
    print("   Continuing with scheduled tasks...")
'''
            
            # Write and execute the prompt script
            try:
                with open(prompt_script, 'w') as f:
                    f.write(prompt_code)
                
                # Launch the prompt script in a new window
                if platform.system() == "Windows":
                    # Windows: Launch in new console window
                    subprocess.Popen(
                        [sys.executable, str(prompt_script)],
                        cwd=str(script_dir),
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    # Linux/Mac: Launch in new terminal
                    try:
                        terminal = os.environ.get('TERM', 'xterm')
                        subprocess.Popen(
                            [terminal, '-e', sys.executable, str(prompt_script)],
                            cwd=str(script_dir)
                        )
                    except Exception:
                        subprocess.Popen([sys.executable, str(prompt_script)], cwd=str(script_dir))
                
                logger.info("Main menu prompt launched in new window")
                
            except Exception as e:
                logger.warning(f"Could not launch main menu prompt: {e}")
                # Fallback: Just launch main.py directly
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen(
                            [sys.executable, str(main_script)],
                            cwd=str(script_dir),
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )
                    else:
                        subprocess.Popen([sys.executable, str(main_script)], cwd=str(script_dir))
                    logger.info("Main menu launched directly")
                except Exception as e2:
                    logger.error(f"Failed to launch main menu: {e2}")
                
        except Exception as e:
            logger.warning(f"Could not prompt for main menu: {e}")
            # Don't fail the task execution if this fails

    def shutdown(self) -> None:
        """Shutdown the scheduler."""
        logger.info("Shutting down scheduler...")
        self.scheduler.shutdown(wait=True)
        logger.info("Scheduler shut down")

