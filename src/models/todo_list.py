"""TodoList collection for managing tasks."""

from typing import Optional
from src.models.task import Task
from src.utils.errors import TaskNotFoundError, ValidationError


class TodoList:
    """Collection managing all tasks with CRUD operations."""

    def __init__(self) -> None:
        """Initialize an empty TodoList."""
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(
        self,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """
        Add a new task to the list.

        Args:
            title: Task title (required, must not be empty)
            description: Optional task description

        Returns:
            The created Task object

        Raises:
            ValidationError: If title is empty after stripping whitespace
        """
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")

        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            status="pending"
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            The Task object

        Raises:
            TaskNotFoundError: If task with given ID does not exist
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return self.tasks[task_id]

    def list_all(self) -> list[Task]:
        """
        Get all tasks sorted by ID.

        Returns:
            List of all Task objects sorted by ID (ascending)
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update a task's title and/or description.

        Args:
            task_id: ID of the task to update
            title: New title (None to keep current title)
            description: New description (None to keep current, "" to clear)

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task with given ID does not exist
            ValidationError: If new title is empty
        """
        task = self.get_task(task_id)

        if title is not None:
            task.update_title(title)

        if description is not None:
            task.update_description(description)

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Raises:
            TaskNotFoundError: If task with given ID does not exist
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        del self.tasks[task_id]

    def mark_complete(self, task_id: int, complete: bool = True) -> Task:
        """
        Mark a task as complete or pending.

        Args:
            task_id: ID of the task to mark
            complete: True to mark complete, False to mark pending

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If task with given ID does not exist
        """
        task = self.get_task(task_id)
        task.status = "complete" if complete else "pending"
        return task

    def count(self) -> int:
        """Get the total number of tasks."""
        return len(self.tasks)

    def is_empty(self) -> bool:
        """Check if the task list is empty."""
        return len(self.tasks) == 0
