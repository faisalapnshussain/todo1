# CLI Todo List - Phase I (In-Memory)

A simple command-line todo list application built with Python 3.13+ and UV, demonstrating spec-driven development principles.

## Overview

This is Phase I of the CLI Todo List project, featuring **in-memory storage only**. All tasks are stored in memory and lost when the application exits. This phase focuses on establishing the core architecture and command structure.

## Features

- ✅ **Add Tasks**: Create tasks with titles and optional descriptions
- ✅ **View Tasks**: Display all tasks with status indicators (○ pending, ✓ complete)
- ✅ **Mark Complete**: Toggle tasks between pending and complete status
- ✅ **Update Tasks**: Modify task titles and/or descriptions
- ✅ **Delete Tasks**: Remove tasks from the list

## Requirements

- Python 3.13+
- UV package manager ([installation guide](https://github.com/astral-sh/uv))

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo1
```

### 2. Install Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment
- Install Typer and dependencies
- Build and install the `todo` command

## Usage

### Add a Task

```bash
# Simple task
uv run todo add "Buy groceries"

# Task with description
uv run todo add "Deploy feature" --description "Deploy to staging first"

# Short flag
uv run todo add "Research" -d "ML frameworks comparison"
```

### View All Tasks

```bash
uv run todo view
```

**Output Example**:
```
TODO LIST (2 tasks)

[1] ○ Buy groceries
    Status: pending

[2] ✓ Deploy feature
    Description: Deploy to staging first
    Status: complete
```

**Status Indicators**:
- `○` = Pending task
- `✓` = Completed task

### Mark Task Complete

```bash
# Mark complete
uv run todo complete 1

# Mark pending (undo)
uv run todo complete 1 --undo
```

### Update a Task

```bash
# Update title only
uv run todo update 1 --title "Buy groceries and supplies"

# Update description only
uv run todo update 2 --description "New description"

# Update both
uv run todo update 3 -t "New title" -d "New description"

# Clear description
uv run todo update 3 --description ""
```

### Delete a Task

```bash
uv run todo delete 1
```

**Note**: Task IDs are never reused. After deleting task #2, the next new task will be #4, not #2.

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add <title>` | Create a new task | `uv run todo add "Task title"` |
| `add <title> -d <desc>` | Create task with description | `uv run todo add "Title" -d "Description"` |
| `view` | List all tasks | `uv run todo view` |
| `complete <id>` | Mark task complete | `uv run todo complete 1` |
| `complete <id> --undo` | Mark task pending | `uv run todo complete 1 --undo` |
| `update <id> -t <title>` | Update task title | `uv run todo update 1 -t "New title"` |
| `update <id> -d <desc>` | Update task description | `uv run todo update 1 -d "New desc"` |
| `delete <id>` | Delete a task | `uv run todo delete 1` |

## Error Handling

The application provides clear error messages:

```bash
# Empty title
$ uv run todo add ""
Error: Title cannot be empty

# Task not found
$ uv run todo complete 999
Error: Task 999 not found

# Invalid ID
$ uv run todo delete abc
Error: Invalid task ID: must be a positive integer

# Missing update fields
$ uv run todo update 1
Error: Must provide --title and/or --description
```

## Architecture

### Project Structure

```
src/
├── models/          # Data entities (Task, TodoList)
├── services/        # Business logic and validation
├── cli/             # CLI commands and formatting
└── utils/           # Custom exceptions

specs/               # Feature specifications and design docs
history/             # Development artifacts (PHRs, ADRs)
```

### Key Design Decisions

- **Modular Design**: Each feature (add, view, update, delete, complete) is self-contained
- **Type Safety**: Python type hints throughout
- **Error Handling**: Custom exceptions with stderr output
- **Status Indicators**: UTF-8 symbols for visual distinction
- **ID Management**: Sequential, never-reused IDs

## Phase I Limitations

⚠️ **Important**: This is Phase I with in-memory storage only.

- **No Persistence**: Tasks are lost when the application exits
- **Single Session**: Each `uv run todo` command is a separate process
- **Demonstration Purpose**: Architecture is production-ready, but practical usage requires persistence

**Example of Limitation**:
```bash
# Session 1
$ uv run todo add "Task 1"
Task #1 added: Task 1

# Session 2 (separate process)
$ uv run todo view
TODO LIST (0 tasks)
No tasks yet.

# Task from Session 1 is NOT preserved
```

### Future Phases

- **Phase II**: File-based persistence (JSON/SQLite)
- **Phase III**: Advanced features (search, categories, due dates)
- **Phase IV**: Cloud sync and multi-device support

## Development

This project follows **Spec-Driven Development** principles:

1. Specification → Planning → Task Breakdown → Implementation
2. All features mapped to user stories (P1-P4 priorities)
3. Each user story independently testable
4. Constitutional compliance (modular, clean code, Python standards)

### Running Tests

Phase I uses manual testing:

```bash
# Test add command
uv run todo add "Test task"

# Test view command
uv run todo view

# Test complete command
uv run todo complete 1

# Test update command
uv run todo update 1 --title "Updated"

# Test delete command
uv run todo delete 1
```

### Development Documentation

- **Specification**: `specs/1-todo-cli-core/spec.md`
- **Implementation Plan**: `specs/1-todo-cli-core/plan.md`
- **Task Breakdown**: `specs/1-todo-cli-core/tasks.md`
- **Data Model**: `specs/1-todo-cli-core/data-model.md`
- **Contracts**: `specs/1-todo-cli-core/contracts/*.md`

## Getting Help

```bash
# General help
uv run todo --help

# Command-specific help
uv run todo add --help
uv run todo update --help
```

## Contributing

This project demonstrates spec-driven development workflows. See `CLAUDE.md` for development guidelines and Claude Code integration.

## License

[Your License Here]

## Acknowledgments

Built with:
- Python 3.13+
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [UV](https://github.com/astral-sh/uv) - Python package manager
- Claude Code - Spec-driven development workflow
