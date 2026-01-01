# Command Contract: Delete Task

**Command**: `todo delete`
**Purpose**: Remove a task from the list permanently
**Maps to**: FR-007 (delete task by ID), User Story 4 (Delete Tasks)

## Command Syntax

```bash
todo delete <task_id>
todo delete <task_id> [--force]
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | int | Yes | - | ID of task to delete (positional) |
| --force, -f | flag | No | False | Skip confirmation (future enhancement) |

**Note**: Confirmation prompt is optional and may be added in future phases. Phase I deletes immediately.

## Input Validation

1. **Task ID**:
   - Must be a positive integer
   - Must exist in the task list
   - Type conversion: string → int

## Output

### Success Case

**Format**:
```
Task #{id} deleted
```

**Example**:
```bash
$ todo delete 1
Task #1 deleted

$ todo delete 5
Task #5 deleted
```

**Output Channel**: stdout
**Exit Code**: 0

### Error Cases

| Error Condition | Error Message | Output Channel | Exit Code |
|----------------|---------------|----------------|-----------|
| Task not found | `Error: Task {id} not found` | stderr | 1 |
| Invalid ID format | `Error: Invalid task ID: must be a positive integer` | stderr | 1 |
| Missing ID argument | `Error: Missing required argument: task_id` | stderr | 1 |

## Behavior

1. Validates task_id is positive integer
2. Looks up task by ID (may raise TaskNotFoundError)
3. Removes task from TodoList
4. Prints confirmation to stdout
5. Returns exit code 0

**Important**: Deleted task IDs are never reused. The next_id counter continues incrementing.

## Examples

### Basic Usage

```bash
# Initial state
$ todo view
TODO LIST (3 tasks)

[1] ○ Buy groceries
    Status: pending

[2] ✓ Write plan
    Status: complete

[3] ○ Review PRs
    Status: pending

# Delete task
$ todo delete 2
Task #2 deleted

# Verify deletion
$ todo view
TODO LIST (2 tasks)

[1] ○ Buy groceries
    Status: pending

[3] ○ Review PRs
    Status: pending

# Add new task - note ID continues from 4 (not reusing 2)
$ todo add "New task"
Task #4 added: New task
```

### Delete Last Task

```bash
$ todo view
TODO LIST (1 task)

[1] ○ Single task
    Status: pending

$ todo delete 1
Task #1 deleted

$ todo view
TODO LIST (0 tasks)

No tasks yet. Use 'todo add "title"' to create one.
```

### Error Cases

```bash
# Task doesn't exist
$ todo delete 999
Error: Task 999 not found

# Invalid ID format
$ todo delete abc
Error: Invalid task ID: must be a positive integer

# Missing ID
$ todo delete
Error: Missing required argument: task_id

# Already deleted
$ todo delete 2
Task #2 deleted

$ todo delete 2
Error: Task 2 not found
```

## ID Persistence Behavior

```bash
# Start with 3 tasks
$ todo add "Task 1"
Task #1 added: Task 1

$ todo add "Task 2"
Task #2 added: Task 2

$ todo add "Task 3"
Task #3 added: Task 3

# Delete middle task
$ todo delete 2
Task #2 deleted

# Add new task - ID is 4, not 2
$ todo add "Task 4"
Task #4 added: Task 4

# Current state: IDs are 1, 3, 4 (not 1, 2, 3)
$ todo view
TODO LIST (3 tasks)

[1] ○ Task 1
    Status: pending

[3] ○ Task 3
    Status: pending

[4] ○ Task 4
    Status: pending
```

This behavior prevents confusion and potential errors from ID reuse.

## Implementation Notes

- Uses Typer for CLI parsing
- task_id is positional required integer argument
- --force flag is placeholder for future confirmation feature
- Delegates to `TodoList.delete_task(task_id)`
- Catches TaskNotFoundError and outputs to stderr
- No undo mechanism in Phase I

## Service Layer Call

```python
# src/cli/commands.py
def delete_command(task_id: int, force: bool = False):
    try:
        todo_list.delete_task(task_id)
        print(f"Task #{task_id} deleted")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Error: Invalid task ID: must be a positive integer", file=sys.stderr)
        sys.exit(1)
```

## Acceptance Criteria

From User Story 4:
- ✓ Task removed from list when deleted
- ✓ Empty list shows appropriate message after deleting last task
- ✓ Clear error for non-existent task ID
- ✓ Other tasks remain unaffected and retain their IDs
- ✓ Deleted IDs are not reused

## Related Requirements

- FR-007: System MUST allow users to delete tasks by ID
- FR-010: System MUST provide clear error messages
- FR-011: System MUST handle empty lists gracefully
- FR-013: System MUST output to stdout, errors to stderr

## Future Enhancements (Out of Scope for Phase I)

1. **Confirmation Prompt**:
   ```bash
   $ todo delete 1
   Delete task #1: "Buy groceries"? [y/N]: y
   Task #1 deleted
   ```

2. **Soft Delete**:
   - Mark as deleted instead of removing
   - Add `todo restore <id>` command
   - Requires additional status: "deleted"

3. **Bulk Delete**:
   ```bash
   $ todo delete 1 2 3
   3 tasks deleted
   ```

These are NOT implemented in Phase I per constitution (in-memory, simple operations only).
