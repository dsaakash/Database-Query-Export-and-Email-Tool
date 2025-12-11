#!/usr/bin/env python3
"""
Scheduler Daemon - Runs continuously to execute scheduled database queries.

This daemon loads all active tasks from storage and executes them according to their schedules.
It runs continuously until stopped (Ctrl+C or SIGTERM).
"""

import signal
import sys
import time
import os
from pathlib import Path

from src.core.config import Config
from src.services.scheduler_service import SchedulerService
from src.services.task_storage import TaskStorage

# Global scheduler instance
scheduler_service = None

# Lock file to track if daemon is running
LOCK_FILE = Path(__file__).parent / ".scheduler_daemon.lock"


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    print("\n\n🛑 Shutdown signal received. Stopping scheduler...")
    if scheduler_service:
        scheduler_service.shutdown()
    # Remove lock file
    if LOCK_FILE.exists():
        try:
            LOCK_FILE.unlink()
        except Exception:
            pass
    print("✓ Scheduler stopped. Goodbye!")
    sys.exit(0)


def main():
    """Main daemon entry point."""
    global scheduler_service

    # Check if already running (lock file exists)
    if LOCK_FILE.exists():
        try:
            # Check if process is still alive
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Try to check if process exists (Windows)
            import platform
            if platform.system() == "Windows":
                import subprocess
                result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True,
                    text=True
                )
                if str(pid) in result.stdout:
                    print(f"⚠️  Scheduler daemon is already running (PID: {pid})")
                    print("   If this is incorrect, delete the lock file:")
                    print(f"   {LOCK_FILE}")
                    return 1
        except Exception:
            # Lock file exists but can't verify, remove it
            try:
                LOCK_FILE.unlink()
            except Exception:
                pass
    
    # Create lock file with current process ID
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
    except Exception as e:
        print(f"⚠️  Warning: Could not create lock file: {e}")

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("\n" + "="*60)
    print("Database Query Scheduler Daemon")
    print("="*60)
    print("This daemon will run continuously to execute scheduled tasks.")
    print("Press Ctrl+C to stop.")
    print("="*60 + "\n")

    try:
        # Initialize services
        config = Config()
        storage = TaskStorage()
        scheduler_service = SchedulerService(config=config, storage=storage)

        # Load all active tasks
        print("📋 Loading scheduled tasks...")
        scheduler_service.load_all_tasks()

        active_jobs = scheduler_service.get_scheduled_jobs()
        if active_jobs:
            print(f"✅ Loaded {len(active_jobs)} active task(s):\n")
            for job in active_jobs:
                print(f"   • {job['name']} (ID: {job['job_id'][:8]}...)")
                if job['next_run']:
                    print(f"     Next run: {job['next_run']}")
        else:
            print("⚠ No active tasks found. Add tasks using the task manager CLI.")
            print("   Run: python manage_tasks.py add")

        print("\n" + "="*60)
        print("🔄 Scheduler is running. Waiting for scheduled tasks...")
        print("="*60 + "\n")

        # Keep the daemon running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        if scheduler_service:
            scheduler_service.shutdown()
        return 1


if __name__ == "__main__":
    sys.exit(main())

