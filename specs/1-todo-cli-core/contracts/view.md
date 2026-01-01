# Command Contract: View Tasks

**Command**: `todo view`
**Purpose**: Display all tasks with IDs, titles, descriptions, and status indicators
**Maps to**: FR-004 (display all tasks), User Story 1 (Add and View Tasks)

## Command Syntax

```bash
todo view
todo view [--status <pending|complete>]
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| --status | str | No | None | Filter by status (pending or complete) |

**Note**: Status filter is optional and may be implemented in future phases. Phase I shows all tasks.

## Input Validation

- No input validation required (no parameters in Phase I)
- If status filter added: must be "pending" or "complete"

## Output

### Success Case - Tasks Exist

**Format**:
```
TODO LIST ({count} tasks)

[{id}] {status_icon} {title}
    Description: {description}  [if description exists]
    Status: {status}

[repeat for each task]
```

**Status Icons**:
- Pending: `○` (U+25CB hollow circle)
- Complete: `✓` (U+2713 checkmark)

**Example**:
```bash
$ todo view
TODO LIST (3 tasks)

[1] ✓ Buy groceries
    Status: complete

[2] ○ Write project plan
    Description: Phase I implementation plan for todo CLI
    Status: pending

[3] ○ Review pull requests
    Status: pending
```

**Output Channel**: stdout
**Exit Code**: 0

### Success Case - Empty List

**Format**:
```
TODO LIST (0 tasks)

No tasks yet. Use 'todo add "title"' to create one.
```

**Example**:
```bash
$ todo view
TODO LIST (0 tasks)

No tasks yet. Use 'todo add "title"' to create one.
```

**Output Channel**: stdout
**Exit Code**: 0

## Behavior

1. Retrieves all tasks from TodoList via `list_all()`
2. If empty, displays empty message
3. If not empty, displays formatted list with:
   - Header with task count
   - Each task with ID, status icon, title
   - Description (indented, only if present)
   - Status (indented)
4. Returns exit code 0

## Examples

### Basic Usage

```bash
# View all tasks
$ todo view
TODO LIST (2 tasks)

[1] ○ Call dentist
    Status: pending

[2] ✓ Deploy feature
    Description: Deploy to staging environment first
    Status: complete
```

### Empty List

```bash
$ todo view
TODO LIST (0 tasks)

No tasks yet. Use 'todo add "title"' to create one.
```

## Error Cases

No error cases - view always succeeds (empty list is valid state)

## Implementation Notes

- Uses Typer for CLI parsing
- No arguments in Phase I
- Calls `TodoList.list_all()` to get all tasks
- Delegates formatting to `Formatter.format_task_list()`
- Handles empty list with special message
- Tasks sorted by ID (ascending)

## Service Layer Call

```python
# src/cli/commands.py
def view_command():
    tasks = todo_list.list_all()
    if todo_list.is_empty():
        print(f"TODO LIST (0 tasks)\n")
        print("No tasks yet. Use 'todo add \"title\"' to create one.")
    else:
        output = formatter.format_task_list(tasks, todo_list.count())
        print(output)
```

## Formatter Implementation

```python
# src/cli/formatter.py
def format_task_list(tasks: list[Task], count: int) -> str:
    lines = [f"TODO LIST ({count} tasks)\n"]
    for task in tasks:
        icon = "✓" if task.is_complete() else "○"
        lines.append(f"[{task.id}] {icon} {task.title}")
        if task.description:
            lines.append(f"    Description: {task.description}")
        lines.append(f"    Status: {task.status}\n")
    return "\n".join(lines)
```

## Acceptance Criteria

From User Story 1:
- ✓ All tasks displayed with ID, title, description, status
- ✓ Status clearly distinguishable (○ vs ✓)
- ✓ Empty list shows helpful message
- ✓ Task count displayed in header

## Related Requirements

- FR-004: System MUST display all tasks in formatted list
- FR-008: System MUST display clear status indicators
- FR-011: System MUST handle empty lists gracefully
- FR-013: System MUST output to stdout
