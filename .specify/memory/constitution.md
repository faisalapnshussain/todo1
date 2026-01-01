<!--
Sync Impact Report:
- Version change: 0.0.0 (initial) → 1.0.0
- New constitution created for CLI Todo List (In-Memory)
- Principles defined: 5 core principles
- Sections added: Core Principles, Code Quality Standards, Development Workflow, Governance
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (reviewed - compatible)
  ✅ .specify/templates/spec-template.md (reviewed - compatible)
  ✅ .specify/templates/tasks-template.md (reviewed - compatible)
- Follow-up TODOs: None - all placeholders filled
-->

# CLI Todo List (In-Memory) Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All features begin with a specification that defines user scenarios, requirements, and success criteria. Implementation follows a structured workflow: specification → planning → task breakdown → implementation. No code is written before the spec is approved and tasks are defined. This ensures accuracy and alignment with user intent throughout development.

**Rationale**: Prevents scope creep, ensures features solve real problems, maintains traceability from requirement to implementation.

### II. In-Memory Storage Only (Phase I Constraint)

All data MUST be stored in memory using Python data structures (lists, dictionaries, etc.). No file persistence, database connections, or external storage mechanisms are permitted in Phase I. Data lifecycle is bound to application runtime—data is lost when the application terminates.

**Rationale**: Simplifies initial implementation, focuses on core todo management logic, establishes foundation before adding persistence complexity in future phases.

### III. CLI-First Interface

The application MUST provide a command-line interface for all operations. Input is accepted via command-line arguments and/or interactive prompts. Output is written to stdout in human-readable format. Errors are written to stderr. The interface must be intuitive for developers familiar with standard CLI tools.

**Rationale**: Aligns with console app objective, provides straightforward testing surface, enables easy automation and scripting.

### IV. Modular Feature Design

Each core feature (Add, Delete, Update, View, Mark Complete) MUST be implemented as a separate, self-contained module with clear responsibilities. Modules expose well-defined interfaces and avoid tight coupling. Shared logic is factored into utility modules when reuse justifies abstraction.

**Rationale**: Improves maintainability, enables parallel development, simplifies testing, supports future extensibility.

### V. Clean Code & Python Standards

All code MUST follow Python 3.13+ standards and PEP 8 style guidelines. Code must be readable, well-structured, and maintainable. Functions have clear names and single responsibilities. Magic numbers and unclear logic are documented with comments. Type hints are encouraged for function signatures.

**Rationale**: Ensures codebase quality, reduces technical debt, makes code accessible to Python developers, facilitates code review.

## Code Quality Standards

**Testing Discipline**:
- Manual testing required for all features before considering them complete
- Test cases must validate happy path and edge cases (empty lists, invalid IDs, etc.)
- Each feature module should be testable independently

**Performance Expectations**:
- Operations on todo list (add, delete, view, update, mark complete) should be near-instantaneous for lists under 1000 items
- No performance optimization needed for in-memory operations at expected scale (< 100 items typical use)

**Security Considerations**:
- Input validation required for all user inputs (prevent crashes from malformed input)
- No security vulnerabilities from command injection or code execution through user input
- No sensitive data handling in Phase I (todos are plain text, no authentication)

## Development Workflow

**Structured Implementation Process**:
1. Feature specification created and approved (`/sp.specify`)
2. Implementation plan designed (`/sp.plan`)
3. Tasks generated and ordered (`/sp.tasks`)
4. Implementation executed task-by-task (`/sp.implement`)
5. Manual validation against acceptance criteria
6. Commit work with descriptive messages (`/sp.git.commit_pr`)

**Directory Structure** (enforced):
```
/src                    # All application code
  /models               # Data structures (Todo, TodoList)
  /services             # Business logic (todo operations)
  /cli                  # CLI interface and command parsing
  /utils                # Shared utilities

/specs                  # Feature specifications and design documents
  /<feature-name>/      # Per-feature directory
    spec.md             # Feature specification
    plan.md             # Implementation plan
    tasks.md            # Task breakdown

/history                # Development artifacts
  /prompts/             # Prompt History Records (PHRs)
    /constitution/      # Constitution-related prompts
    /general/           # General development prompts
    /<feature-name>/    # Feature-specific prompts
  /adr/                 # Architecture Decision Records

README.md               # Project overview and usage
CLAUDE.md               # AI assistant instructions
```

**Commit Standards**:
- Commit after completing each logical task
- Commit messages follow conventional format: `type(scope): description`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
- Example: `feat(cli): add task deletion command`

**Prompt History Recording**:
- Every user interaction that produces work MUST generate a Prompt History Record (PHR)
- PHRs capture: user input (verbatim), assistant response, files modified, stage, outcome
- PHRs routed to: `history/prompts/constitution/`, `history/prompts/<feature>/`, or `history/prompts/general/`
- PHR creation uses `.specify/templates/phr-template.prompt.md` template

## Governance

This constitution supersedes all other development practices and conventions for the CLI Todo List project. All features, design decisions, and code must comply with these principles.

**Amendment Process**:
- Amendments require explicit user approval
- Version incremented per semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes to principles or removing established rules
- MINOR: Adding new principles or materially expanding guidance
- PATCH: Clarifications, wording improvements, non-semantic fixes
- Amendment impact documented in Sync Impact Report at file top
- Dependent templates (.specify/templates/*.md) reviewed for consistency after amendments

**Compliance Verification**:
- All specifications must reference relevant constitutional principles
- Code reviews verify adherence to modular design and clean code standards
- No persistence layer implementation permitted in Phase I
- CLI interface requirements verified before feature considered complete

**Architectural Decision Records**:
- Significant architectural decisions should be documented as ADRs in `history/adr/`
- ADR suggestion triggered when decisions meet criteria: long-term impact, multiple alternatives, cross-cutting scope
- ADRs are never auto-created; require user consent via `/sp.adr` command
- Example decisions warranting ADRs: data structure choices, CLI framework selection, error handling strategy

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
