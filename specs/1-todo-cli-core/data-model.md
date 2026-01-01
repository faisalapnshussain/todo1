# Data Model: CLI Todo List

**Feature**: CLI Todo List - Core Functionality
**Date**: 2026-01-01
**Purpose**: Define entities, their attributes, validation rules, and behaviors

## Entity Overview

The application has two primary entities:

1. **Task** - Individual todo item with title, description, and status
2. **TodoList** - Collection managing all tasks with CRUD operations

## Task Entity

### Attributes

| Attribute | Type | Required | Default | Immutable | Description |
|-----------|------|----------|---------|-----------|-------------|
| id | int | Yes | Auto-assigned | Yes | Unique sequential identifier (1, 2, 3...) |
| title | str | Yes | None | No | Task title, minimum 1 character after strip() |
| description | str \| None | No | None | No | Optional task details, can be empty or absent |
| status | str | Yes | "pending" | No | Task completion state: "pending" or "complete" |

### Validation Rules

1. **ID Validation**:
   - Must be positive integer (> 0)
   - Assigned automatically on creation
   - Cannot be changed after creation
   - Validated on lookup operations

2. **Title Validation**:
   - Cannot be empty after stripping whitespace
   - Minimum length: 1 character (post-strip)
   - Maximum length: No explicit limit (Python string)
   - Validated on create and update operations

3. **Description Validation**:
   - Optional field
   - Can be None, empty string, or any text
   - No minimum or maximum length
   - Validated: None (always valid)

4. **Status Validation**:
   - Must be exactly "pending" or "complete" (case-sensitive)
   - Defaults to "pending" on creation
   - Changed only via mark_complete operation or explicit toggle
   - Validated on assignment

### Behaviors

**Constructor**:
```python
Task(id: int, title: str, description: str | None = None, status: str = "pending")
```

**Methods**:

1. `toggle_status() -> None`
   - Switches status between "pending" and "complete"
   - If current status is "pending", set to "complete"
   - If current status is "complete", set to "pending"

2. `update_title(new_title: str) -> None`
   - Updates the task title
   - Validates new_title is not empty (post-strip)
   - Raises ValidationError if empty

3. `update_description(new_description: str | None) -> None`
   - Updates the task description
   - Accepts None to clear description
   - No validation required

4. `is_complete() -> bool`
   - Returns True if status == "complete"
   - Returns False if status == "pending"

5. `__repr__() -> str`
   - Returns string representation for debugging
   - Format: `Task(id={id}, title="{title}", status="{status}")`

### State Transitions

```
[Create Task]
     ↓
  pending ←→ complete
     ↑          ↓
  [toggle_status()]
```

**Valid Transitions**:
- Create → pending (default)
- pending → complete (mark complete)
- complete → pending (unmark/toggle)

**Invalid Transitions**:
- Any other status values (validated on assignment)

## TodoList Entity

### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| tasks | dict[int, Task] | Yes | {} | Dictionary mapping task IDs to Task objects |
| next_id | int | Yes | 1 | Counter for next task ID to assign |

### ID Management

- **Initial State**: `next_id = 1`, `tasks = {}`
- **On Add**: Assign current `next_id` to new task, increment `next_id`
- **On Delete**: Remove task from dictionary, do NOT decrement `next_id`
- **ID Reuse**: Never reuse IDs (next_id only increases)
- **Lookup Efficiency**: O(1) via dictionary keys

### Validation Rules

1. **Task ID Existence**:
   - Before get/update/delete/mark_complete: verify `id in tasks`
   - If not found: raise `TaskNotFoundError(f"Task {id} not found")`

2. **Task Object Validity**:
   - Validate Task object before adding to dictionary
   - Ensure title is not empty via Task constructor validation

### Behaviors

**Constructor**:
```python
TodoList()
```
- Initializes empty tasks dictionary
- Sets next_id to 1

**Methods**:

1. `add_task(title: str, description: str | None = None) -> Task`
   - Validates title is not empty (calls validator)
   - Creates new Task with current next_id
   - Adds task to tasks dictionary
   - Increments next_id
   - Returns created Task object
   - Raises: `ValidationError` if title empty

2. `get_task(task_id: int) -> Task`
   - Looks up task by ID in dictionary
   - Returns Task object if found
   - Raises: `TaskNotFoundError` if ID not in tasks

3. `list_all() -> list[Task]`
   - Returns list of all Task objects
   - Sorted by task ID (ascending)
   - Returns empty list if no tasks
   - No exceptions raised

4. `update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task`
   - Gets task by ID (may raise TaskNotFoundError)
   - Updates title if provided and not None
   - Updates description if provided (None clears description)
   - At least one of title or description must be provided
   - Validates new title if updating title
   - Returns updated Task object
   - Raises: `TaskNotFoundError`, `ValidationError`

5. `delete_task(task_id: int) -> None`
   - Gets task by ID (may raise TaskNotFoundError)
   - Removes task from tasks dictionary
   - Does NOT decrement next_id
   - Raises: `TaskNotFoundError`

6. `mark_complete(task_id: int, complete: bool = True) -> Task`
   - Gets task by ID (may raise TaskNotFoundError)
   - If complete=True: sets status to "complete"
   - If complete=False: sets status to "pending"
   - Alternative: can use task.toggle_status() for toggle behavior
   - Returns updated Task object
   - Raises: `TaskNotFoundError`

7. `count() -> int`
   - Returns total number of tasks (len(tasks))
   - Used for display: "TODO LIST (3 tasks)"

8. `is_empty() -> bool`
   - Returns True if len(tasks) == 0
   - Used to show "No tasks yet" message

### Example Usage Flow

```python
# Initialize
todo_list = TodoList()  # next_id=1, tasks={}

# Add tasks
task1 = todo_list.add_task("Buy groceries")
# task1.id=1, next_id=2, tasks={1: task1}

task2 = todo_list.add_task("Write plan", "Phase I implementation")
# task2.id=2, next_id=3, tasks={1: task1, 2: task2}

# View all
all_tasks = todo_list.list_all()  # [task1, task2]

# Mark complete
todo_list.mark_complete(1)  # task1.status = "complete"

# Update
todo_list.update_task(2, title="Write detailed plan")

# Delete
todo_list.delete_task(1)  # tasks={2: task2}, next_id=3 (unchanged)

# Add another
task3 = todo_list.add_task("Review code")
# task3.id=3, next_id=4, tasks={2: task2, 3: task3}
# Note: ID 1 is never reused
```

## Relationship Diagram

```
TodoList (1)
    │
    │ contains
    ↓
   Task (0..*)

TodoList:
- tasks: dict[int, Task]
- next_id: int

Task:
- id: int
- title: str
- description: str | None
- status: str
```

## Persistence Notes

**Phase I (Current)**:
- All data stored in memory (TodoList instance)
- Data lost on application exit
- No file or database operations

**Future Phases**:
- TodoList could serialize/deserialize to JSON
- Task entity remains unchanged
- Add save()/load() methods to TodoList

## Implementation Files

- **src/models/task.py**: Task class definition
- **src/models/todo_list.py**: TodoList class definition
- **src/services/validator.py**: Validation functions (validate_title, validate_id)
- **src/utils/errors.py**: Custom exceptions (TaskNotFoundError, ValidationError)

## Validation Summary

| Operation | Validation | Exception |
|-----------|-----------|-----------|
| add_task() | Title not empty | ValidationError |
| get_task() | ID exists | TaskNotFoundError |
| update_task() | ID exists, title not empty (if updating) | TaskNotFoundError, ValidationError |
| delete_task() | ID exists | TaskNotFoundError |
| mark_complete() | ID exists | TaskNotFoundError |
| list_all() | None | None |

## Type Hints

All methods use Python type hints:

```python
from typing import Optional

class Task:
    def __init__(self, id: int, title: str, description: Optional[str] = None,
                 status: str = "pending") -> None: ...
    def toggle_status(self) -> None: ...
    def update_title(self, new_title: str) -> None: ...
    def is_complete(self) -> bool: ...

class TodoList:
    def add_task(self, title: str, description: Optional[str] = None) -> Task: ...
    def get_task(self, task_id: int) -> Task: ...
    def list_all(self) -> list[Task]: ...
    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Task: ...
    def delete_task(self, task_id: int) -> None: ...
    def mark_complete(self, task_id: int, complete: bool = True) -> Task: ...
```

Aligns with Constitution Principle V (Python Standards with type hints encouraged).
