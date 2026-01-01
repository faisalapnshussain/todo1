"""Task entity representing a single todo item."""

from typing import Optional
from src.utils.errors import ValidationError


class Task:
    """Represents a single todo task with id, title, description, and status."""

    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        status: str = "pending"
    ) -> None:
        """
        Initialize a Task instance.

        Args:
            id: Unique task identifier (positive integer)
            title: Task title (minimum 1 character after strip)
            description: Optional task description
            status: Task status ("pending" or "complete")
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    def toggle_status(self) -> None:
        """Toggle task status between 'pending' and 'complete'."""
        if self.status == "pending":
            self.status = "complete"
        else:
            self.status = "pending"

    def update_title(self, new_title: str) -> None:
        """
        Update the task title.

        Args:
            new_title: New title for the task

        Raises:
            ValidationError: If new_title is empty after stripping whitespace
        """
        if not new_title or not new_title.strip():
            raise ValidationError("Title cannot be empty")
        self.title = new_title

    def update_description(self, new_description: Optional[str]) -> None:
        """
        Update the task description.

        Args:
            new_description: New description (None to clear description)
        """
        self.description = new_description

    def is_complete(self) -> bool:
        """
        Check if task is complete.

        Returns:
            True if status is 'complete', False otherwise
        """
        return self.status == "complete"

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"Task(id={self.id}, title=\"{self.title}\", status=\"{self.status}\")"
