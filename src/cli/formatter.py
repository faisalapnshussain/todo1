"""Output formatting for task display in the CLI."""

from src.models.task import Task


class Formatter:
    """Handles formatting of tasks for console output."""

    @staticmethod
    def format_task_list(tasks: list[Task], count: int) -> str:
        """
        Format a list of tasks for display.

        Args:
            tasks: List of Task objects to format
            count: Total number of tasks

        Returns:
            Formatted string ready for console output
        """
        lines = [f"TODO LIST ({count} tasks)\n"]

        for task in tasks:
            icon = "✓" if task.is_complete() else "○"
            lines.append(f"[{task.id}] {icon} {task.title}")

            if task.description:
                lines.append(f"    Description: {task.description}")

            lines.append(f"    Status: {task.status}\n")

        return "\n".join(lines)

    @staticmethod
    def format_task(task: Task) -> str:
        """
        Format a single task for display.

        Args:
            task: Task object to format

        Returns:
            Formatted string for the task
        """
        icon = "✓" if task.is_complete() else "○"
        lines = [f"[{task.id}] {icon} {task.title}"]

        if task.description:
            lines.append(f"    Description: {task.description}")

        lines.append(f"    Status: {task.status}")

        return "\n".join(lines)

    @staticmethod
    def format_empty_list() -> str:
        """
        Format message for empty task list.

        Returns:
            Formatted empty list message
        """
        return 'TODO LIST (0 tasks)\n\nNo tasks yet. Use \'todo add "title"\' to create one.'
