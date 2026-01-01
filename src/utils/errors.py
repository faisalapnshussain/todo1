"""Custom exception classes for the Todo CLI application."""


class TodoError(Exception):
    """Base exception for all Todo application errors."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with the specified ID cannot be found."""
    pass


class ValidationError(TodoError):
    """Raised when input validation fails."""
    pass
