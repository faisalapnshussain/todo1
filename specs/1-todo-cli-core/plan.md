# Implementation Plan: CLI Todo List - Core Functionality

**Branch**: `1-todo-cli-core` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-todo-cli-core/spec.md`

## Summary

Build an in-memory CLI todo list application in Python 3.13+ using UV for environment management. The application provides five core operations: add tasks (with title and optional description), view all tasks with status indicators, mark tasks complete/pending, update task details, and delete tasks. All data is stored in memory using Python data structures with no persistence. The CLI interface accepts commands via arguments or interactive prompts, outputs to stdout, and provides clear error messages via stderr.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Typer (CLI framework, optional - evaluate in Phase 0)
**Storage**: In-memory (Python lists/dictionaries, no persistence)
**Testing**: Manual testing via UV console (pytest optional for future phases)
**Target Platform**: Cross-platform (Windows, macOS, Linux) via UV
**Project Type**: Single project (console application)
**Performance Goals**: Sub-2-second response for all operations, support 100+ tasks
**Constraints**: In-memory only, single-user, CLI-only, UV environment required
**Scale/Scope**: ~100 tasks max, 5 core commands, Phase I MVP scope

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitutional Compliance

✅ **I. Spec-Driven Development (NON-NEGOTIABLE)**
- Status: PASS
- Evidence: Specification created and approved before planning phase
- Implementation follows: spec → plan → tasks → implementation workflow

✅ **II. In-Memory Storage Only (Phase I Constraint)**
- Status: PASS
- Evidence: FR-003 mandates Python data structures, no file/database persistence
- Implementation: Tasks stored in memory, lost on application exit

✅ **III. CLI-First Interface**
- Status: PASS
- Evidence: FR-012, FR-013 mandate CLI arguments/prompts, stdout/stderr output
- Implementation: Command-line interface for all five operations

✅ **IV. Modular Feature Design**
- Status: PASS
- Evidence: Constitution requires separate modules for each feature
- Implementation: Planned structure with /models, /services, /cli, /utils

✅ **V. Clean Code & Python Standards**
- Status: PASS
- Evidence: Python 3.13+, PEP 8, UV environment per constitution
- Implementation: Type hints, clear naming, modular design, UV tooling

### Constitutional Gates

All constitutional principles are satisfied. No violations requiring justification.

**Decision**: Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-cli-core/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (CLI framework evaluation)
├── data-model.md        # Phase 1 output (Task and TodoList entities)
├── quickstart.md        # Phase 1 output (usage guide)
├── contracts/           # Phase 1 output (CLI command specifications)
│   ├── add.md           # Add task command contract
│   ├── view.md          # View tasks command contract
│   ├── complete.md      # Mark complete command contract
│   ├── update.md        # Update task command contract
│   └── delete.md        # Delete task command contract
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── task.py          # Task entity with id, title, description, status
│   └── todo_list.py     # TodoList collection with CRUD operations
├── services/
│   ├── __init__.py
│   ├── task_service.py  # Business logic for task operations
│   └── validator.py     # Input validation (title not empty, ID valid)
├── cli/
│   ├── __init__.py
│   ├── commands.py      # CLI command definitions (add, view, update, etc.)
│   └── formatter.py     # Output formatting for task display
└── utils/
    ├── __init__.py
    └── errors.py        # Custom exception classes

tests/
├── manual/
│   └── test_scenarios.md  # Manual test scenarios for UV console
├── integration/           # Reserved for future automated tests
└── unit/                  # Reserved for future automated tests

pyproject.toml             # UV project configuration
uv.lock                    # UV lockfile (generated)
README.md                  # Project overview and quickstart
```

**Structure Decision**: Single project structure selected. This is a console application with no frontend/backend separation. The modular structure (/models, /services, /cli, /utils) aligns with constitutional Principle IV (Modular Feature Design). Each of the five core features will be implemented as methods in task_service.py, with CLI commands in commands.py delegating to the service layer.

## Complexity Tracking

> No constitutional violations - this section is not needed.

## Phase 0: Research & Design Decisions

### Research Tasks

1. **CLI Framework Evaluation**
   - Decision needed: Use Typer (suggested), argparse (stdlib), or click?
   - Research focus: Ease of use for 5 simple commands, UV compatibility, type hints support
   - Deliverable: Framework recommendation in research.md

2. **Error Handling Patterns**
   - Research: Best practices for CLI error messages (stderr output)
   - Research: Exception handling patterns for invalid ID, empty title, etc.
   - Deliverable: Error handling strategy in research.md

3. **Console Output Formatting**
   - Research: Simple text formatting vs. rich library for task display
   - Research: Status indicator patterns (checkmarks, symbols, colors)
   - Deliverable: Output format recommendation in research.md

### Phase 0 Output

**File**: `specs/1-todo-cli-core/research.md`

**Contents**:
- CLI Framework Decision (Typer vs argparse vs click)
  - Rationale for selection
  - Alternatives considered
  - UV compatibility verification
- Error Handling Strategy
  - Exception class hierarchy
  - stderr output patterns
  - User-facing error messages
- Output Formatting Approach
  - Task list display format
  - Status indicator choices (pending vs complete)
  - Empty list message

## Phase 1: Detailed Design

### Data Model (`data-model.md`)

**Entities to define**:

1. **Task**
   - Fields: id (int), title (str), description (str | None), status (str: "pending" | "complete")
   - Validation: title min 1 char, id immutable, status enum
   - Behaviors: toggle_status(), update_title(), update_description()

2. **TodoList**
   - Fields: tasks (dict[int, Task]), next_id (int)
   - Behaviors: add_task(), get_task(), update_task(), delete_task(), mark_complete(), list_all()
   - ID management: Sequential from 1, never reused

### CLI Contracts (`contracts/`)

**Command specifications** (one file per command):

1. **add.md**: `todo add "title" [--description "desc"]`
   - Input: title (required), description (optional)
   - Output: "Task #{id} added: {title}" to stdout
   - Errors: Empty title → stderr "Error: Title cannot be empty"

2. **view.md**: `todo view`
   - Input: None
   - Output: Formatted list of all tasks with ID, title, status
   - Errors: None (empty list shows "No tasks yet")

3. **complete.md**: `todo complete <id>` or `todo complete <id> --undo`
   - Input: id (required), --undo flag (optional)
   - Output: "Task #{id} marked complete/pending"
   - Errors: Invalid ID → stderr "Error: Task {id} not found"

4. **update.md**: `todo update <id> --title "new" [--description "new"]`
   - Input: id (required), title and/or description (at least one required)
   - Output: "Task #{id} updated"
   - Errors: Invalid ID, no fields provided, empty title

5. **delete.md**: `todo delete <id>`
   - Input: id (required)
   - Output: "Task #{id} deleted"
   - Errors: Invalid ID → stderr "Error: Task {id} not found"

### Quickstart Guide (`quickstart.md`)

**Contents**:
- UV environment setup: `uv init`, `uv add typer` (if selected)
- Running the app: `uv run src/cli/commands.py <command>`
- Example usage for each of 5 commands
- Common error scenarios and solutions

### Phase 1 Deliverables

1. `specs/1-todo-cli-core/research.md` - Technology decisions
2. `specs/1-todo-cli-core/data-model.md` - Entity definitions
3. `specs/1-todo-cli-core/contracts/` - Five command specifications
4. `specs/1-todo-cli-core/quickstart.md` - Usage guide
5. Constitution Check re-evaluation (post-design)

## Next Steps

After `/sp.plan` completion:
1. Run `/sp.tasks` to generate task breakdown from this plan
2. Run `/sp.implement` to execute tasks in dependency order
3. Manual validation against acceptance criteria in spec.md
4. Run `/sp.git.commit_pr` to commit work

## Notes

- This plan focuses on Phase I MVP: in-memory storage only
- Future phases can add: file persistence, search, categories, due dates
- Testing strategy: Manual console testing sufficient for Phase I
- Architecture supports future extensibility (persistence layer can be added to services/)
