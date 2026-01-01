"""CLI commands for the Todo application using Typer."""

import sys
import io
from typing import Optional
import typer
from src.models.todo_list import TodoList
from src.cli.formatter import Formatter
from src.utils.errors import TaskNotFoundError, ValidationError

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Global TodoList instance (in-memory storage)
todo_list = TodoList()
formatter = Formatter()

# Create Typer app
app = typer.Typer(help="CLI Todo List - Manage your tasks from the command line")


@app.command()
def add(
    title: str = typer.Argument(..., help="Task title (required)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Task description (optional)")
) -> None:
    """Add a new task to the todo list."""
    try:
        task = todo_list.add_task(title, description)
        typer.echo(f"Task #{task.id} added: {task.title}")
    except ValidationError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def view() -> None:
    """View all tasks in the todo list."""
    if todo_list.is_empty():
        output = formatter.format_empty_list()
    else:
        tasks = todo_list.list_all()
        output = formatter.format_task_list(tasks, todo_list.count())

    typer.echo(output)


@app.command()
def complete(
    task_id: int = typer.Argument(..., help="ID of the task to mark complete/pending"),
    undo: bool = typer.Option(False, "--undo", help="Mark task as pending instead of complete")
) -> None:
    """Mark a task as complete or pending."""
    try:
        complete_status = not undo
        task = todo_list.mark_complete(task_id, complete_status)
        status_word = "pending" if undo else "complete"
        typer.echo(f"Task #{task_id} marked {status_word}")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError:
        typer.echo("Error: Invalid task ID: must be a positive integer", err=True)
        raise typer.Exit(code=1)


@app.command()
def update(
    task_id: int = typer.Argument(..., help="ID of the task to update"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New task title"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New task description")
) -> None:
    """Update a task's title and/or description."""
    if title is None and description is None:
        typer.echo("Error: Must provide --title and/or --description", err=True)
        raise typer.Exit(code=1)

    try:
        task = todo_list.update_task(task_id, title, description)
        typer.echo(f"Task #{task_id} updated")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except ValidationError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError:
        typer.echo("Error: Invalid task ID: must be a positive integer", err=True)
        raise typer.Exit(code=1)


@app.command()
def delete(
    task_id: int = typer.Argument(..., help="ID of the task to delete")
) -> None:
    """Delete a task from the list."""
    try:
        todo_list.delete_task(task_id)
        typer.echo(f"Task #{task_id} deleted")
    except TaskNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError:
        typer.echo("Error: Invalid task ID: must be a positive integer", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
