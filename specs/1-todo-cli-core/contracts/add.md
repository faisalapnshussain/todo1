# Command Contract: Add Task

**Command**: `todo add`
**Purpose**: Create a new task with title and optional description
**Maps to**: FR-001 (allow users to add task), User Story 1 (Add and View Tasks)

## Command Syntax

```bash
todo add <title> [--description <text>]
todo add <title> [-d <text>]
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| title | str | Yes | - | Task title (positional argument) |
| --description, -d | str | No | None | Task description (optional flag) |

## Input Validation

1. **Title**:
   - Must not be empty after stripping whitespace
   - Minimum length: 1 character (post-strip)
   - Special characters allowed
   - Quotes preserved in title text

2. **Description**:
   - Optional, can be omitted
   - If provided, can be empty string
   - Special characters allowed
   - Multi-line text supported (quote handling per shell)

## Output

### Success Case

**Format**:
```
Task #{id} added: {title}
```

**Example**:
```bash
$ todo add "Buy groceries"
Task #1 added: Buy groceries

$ todo add "Write plan" --description "Phase I implementation"
Task #2 added: Write plan
```

**Output Channel**: stdout
**Exit Code**: 0

### Error Cases

| Error Condition | Error Message | Output Channel | Exit Code |
|----------------|---------------|----------------|-----------|
| Empty title | `Error: Title cannot be empty` | stderr | 1 |
| Missing title argument | `Error: Missing required argument: title` | stderr | 1 |

## Behavior

1. Validates title is not empty
2. Creates Task object with auto-assigned ID
3. Adds task to TodoList
4. Prints confirmation to stdout
5. Returns exit code 0

## Examples

### Basic Usage

```bash
# Simple task
$ todo add "Call dentist"
Task #1 added: Call dentist

# Task with description
$ todo add "Deploy feature" -d "Deploy to staging environment first"
Task #2 added: Deploy feature

# Task with special characters
$ todo add "Research ML/AI frameworks"
Task #3 added: Research ML/AI frameworks
```

### Error Cases

```bash
# Empty title
$ todo add ""
Error: Title cannot be empty

# Missing title
$ todo add
Error: Missing required argument: title
```

## Implementation Notes

- Uses Typer for CLI parsing
- Title is positional required argument
- Description is optional flag (--description or -d)
- Delegates to `TodoList.add_task(title, description)`
- Catches ValidationError and outputs to stderr

## Service Layer Call

```python
# src/cli/commands.py
def add_command(title: str, description: Optional[str] = None):
    try:
        task = todo_list.add_task(title, description)
        print(f"Task #{task.id} added: {task.title}")
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

## Acceptance Criteria

From User Story 1:
- ✓ Task created with unique ID
- ✓ Task has status "pending" by default
- ✓ Title is stored correctly
- ✓ Description is stored correctly (if provided)
- ✓ Confirmation message displays ID and title

## Related Requirements

- FR-001: System MUST allow users to add task with title and optional description
- FR-002: System MUST assign unique numeric ID automatically
- FR-009: System MUST validate title is not empty
- FR-010: System MUST provide clear error messages
- FR-013: System MUST output to stdout, errors to stderr
