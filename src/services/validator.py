"""Input validation functions for the Todo CLI application."""

from src.utils.errors import ValidationError


def validate_title(title: str) -> None:
    """
    Validate that a task title is not empty.

    Args:
        title: The title to validate

    Raises:
        ValidationError: If title is empty after stripping whitespace
    """
    if not title or not title.strip():
        raise ValidationError("Title cannot be empty")


def validate_id(task_id: int) -> None:
    """
    Validate that a task ID is a positive integer.

    Args:
        task_id: The ID to validate

    Raises:
        ValidationError: If ID is not a positive integer
    """
    if task_id <= 0:
        raise ValidationError("Task ID must be a positive integer")
