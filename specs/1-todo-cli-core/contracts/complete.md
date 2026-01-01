# Command Contract: Mark Complete

**Command**: `todo complete`
**Purpose**: Toggle task status between pending and complete
**Maps to**: FR-005 (mark tasks complete/pending), User Story 2 (Mark Tasks Complete)

## Command Syntax

```bash
todo complete <task_id>
todo complete <task_id> --undo
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | int | Yes | - | ID of task to mark complete/pending (positional) |
| --undo | flag | No | False | If present, mark as pending instead of complete |

## Input Validation

1. **Task ID**:
   - Must be a positive integer
   - Must exist in the task list
   - Type conversion: string → int

## Output

### Success Case

**Format**:
```
Task #{id} marked {status}
```

**Example**:
```bash
$ todo complete 1
Task #1 marked complete

$ todo complete 1 --undo
Task #1 marked pending
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
3. If --undo flag present: mark as pending
4. If --undo flag absent: mark as complete
5. Prints confirmation to stdout
6. Returns exit code 0

## Examples

### Basic Usage

```bash
# Mark task complete
$ todo complete 1
Task #1 marked complete

# Mark task pending (undo)
$ todo complete 1 --undo
Task #1 marked pending

# Complete another task
$ todo complete 3
Task #3 marked complete
```

### Error Cases

```bash
# Task doesn't exist
$ todo complete 999
Error: Task 999 not found

# Invalid ID format
$ todo complete abc
Error: Invalid task ID: must be a positive integer

# Missing ID
$ todo complete
Error: Missing required argument: task_id
```

## Toggle Behavior

The command supports toggling via --undo flag:

```bash
# Initial state: pending
$ todo view
[1] ○ Buy groceries
    Status: pending

# Mark complete
$ todo complete 1
Task #1 marked complete

$ todo view
[1] ✓ Buy groceries
    Status: complete

# Toggle back to pending
$ todo complete 1 --undo
Task #1 marked pending

$ todo view
[1] ○ Buy groceries
    Status: pending
```

## Implementation Notes

- Uses Typer for CLI parsing
- task_id is positional required integer argument
- --undo is optional boolean flag
- Delegates to `TodoList.mark_complete(task_id, complete=True/False)`
- Catches TaskNotFoundError and outputs to stderr

## Service Layer Call

```python
# src/cli/commands.py
def complete_command(task_id: int, undo: bool = False):
    try:
        complete = not undo
        task = todo_list.mark_complete(task_id, complete)
        status_word = "pending" if undo else "complete"
        print(f"Task #{task_id} marked {status_word}")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Error: Invalid task ID: must be a positive integer", file=sys.stderr)
        sys.exit(1)
```

## Acceptance Criteria

From User Story 2:
- ✓ Pending task changes to complete when marked
- ✓ Complete task changes to pending when unmarked
- ✓ Status change visible in view command
- ✓ Clear error for non-existent task ID

## Related Requirements

- FR-005: System MUST support marking tasks complete or pending by ID
- FR-008: System MUST display clear status indicators
- FR-010: System MUST provide clear error messages
- FR-013: System MUST output to stdout, errors to stderr

## Alternative Design (Not Implemented)

Could use separate commands:
- `todo complete <id>` - mark complete only
- `todo uncomplete <id>` - mark pending only

Decision: Single command with --undo flag is simpler and more intuitive for toggle behavior.
