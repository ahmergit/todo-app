---
id: 0003
title: CLI todo app implementation plan
stage: plan
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-cli-todo-app
branch: 001-cli-todo-app
user: user
command: /sp.plan
labels: ["planning", "architecture", "tdd", "clean-architecture", "in-memory"]
links:
  spec: specs/001-cli-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo-app/plan.md
  - specs/001-cli-todo-app/research.md
  - specs/001-cli-todo-app/data-model.md
  - specs/001-cli-todo-app/contracts/task_manager_interface.md
  - specs/001-cli-todo-app/quickstart.md
  - CLAUDE.md (agent context updated)
tests:
  - N/A (planning phase - tests designed but not yet written)
---

## Prompt

Use Python 3.13+ and initialize the project using UV with a standard package layout under src/todo/.

Define a Task dataclass in models.py with fields: id, title, description, priority, completed, and created_at.

Implement a TaskManager in manager.py to store tasks in memory using a Python list with methods for add, view, update, delete, and toggle-complete.

Build a UI layer in ui.py responsible only for displaying menus, reading user input, and calling TaskManager functions.

Create main.py as the application entry point running a numbered interactive menu loop that routes actions to the UI layer.

Enforce strict input validation in UI functions (menu choice, task ID, title lengths, priority selection).

Apply TDD with pytest: write tests for Task model, TaskManager logic, and UI helper functions before implementation.

Keep all storage in-memory only, no external dependencies, no database, and no persistence layer.

Follow clean architecture principles: UI → Manager → Model, with no circular imports and clear separation of concerns.

Document full setup and run instructions in README.md, including how to run via uv run todo.main.

## Response snapshot

Completed comprehensive implementation plan for CLI Todo Application with full Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts.

**Technical Context Established**:
- Language: Python 3.13+
- Dependencies: None (standard library only; pytest for dev/test)
- Storage: In-memory Python list
- Testing: pytest with TDD (Red-Green-Refactor)
- Platform: Cross-platform CLI
- Performance: <100ms for 1000 tasks
- Project Type: Single package (src/todo/)

**Constitution Check** (all principles ✅ PASS):
1. Spec-Driven Development: Complete spec with 5 user stories, 20 FRs
2. Test-First Development: TDD workflow mandated with pytest
3. Environment Management: uv + Python 3.13+ specified
4. Clean Code Practices: Clear separation (UI→Manager→Model)
5. Modular Architecture: 4 modules with unidirectional dependencies
6. Lightweight Design: Zero runtime dependencies

**Phase 0: Research** (research.md created):
- Dataclass pattern for Task model
- In-memory list storage with linear search (O(n) acceptable for n≤1000)
- ANSI escape codes for terminal colors (green for completed tasks)
- UI-layer input validation strategy
- uv project setup with pyproject.toml
- pytest TDD workflow with fixtures and parametrize
- Main menu loop pattern with exception handling

**Phase 1: Design & Contracts** (artifacts created):

1. **data-model.md**: Complete entity definitions
   - Task entity with 5 attributes (id, description, priority, completed, created_at)
   - Priority enum (HIGH, MEDIUM, LOW)
   - TaskList collection with 7 invariants
   - State machines for completion and priority transitions
   - Validation rules mapped to FR requirements
   - Performance analysis (O(n) operations justified)

2. **contracts/task_manager_interface.md**: TaskManager contract
   - 8 public methods with preconditions, postconditions, side effects
   - 7 critical invariants (ID uniqueness, sequence, positivity, etc.)
   - Performance guarantees (<100ms for all operations at n=1000)
   - Error handling philosophy (exceptions vs return values)
   - Contract test requirements

3. **quickstart.md**: Complete development guide
   - Prerequisites and verification steps
   - uv project setup (init, structure, configuration)
   - TDD workflow (Red-Green-Refactor detailed examples)
   - Running application (`uv run todo`)
   - Testing strategies (unit/integration/contract)
   - Debugging techniques
   - Common issues and solutions

**Project Structure Defined**:
```
src/todo/
├── models.py (Task dataclass, Priority enum)
├── manager.py (TaskManager business logic)
├── ui.py (UI layer with menu/input/formatting)
└── main.py (Entry point with menu loop)

tests/
├── unit/ (fast, isolated tests)
├── integration/ (end-to-end workflows)
└── contract/ (interface verification)
```

**Agent Context Updated**: CLAUDE.md now includes Python 3.13+ and in-memory storage technology.

## Outcome

- ✅ Impact: Complete technical plan ready for implementation; all research resolved, architecture designed, contracts defined, TDD workflow documented
- 🧪 Tests: Test strategy defined across 3 levels (unit/integration/contract); test examples provided; TDD workflow fully documented
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/task_manager_interface.md, quickstart.md; updated CLAUDE.md
- 🔁 Next prompts: `/sp.tasks` to generate actionable task list from plan, then begin TDD implementation
- 🧠 Reflection: Plan successfully satisfies all constitution principles with zero violations. Clean architecture (UI→Manager→Model) ensures testability and maintainability. In-memory storage with standard library only achieves lightweight design goal. TDD workflow integrated throughout documentation ensures test-first discipline.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All constitution gates passed; all technical decisions researched and justified; complete contract definitions; comprehensive quickstart guide
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor if linear search O(n) performance remains acceptable during implementation; consider dict-based lookup if <100ms SLA at risk
