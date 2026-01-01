# Command Contract: Update Task

**Command**: `todo update`
**Purpose**: Modify task title and/or description
**Maps to**: FR-006 (update task by ID), User Story 3 (Update Task Details)

## Command Syntax

```bash
todo update <task_id> --title <new_title>
todo update <task_id> --description <new_description>
todo update <task_id> -t <new_title> -d <new_description>
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| task_id | int | Yes | - | ID of task to update (positional) |
| --title, -t | str | No* | None | New task title |
| --description, -d | str | No* | None | New task description (empty string clears it) |

**At least one of --title or --description must be provided.*

## Input Validation

1. **Task ID**:
   - Must be a positive integer
   - Must exist in the task list
   - Type conversion: string → int

2. **Title** (if provided):
   - Must not be empty after stripping whitespace
   - Minimum length: 1 character (post-strip)

3. **Description** (if provided):
   - Can be any string including empty
   - Empty string clears the description
   - None (not provided) leaves description unchanged

4. **At Least One Field**:
   - Error if neither --title nor --description provided
   - Valid to provide just one or both

## Output

### Success Case

**Format**:
```
Task #{id} updated
```

**Example**:
```bash
$ todo update 1 --title "Buy groceries and supplies"
Task #1 updated

$ todo update 2 -t "Write detailed plan" -d "Include Phase II considerations"
Task #2 updated

$ todo update 3 --description "Updated description only"
Task #3 updated
```

**Output Channel**: stdout
**Exit Code**: 0

### Error Cases

| Error Condition | Error Message | Output Channel | Exit Code |
|----------------|---------------|----------------|-----------|
| Task not found | `Error: Task {id} not found` | stderr | 1 |
| Empty title | `Error: Title cannot be empty` | stderr | 1 |
| No fields provided | `Error: Must provide --title and/or --description` | stderr | 1 |
| Invalid ID format | `Error: Invalid task ID: must be a positive integer` | stderr | 1 |
| Missing ID argument | `Error: Missing required argument: task_id` | stderr | 1 |

## Behavior

1. Validates task_id is positive integer
2. Validates at least one of title or description is provided
3. Looks up task by ID (may raise TaskNotFoundError)
4. If title provided: validates not empty, updates task title
5. If description provided: updates task description (empty string clears)
6. Prints confirmation to stdout
7. Returns exit code 0

## Examples

### Update Title Only

```bash
$ todo view
[1] ○ Buy groceries
    Status: pending

$ todo update 1 --title "Buy groceries and milk"
Task #1 updated

$ todo view
[1] ○ Buy groceries and milk
    Status: pending
```

### Update Description Only

```bash
$ todo view
[2] ○ Write plan
    Status: pending

$ todo update 2 --description "Phase I implementation with UV setup"
Task #2 updated

$ todo view
[2] ○ Write plan
    Description: Phase I implementation with UV setup
    Status: pending
```

### Update Both Title and Description

```bash
$ todo update 3 -t "Review PRs" -d "Focus on security and performance"
Task #3 updated
```

### Clear Description

```bash
$ todo view
[2] ○ Write plan
    Description: Phase I implementation with UV setup
    Status: pending

$ todo update 2 --description ""
Task #2 updated

$ todo view
[2] ○ Write plan
    Status: pending
```

### Error Cases

```bash
# Task doesn't exist
$ todo update 999 --title "New title"
Error: Task 999 not found

# Empty title
$ todo update 1 --title ""
Error: Title cannot be empty

# No fields provided
$ todo update 1
Error: Must provide --title and/or --description

# Invalid ID
$ todo update abc --title "Test"
Error: Invalid task ID: must be a positive integer
```

## Implementation Notes

- Uses Typer for CLI parsing
- task_id is positional required integer argument
- --title and --description are optional string flags
- At least one flag must be provided (validated in command)
- Delegates to `TodoList.update_task(task_id, title, description)`
- Catches TaskNotFoundError and ValidationError, outputs to stderr

## Service Layer Call

```python
# src/cli/commands.py
def update_command(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
):
    if title is None and description is None:
        print("Error: Must provide --title and/or --description", file=sys.stderr)
        sys.exit(1)

    try:
        task = todo_list.update_task(task_id, title, description)
        print(f"Task #{task_id} updated")
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Error: Invalid task ID: must be a positive integer", file=sys.stderr)
        sys.exit(1)
```

## Acceptance Criteria

From User Story 3:
- ✓ Task title updates correctly when provided
- ✓ Task description updates correctly when provided
- ✓ Other attributes remain unchanged during update
- ✓ Can update title alone, description alone, or both
- ✓ Clear error for non-existent task ID
- ✓ Can clear description with empty string

## Related Requirements

- FR-006: System MUST allow users to update task title and/or description by ID
- FR-009: System MUST validate title is not empty
- FR-010: System MUST provide clear error messages
- FR-013: System MUST output to stdout, errors to stderr

## Design Note

Empty string for description clears it, while None (not provided) leaves it unchanged. This distinction allows:
- Update title only: `--title "new"` (description unchanged)
- Clear description: `--description ""` (description set to empty/None)
- Update both: `--title "new" --description "new desc"`
