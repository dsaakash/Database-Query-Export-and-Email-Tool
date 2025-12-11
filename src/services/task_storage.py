"""Storage service for scheduled tasks."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import uuid

from src.core.task_model import ScheduledTask


class TaskStorage:
    """Service for storing and retrieving scheduled tasks."""

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize task storage.

        Args:
            storage_path: Path to JSON file for storing tasks (default: tasks.json in project root)
        """
        if storage_path is None:
            storage_path = Path(__file__).parent.parent.parent / "tasks.json"
        
        self.storage_path = Path(storage_path)
        self._ensure_storage_file()

    def _ensure_storage_file(self) -> None:
        """Ensure storage file exists."""
        if not self.storage_path.exists():
            self.storage_path.write_text(json.dumps([], indent=2))

    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load all tasks from storage."""
        try:
            if not self.storage_path.exists():
                return []
            content = self.storage_path.read_text()
            return json.loads(content) if content.strip() else []
        except (json.JSONDecodeError, IOError):
            return []

    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to storage."""
        self.storage_path.write_text(json.dumps(tasks, indent=2))

    def add_task(self, task: ScheduledTask) -> str:
        """Add a new task to storage.

        Args:
            task: ScheduledTask instance

        Returns:
            Task ID
        """
        tasks = self._load_tasks()
        
        # Generate task ID if not provided
        if not task.task_id:
            task.task_id = str(uuid.uuid4())
        
        # Check if task ID already exists
        if any(t.get("task_id") == task.task_id for t in tasks):
            raise ValueError(f"Task with ID '{task.task_id}' already exists")
        
        tasks.append(task.to_dict())
        self._save_tasks(tasks)
        return task.task_id

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            ScheduledTask instance or None if not found
        """
        tasks = self._load_tasks()
        for task_dict in tasks:
            if task_dict.get("task_id") == task_id:
                return ScheduledTask.from_dict(task_dict)
        return None

    def get_all_tasks(self) -> List[ScheduledTask]:
        """Get all tasks.

        Returns:
            List of ScheduledTask instances
        """
        tasks = self._load_tasks()
        return [ScheduledTask.from_dict(t) for t in tasks]

    def get_active_tasks(self) -> List[ScheduledTask]:
        """Get all active tasks.

        Returns:
            List of active ScheduledTask instances
        """
        all_tasks = self.get_all_tasks()
        return [t for t in all_tasks if t.is_active]

    def update_task(self, task: ScheduledTask) -> None:
        """Update an existing task.

        Args:
            task: Updated ScheduledTask instance

        Raises:
            ValueError: If task ID not found
        """
        tasks = self._load_tasks()
        found = False
        
        for i, task_dict in enumerate(tasks):
            if task_dict.get("task_id") == task.task_id:
                tasks[i] = task.to_dict()
                found = True
                break
        
        if not found:
            raise ValueError(f"Task with ID '{task.task_id}' not found")
        
        self._save_tasks(tasks)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        tasks = self._load_tasks()
        original_count = len(tasks)
        tasks = [t for t in tasks if t.get("task_id") != task_id]
        
        if len(tasks) < original_count:
            self._save_tasks(tasks)
            return True
        return False

    def update_task_run_info(
        self,
        task_id: str,
        last_run: Optional[str] = None,
        next_run: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        """Update task run information.

        Args:
            task_id: Task ID
            last_run: Last run timestamp (ISO format)
            next_run: Next run timestamp (ISO format)
            error: Error message if task failed
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")
        
        if last_run:
            task.last_run = last_run
            task.run_count += 1
        
        if next_run:
            task.next_run = next_run
        
        if error:
            task.error_count += 1
            task.last_error = error
        else:
            # Clear error on successful run
            task.last_error = None
        
        self.update_task(task)

