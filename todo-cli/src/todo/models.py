"""Data models for the todo application"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Task priority levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique integer identifier (auto-assigned, never reused)
        description: Text description of the task (1-500 chars)
        priority: Task priority (HIGH, MEDIUM, or LOW)
        completed: Whether the task is complete
        created_at: Timestamp when task was created
    """
    id: int
    description: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task attributes after initialization"""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(self.description, str):
            raise TypeError("Description must be a string")

        description = self.description.strip()
        if not description:
            raise ValueError("Description cannot be empty")

        if len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")

        if not isinstance(self.priority, Priority):
            raise TypeError("Priority must be a Priority enum value")

        if not isinstance(self.completed, bool):
            raise TypeError("Completed must be a boolean")
