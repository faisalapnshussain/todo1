# Research: CLI Todo List - Technology Decisions

**Feature**: CLI Todo List - Core Functionality
**Date**: 2026-01-01
**Purpose**: Resolve technical unknowns and establish implementation patterns for Phase I

## CLI Framework Decision

### Decision: Use Typer

**Rationale**:
- Native type hint support aligns with constitution Principle V (Python Standards)
- Minimal boilerplate for simple commands (5 commands in Phase I)
- Excellent UV compatibility (pure Python, no special build requirements)
- Automatic help generation from function signatures and docstrings
- Built on click (mature, battle-tested foundation)
- Modern Python 3.6+ design patterns

**Alternatives Considered**:

1. **argparse (stdlib)**
   - Pros: No external dependency, part of standard library
   - Cons: More verbose code, manual type conversion, less intuitive API
   - Rejected: Boilerplate overhead outweighs stdlib benefit for 5 commands

2. **click**
   - Pros: Mature, widely used, flexible decorator-based API
   - Cons: Less type-safe than Typer, more decorator ceremony
   - Rejected: Typer provides same benefits with better type safety

3. **No framework (manual sys.argv parsing)**
   - Pros: Zero dependencies
   - Cons: Manual parsing, validation, help generation, error handling
   - Rejected: Violates Principle V (clean code) - reinventing solved problems

### Implementation Notes

- Install: `uv add typer`
- Entry point: `src/cli/commands.py` with Typer app
- Command pattern: One function per operation (add, view, update, delete, complete)
- Help generation: Automatic from docstrings and type hints

## Error Handling Strategy

### Exception Hierarchy

```
TodoError (base)
├── TaskNotFoundError     # Invalid task ID
├── ValidationError       # Empty title, invalid input
└── InvalidOperationError # Unsupported operation
```

### Pattern

1. **Service Layer**: Raise specific exceptions (TaskNotFoundError, ValidationError)
2. **CLI Layer**: Catch exceptions, write to stderr, exit with code 1
3. **User Messages**: Clear, actionable error text

### Error Output Format

```
Error: Task 999 not found
Error: Title cannot be empty
Error: Invalid task ID: must be a positive integer
```

### Implementation Notes

- Define exceptions in `src/utils/errors.py`
- Service methods raise exceptions on failure
- CLI commands catch and format for stderr
- Exit codes: 0 = success, 1 = error

## Console Output Formatting

### Decision: Simple Text Formatting (No External Library)

**Rationale**:
- Phase I scope is simple (list of tasks)
- Standard library string formatting sufficient
- No need for colors, tables, or complex layouts
- Keeps dependencies minimal
- Fast rendering for 100-task lists

**Alternatives Considered**:

1. **rich library**
   - Pros: Beautiful tables, colors, progress bars
   - Cons: Overkill for Phase I, adds dependency, may not work in all terminals
   - Rejected: Over-engineering for MVP

2. **tabulate**
   - Pros: Nice table formatting
   - Cons: Another dependency, Phase I doesn't need sophisticated tables
   - Rejected: Simple text adequate

### Task Display Format

**View command output**:

```
TODO LIST (3 tasks)

[1] ✓ Buy groceries
    Status: complete

[2] ○ Write project plan
    Description: Phase I implementation plan for todo CLI
    Status: pending

[3] ○ Review pull requests
    Status: pending
```

**Status Indicators**:
- Pending: `○` (hollow circle, U+25CB)
- Complete: `✓` (checkmark, U+2713)

**Empty List**:
```
TODO LIST (0 tasks)

No tasks yet. Use 'todo add "title"' to create one.
```

### Implementation Notes

- Formatter class: `src/cli/formatter.py`
- Methods: `format_task()`, `format_task_list()`, `format_empty_list()`
- UTF-8 encoding assumed (as per spec assumptions)
- Fallback ASCII: `[ ]` for pending, `[X]` for complete (if UTF-8 issues)

## Data Structure Decision

### In-Memory Storage: Dictionary of Tasks

**Decision**: Use `dict[int, Task]` for task storage

**Rationale**:
- O(1) lookup by ID (required for update, delete, complete operations)
- Simple iteration for view operation
- Natural ID management (keys are task IDs)
- Pythonic and clean

**Alternatives Considered**:

1. **List of Tasks**
   - Pros: Simple, ordered
   - Cons: O(n) lookup by ID, index ≠ task ID after deletions
   - Rejected: Performance and ID management issues

2. **dataclass with list**
   - Pros: Type-safe
   - Cons: Still O(n) lookup
   - Rejected: Same performance issue as plain list

### ID Management

- `next_id` counter: Starts at 1, increments on each add
- Never reuse IDs (per spec assumptions)
- IDs persist in dictionary keys

## Input Validation Strategy

### Validation Rules

1. **Title validation**: `len(title.strip()) >= 1`
   - Error: "Title cannot be empty"

2. **ID validation**:
   - Must be positive integer: `id > 0`
   - Must exist in task dictionary
   - Error: "Task {id} not found" or "Invalid task ID"

3. **Description validation**:
   - Optional, can be empty string or None
   - No minimum length

### Implementation

- Validator functions in `src/services/validator.py`
- Called before service operations
- Raise `ValidationError` with descriptive messages
- CLI layer converts to stderr output

## UV Project Configuration

### pyproject.toml Structure

```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "In-memory CLI todo list application"
requires-python = ">=3.13"
dependencies = [
    "typer>=0.12.0",
]

[project.scripts]
todo = "src.cli.commands:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### UV Commands

- Init project: `uv init`
- Add dependency: `uv add typer`
- Run app: `uv run todo <command>`
- Example: `uv run todo add "My task"`

## Summary

All technical unknowns resolved:

1. ✅ **CLI Framework**: Typer (type-safe, minimal boilerplate)
2. ✅ **Error Handling**: Custom exception hierarchy with stderr output
3. ✅ **Output Formatting**: Simple text with UTF-8 symbols (○/✓)
4. ✅ **Data Structure**: Dictionary of Task objects with O(1) lookup
5. ✅ **Input Validation**: Centralized validator with clear error messages
6. ✅ **UV Setup**: pyproject.toml with script entry point

**Ready for Phase 1**: Detailed data model and contract definitions
