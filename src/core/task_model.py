"""Task model for scheduled database queries."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
from pathlib import Path


@dataclass
class ScheduledTask:
    """Model for a scheduled database query task."""

    task_id: str
    name: str
    description: str
    database_type: str
    database_url: str
    query: str
    schedule_type: str  # 'cron', 'interval', 'once'
    schedule_config: Dict[str, Any]  # Cron expression or interval config
    email_recipients: List[str]
    email_cc_recipients: Optional[List[str]] = None
    email_subject: str = "Scheduled Database Report"
    export_excel: bool = True
    export_pdf: bool = False
    excel_path: Optional[str] = None
    pdf_path: Optional[str] = None
    is_active: bool = True
    created_at: str = ""
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    run_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None

    def __post_init__(self):
        """Set created_at if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScheduledTask":
        """Create task from dictionary."""
        return cls(**data)

    def to_json(self) -> str:
        """Convert task to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "ScheduledTask":
        """Create task from JSON string."""
        return cls.from_dict(json.loads(json_str))

