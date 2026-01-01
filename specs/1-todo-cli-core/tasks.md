---
description: "Task list for CLI Todo List - Core Functionality"
---

# Tasks: CLI Todo List - Core Functionality

**Input**: Design documents from `/specs/1-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification. This feature does NOT request automated tests, so manual testing only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with `uv init` in project root
- [x] T002 Add Typer dependency with `uv add typer` for CLI framework
- [x] T003 [P] Create src/models/__init__.py as empty file
- [x] T004 [P] Create src/services/__init__.py as empty file
- [x] T005 [P] Create src/cli/__init__.py as empty file
- [x] T006 [P] Create src/utils/__init__.py as empty file
- [x] T007 Configure pyproject.toml with script entry point: `todo = "src.cli.commands:app"`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 [P] Create custom exception classes in src/utils/errors.py (TodoError, TaskNotFoundError, ValidationError)
- [x] T009 [P] Create Task entity class in src/models/task.py with id, title, description, status attributes and methods
- [x] T010 Create TodoList collection class in src/models/todo_list.py with tasks dict, next_id counter, and CRUD methods
- [x] T011 [P] Create input validator functions in src/services/validator.py (validate_title, validate_id)
- [x] T012 Create output formatter class in src/cli/formatter.py with format_task_list() and format_task() methods

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks and view them in a formatted list

**Independent Test**: Add several tasks with titles and optional descriptions, then view the list to confirm all tasks appear with correct information and status indicators (○ for pending)

### Implementation for User Story 1

- [x] T013 [P] [US1] Implement add command in src/cli/commands.py using Typer with title (required) and description (optional flag)
- [x] T014 [P] [US1] Implement view command in src/cli/commands.py using Typer with no arguments, calls formatter
- [x] T015 [US1] Add error handling to add command for ValidationError (empty title) with stderr output
- [x] T016 [US1] Add empty list message handling to view command ("No tasks yet" message)
- [x] T017 [US1] Create Typer app instance in src/cli/commands.py and register add/view commands

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add tasks and view them.

**Manual Test Scenarios**:
1. Run `uv run todo add "Buy groceries"` - should show "Task #1 added: Buy groceries"
2. Run `uv run todo add "Write plan" --description "Phase I implementation"` - should show "Task #2 added: Write plan"
3. Run `uv run todo view` - should show formatted list with both tasks, status indicators (○), descriptions
4. Run `uv run todo add ""` - should show error "Error: Title cannot be empty"

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete/pending to track progress

**Independent Test**: Create tasks, mark some complete, view the list to verify status changes (○ vs ✓), and toggle tasks between complete and pending states

### Implementation for User Story 2

- [x] T018 [US2] Implement complete command in src/cli/commands.py with task_id (required int) and --undo flag (optional)
- [x] T019 [US2] Add error handling to complete command for TaskNotFoundError (invalid ID) with stderr output
- [x] T020 [US2] Add error handling for ValueError (non-numeric ID) with stderr output
- [x] T021 [US2] Update formatter to display ✓ for complete tasks and ○ for pending tasks
- [x] T022 [US2] Register complete command with Typer app in src/cli/commands.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and mark tasks complete.

**Manual Test Scenarios**:
1. Run `uv run todo complete 1` - should show "Task #1 marked complete"
2. Run `uv run todo view` - should show task #1 with ✓ indicator
3. Run `uv run todo complete 1 --undo` - should show "Task #1 marked pending"
4. Run `uv run todo complete 999` - should show error "Error: Task 999 not found"

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to modify task titles and descriptions

**Independent Test**: Create tasks, update their titles and/or descriptions, and verify the changes persist when viewing the task list

### Implementation for User Story 3

- [x] T023 [US3] Implement update command in src/cli/commands.py with task_id (required int), --title flag (optional str), --description flag (optional str)
- [x] T024 [US3] Add validation to update command to ensure at least one of --title or --description is provided
- [x] T025 [US3] Add error handling to update command for TaskNotFoundError with stderr output
- [x] T026 [US3] Add error handling to update command for ValidationError (empty title) with stderr output
- [x] T027 [US3] Register update command with Typer app in src/cli/commands.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently.

**Manual Test Scenarios**:
1. Run `uv run todo update 1 --title "Buy groceries and supplies"` - should show "Task #1 updated"
2. Run `uv run todo update 2 --description "Updated description"` - should show "Task #2 updated"
3. Run `uv run todo update 3 -t "New title" -d "New description"` - should show "Task #3 updated"
4. Run `uv run todo update 1 --title ""` - should show error "Error: Title cannot be empty"
5. Run `uv run todo update 999 --title "Test"` - should show error "Error: Task 999 not found"
6. Run `uv run todo update 1` - should show error "Error: Must provide --title and/or --description"

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove tasks from the list

**Independent Test**: Create tasks, delete specific tasks by ID, and verify they no longer appear in the task list

### Implementation for User Story 4

- [x] T028 [US4] Implement delete command in src/cli/commands.py with task_id (required int)
- [x] T029 [US4] Add error handling to delete command for TaskNotFoundError with stderr output
- [x] T030 [US4] Add error handling to delete command for ValueError (non-numeric ID) with stderr output
- [x] T031 [US4] Register delete command with Typer app in src/cli/commands.py

**Checkpoint**: All user stories should now be independently functional. All 5 core commands work.

**Manual Test Scenarios**:
1. Run `uv run todo delete 1` - should show "Task #1 deleted"
2. Run `uv run todo view` - should NOT show task #1
3. Run `uv run todo delete 999` - should show error "Error: Task 999 not found"
4. Run `uv run todo add "New task"` - should assign ID that continues sequence (not reusing deleted IDs)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T032 [P] Create README.md with project overview, UV setup instructions, and command reference examples
- [x] T033 [P] Update CLAUDE.md (if exists) with spec-driven workflow instructions for Phase I
- [x] T034 Verify all CLI commands display UTF-8 status indicators correctly (○ and ✓) via manual testing
- [x] T035 Verify all error messages go to stderr and use exit code 1 via manual testing
- [x] T036 Verify empty title validation works across add and update commands via manual testing
- [x] T037 Verify task ID never reused after deletion via manual testing
- [x] T038 Run full manual test suite covering all acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Enhances US1 but independently testable

### Within Each User Story

- All tasks within a story follow natural dependency order
- [P] marked tasks can run in parallel within their phase
- Commands depend on their error handling being implemented
- Typer app registration happens after command implementation

### Parallel Opportunities

- **Setup phase**: Tasks T003-T006 (create __init__.py files) can run in parallel
- **Foundational phase**: Tasks T008, T009, T011, T012 can run in parallel (different files)
- **User Story 1**: Tasks T013 and T014 can run in parallel (add and view commands)
- **Once Foundational completes**: All 4 user stories can be worked on in parallel by different developers

---

## Parallel Example: User Story 1

```bash
# After Foundational phase is complete, launch these in parallel:
Task T013: "Implement add command in src/cli/commands.py"
Task T014: "Implement view command in src/cli/commands.py"

# Then sequentially:
Task T015: "Add error handling to add command"
Task T016: "Add empty list handling to view command"
Task T017: "Create Typer app and register commands"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T012) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T013-T017)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can add tasks with `uv run todo add "title"`
   - Can view tasks with `uv run todo view`
   - Empty title shows error
   - Empty list shows helpful message
5. Deploy/demo if ready - you now have a working MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T012)
2. Add User Story 1 (T013-T017) → Test independently → Deploy/Demo (MVP! ✅)
3. Add User Story 2 (T018-T022) → Test independently → Deploy/Demo (Can now mark complete ✅)
4. Add User Story 3 (T023-T027) → Test independently → Deploy/Demo (Can now update ✅)
5. Add User Story 4 (T028-T031) → Test independently → Deploy/Demo (Can now delete ✅)
6. Polish (T032-T038) → Final validation and documentation
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T017)
   - Developer B: User Story 2 (T018-T022)
   - Developer C: User Story 3 (T023-T027)
   - Developer D: User Story 4 (T028-T031)
3. Stories complete and integrate independently
4. Team completes Polish together (T032-T038)

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing only (no automated test suite in Phase I per spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 7 tasks
- **Phase 2 (Foundational)**: 5 tasks (BLOCKS all user stories)
- **Phase 3 (User Story 1 - P1)**: 5 tasks ← MVP
- **Phase 4 (User Story 2 - P2)**: 5 tasks
- **Phase 5 (User Story 3 - P3)**: 5 tasks
- **Phase 6 (User Story 4 - P4)**: 4 tasks
- **Phase 7 (Polish)**: 7 tasks

**Total**: 38 tasks

**Parallel Tasks**: 11 tasks marked [P] can run in parallel within their phases

**MVP Scope**: Tasks T001-T017 (Phases 1-3) = 17 tasks for working add/view functionality

**Independent Test Checkpoints**: 4 (one after each user story phase)
