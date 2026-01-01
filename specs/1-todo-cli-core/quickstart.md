# Quickstart Guide: CLI Todo List

**Feature**: CLI Todo List - Core Functionality
**Audience**: Python developers using UV
**Setup Time**: ~5 minutes

## Prerequisites

- Python 3.13+ installed
- UV installed ([installation guide](https://github.com/astral-sh/uv))
- Terminal/console access

## Initial Setup

### 1. Initialize UV Project

```bash
# Navigate to project directory
cd todo1

# Initialize UV project (if not already done)
uv init

# Project structure created:
# - pyproject.toml
# - src/ directory
```

### 2. Add Dependencies

```bash
# Add Typer for CLI framework
uv add typer

# Dependencies are added to pyproject.toml and uv.lock
```

### 3. Verify Setup

```bash
# Check Python version
uv run python --version
# Should show: Python 3.13.x

# Verify Typer installation
uv run python -c "import typer; print(typer.__version__)"
# Should show: 0.12.x or higher
```

## Running the Application

### Basic Usage

```bash
# Run via UV (after implementation)
uv run todo <command>

# Example commands:
uv run todo add "My first task"
uv run todo view
uv run todo complete 1
uv run todo update 1 --title "Updated task"
uv run todo delete 1
```

### Entry Point Configuration

The `pyproject.toml` includes a script entry point:

```toml
[project.scripts]
todo = "src.cli.commands:app"
```

This allows running: `uv run todo <command>` instead of `uv run python src/cli/commands.py <command>`

## Command Reference

### Add Task

Create a new task with title and optional description.

```bash
# Simple task
uv run todo add "Buy groceries"
# Output: Task #1 added: Buy groceries

# Task with description
uv run todo add "Deploy feature" --description "Deploy to staging first"
# Output: Task #2 added: Deploy feature

# Short flag for description
uv run todo add "Research frameworks" -d "Focus on ML/AI frameworks"
# Output: Task #3 added: Research frameworks
```

### View Tasks

Display all tasks with status indicators.

```bash
# View all tasks
uv run todo view

# Example output:
# TODO LIST (3 tasks)
#
# [1] ○ Buy groceries
#     Status: pending
#
# [2] ✓ Deploy feature
#     Description: Deploy to staging first
#     Status: complete
#
# [3] ○ Research frameworks
#     Description: Focus on ML/AI frameworks
#     Status: pending
```

**Status Indicators**:
- `○` = Pending task
- `✓` = Completed task

### Mark Task Complete

Toggle task between pending and complete status.

```bash
# Mark task complete
uv run todo complete 1
# Output: Task #1 marked complete

# Mark task pending (undo)
uv run todo complete 1 --undo
# Output: Task #1 marked pending
```

### Update Task

Modify task title and/or description.

```bash
# Update title only
uv run todo update 1 --title "Buy groceries and supplies"
# Output: Task #1 updated

# Update description only
uv run todo update 2 --description "Deploy to production after testing"
# Output: Task #2 updated

# Update both (short flags)
uv run todo update 3 -t "Research AI frameworks" -d "Compare PyTorch and TensorFlow"
# Output: Task #3 updated

# Clear description
uv run todo update 3 --description ""
# Output: Task #3 updated
```

### Delete Task

Remove a task permanently.

```bash
# Delete task
uv run todo delete 2
# Output: Task #2 deleted

# Note: Task IDs are never reused
# If you delete task #2, the next new task will be #4 (not #2)
```

## Common Workflows

### Daily Task Management

```bash
# Morning: Check what needs to be done
uv run todo view

# Add new tasks
uv run todo add "Team meeting at 10am"
uv run todo add "Code review for PR #123"
uv run todo add "Update documentation"

# As you complete tasks
uv run todo complete 1
uv run todo complete 2

# End of day: Review what's left
uv run todo view
```

### Task Refinement

```bash
# Add initial task
uv run todo add "Work on project"

# Later: Add more details
uv run todo update 1 -t "Work on CLI project" -d "Focus on error handling"

# Even later: Refine further
uv run todo update 1 --description "Implement error handling for all CLI commands"
```

### Cleaning Up

```bash
# View all tasks
uv run todo view

# Delete completed tasks
uv run todo delete 1
uv run todo delete 2

# Or keep them as a record (they're marked complete)
```

## Error Handling

### Common Errors and Solutions

**Error: Title cannot be empty**
```bash
$ uv run todo add ""
Error: Title cannot be empty

# Solution: Provide a non-empty title
$ uv run todo add "Valid title"
Task #1 added: Valid title
```

**Error: Task X not found**
```bash
$ uv run todo complete 999
Error: Task 999 not found

# Solution: Check available task IDs
$ uv run todo view
TODO LIST (2 tasks)
[1] ○ Task one
[2] ○ Task two

$ uv run todo complete 1
Task #1 marked complete
```

**Error: Invalid task ID**
```bash
$ uv run todo delete abc
Error: Invalid task ID: must be a positive integer

# Solution: Use numeric task ID
$ uv run todo delete 1
Task #1 deleted
```

**Error: Must provide --title and/or --description**
```bash
$ uv run todo update 1
Error: Must provide --title and/or --description

# Solution: Provide at least one field to update
$ uv run todo update 1 --title "New title"
Task #1 updated
```

## Tips and Best Practices

### 1. Use Descriptive Titles

```bash
# Poor
uv run todo add "Work"

# Better
uv run todo add "Work on CLI implementation"

# Best
uv run todo add "Implement error handling for CLI commands"
```

### 2. Use Descriptions for Context

```bash
# Add important details in description
uv run todo add "Deploy feature" -d "Deploy to staging first, then production after QA approval"
```

### 3. Regular Review

```bash
# Check tasks daily
uv run todo view

# Mark completed tasks
uv run todo complete <id>

# Remove old completed tasks periodically
uv run todo delete <id>
```

### 4. Task ID Management

- Task IDs start at 1 and increment
- IDs are never reused after deletion
- If you delete tasks 2 and 3, your list might have IDs: 1, 4, 5, 6
- This is normal and prevents confusion

## Troubleshooting

### Application Won't Start

```bash
# Check UV installation
uv --version

# Verify Python version
uv run python --version

# Reinstall dependencies
uv sync
```

### Commands Not Found

```bash
# Make sure you're in the project directory
pwd

# Verify pyproject.toml exists
ls pyproject.toml

# Check script entry point
grep -A 2 "\[project.scripts\]" pyproject.toml
```

### UTF-8 Display Issues

If status icons don't display correctly (`○` and `✓`):

1. Check terminal UTF-8 support
2. Application will fallback to ASCII: `[ ]` and `[X]`
3. Or update terminal encoding settings

## Data Persistence Notes

**Important**: This is Phase I with in-memory storage only.

- All tasks are stored in memory
- Tasks are lost when application exits
- Each `uv run todo` command is a separate session
- No file or database persistence in Phase I

**Example**:
```bash
# Session 1
$ uv run todo add "Task 1"
Task #1 added: Task 1

# Session 2 (separate process)
$ uv run todo view
TODO LIST (0 tasks)
No tasks yet. Use 'todo add "title"' to create one.

# Task from Session 1 is NOT preserved (in-memory only)
```

Future phases will add file/database persistence.

## Next Steps

After familiarizing yourself with the commands:

1. **Review the Implementation Plan**: `specs/1-todo-cli-core/plan.md`
2. **Check Data Model**: `specs/1-todo-cli-core/data-model.md`
3. **Review Contracts**: `specs/1-todo-cli-core/contracts/*.md`
4. **Start Implementation**: Run `/sp.tasks` to generate task breakdown

## Getting Help

```bash
# View command help
uv run todo --help

# View specific command help
uv run todo add --help
uv run todo update --help
```

## Summary

**5 Core Commands**:
1. `add` - Create tasks
2. `view` - List all tasks
3. `complete` - Mark tasks done/pending
4. `update` - Modify task details
5. `delete` - Remove tasks

**Remember**:
- All operations work with task IDs
- Status indicators: `○` (pending), `✓` (complete)
- Task IDs never reused
- Phase I: In-memory only (no persistence)

Start with: `uv run todo add "My first task"` and `uv run todo view`
