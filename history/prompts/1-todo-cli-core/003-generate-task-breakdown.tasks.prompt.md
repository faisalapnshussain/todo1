---
id: 003
title: Generate Task Breakdown
stage: tasks
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 1-todo-cli-core
branch: 1-todo-cli-core
user: user
command: /sp.tasks
labels: ["tasks", "breakdown", "user-stories", "mvp", "incremental-delivery"]
links:
  spec: specs/1-todo-cli-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-todo-cli-core/tasks.md
tests:
 - Task format validation (all tasks follow checkbox [ID] [P?] [Story?] format)
 - User story independence validation (each story testable independently)
---

## Prompt

```text
— Phase I: Todo In-Memory Python Console App

Initialization Tasks

Create project structure:

/src — Python source code

/data — For storing any future data (optional for in-memory)

README.md — Setup instructions

CLAUDE.md — Instructions for Claude Code usage

Add main.py entry file

Implement init command:

Initializes empty todo list in memory

Displays success message

Model Tasks
4. Create Todo class in /src/models/todo.py:

Fields: id, title, description, completed, created_at

Methods: to_dict(), from_dict(), __repr__()

Core Feature Tasks
5. Implement add command:

Add a new todo to the in-memory list

Assign unique incremental ID

Implement view command:

List all todos with ID, title, status, timestamp

Implement update command:

Update title and description by ID

Handle invalid ID

Implement delete command:

Delete a todo by ID

Confirm deletion

Implement mark complete command:

Toggle todo completed/pending status

CLI & User Experience Tasks
10. Use console output formatting (UV or Rich if desired)
11. Add colored status indicators (Pending / Done)
12. Display clear success/error messages for each operation

Error Handling Tasks
13. Handle invalid commands, missing IDs, empty list
14. Handle actions before init is run (show warning)

Validation & Testing Tasks
15. Run each CLI command in UV to confirm expected behavior
16. Ensure project can be initialized and run easily using init

Documentation Tasks
17. Update README.md with:
- Setup instructions
- CLI commands usage examples
18. Update CLAUDE.md with:
- Claude Code instructions for spec-driven workflow
```

## Response snapshot

Generated comprehensive task breakdown organized by user stories for incremental, independent delivery.

**Task Structure** (`tasks.md`):

**38 Total Tasks** organized into 7 phases:

1. **Phase 1: Setup (7 tasks)**:
   - UV project initialization (uv init, uv add typer)
   - Directory structure creation (src/models, src/services, src/cli, src/utils)
   - pyproject.toml configuration with script entry point
   - Parallel opportunities: __init__.py file creation (T003-T006)

2. **Phase 2: Foundational (5 tasks)** - BLOCKS all user stories:
   - Custom exceptions (TodoError, TaskNotFoundError, ValidationError)
   - Task entity (id, title, description, status + methods)
   - TodoList collection (tasks dict, next_id, CRUD operations)
   - Input validator (validate_title, validate_id)
   - Output formatter (format_task_list, format_task)
   - Parallel opportunities: 4 out of 5 tasks can run in parallel

3. **Phase 3: User Story 1 - Add and View (5 tasks)** 🎯 MVP:
   - Implement add command with Typer (title required, description optional)
   - Implement view command with formatter
   - Error handling for empty title (stderr)
   - Empty list message handling
   - Typer app creation and command registration
   - Independent test: Add tasks, view formatted list with status indicators

4. **Phase 4: User Story 2 - Mark Complete (5 tasks)**:
   - Implement complete command (task_id, --undo flag)
   - Error handling for TaskNotFoundError and ValueError
   - Update formatter for ✓/○ status indicators
   - Command registration
   - Independent test: Mark tasks complete/pending, verify visual distinction

5. **Phase 5: User Story 3 - Update Details (5 tasks)**:
   - Implement update command (--title, --description flags)
   - Validation for at least one field provided
   - Error handling for not found and empty title
   - Command registration
   - Independent test: Update titles and descriptions, verify persistence

6. **Phase 6: User Story 4 - Delete Tasks (4 tasks)**:
   - Implement delete command
   - Error handling for not found and invalid ID
   - Command registration
   - Independent test: Delete tasks, verify ID non-reuse

7. **Phase 7: Polish (7 tasks)**:
   - Documentation (README.md, CLAUDE.md)
   - Manual validation (UTF-8 indicators, stderr, validation, ID management)
   - Full acceptance scenario testing

**Key Design Decisions**:

1. **User Story Organization**: Each story (P1-P4) is independently implementable and testable
2. **MVP Scope**: Phase 1-3 (17 tasks) delivers working add/view functionality
3. **Parallel Execution**: 11 tasks marked [P] for concurrent execution
4. **Incremental Delivery**: Each story adds value without breaking prior stories
5. **Manual Testing Only**: No automated tests per spec requirements
6. **Foundational Blocking**: Phase 2 must complete before any user story work

**Task Format Compliance**:
- ✓ All tasks follow `- [ ] [ID] [P?] [Story?] Description with file path` format
- ✓ Sequential IDs (T001-T038)
- ✓ [P] markers for parallelizable tasks (11 tasks)
- ✓ [US1-US4] labels for user story tasks (19 tasks)
- ✓ Exact file paths in all implementation tasks

**Dependency Structure**:
- Setup → Foundational → User Stories → Polish
- User Stories 1-4 are independent after Foundational completes
- Within stories: natural command → error handling → registration order

**Manual Test Checkpoints**: 4 independent test validations (one per user story)

**Implementation Strategies Provided**:
1. MVP First: Setup + Foundational + US1 (17 tasks)
2. Incremental: Add one story at a time, validate, deploy
3. Parallel Team: 4 developers work on US1-US4 simultaneously after Foundational

## Outcome

- ✅ Impact: Complete task breakdown ready for implementation, clear execution paths defined
- 🧪 Tests: Manual testing approach specified, 4 independent test checkpoints per user story
- 📁 Files: tasks.md with 38 tasks across 7 phases
- 🔁 Next prompts: `/sp.implement` to execute tasks in dependency order
- 🧠 Reflection: Task breakdown successfully organized by user story priority (P1-P4) for maximum delivery flexibility. MVP scope clearly defined (17 tasks for add/view). Foundational phase properly blocks all user stories to ensure solid base. Each story independently testable with clear acceptance criteria and manual test scenarios.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks properly formatted with IDs, labels, and file paths
- Graders run and results (PASS/FAIL): Format validation PASS (38/38 tasks follow checklist format), Independence validation PASS (4 user stories can be tested independently)
- Prompt variant (if applicable): Standard task generation from spec user stories + plan structure + data model
- Next experiment (smallest change to try): Execute `/sp.implement` to begin Phase 1 (Setup) tasks, then validate Foundational phase before proceeding to user stories
