# Research: CLI Todo Application

**Feature**: 001-cli-todo-app
**Phase**: 0 (Outline & Research)
**Date**: 2025-12-05

## Purpose

Resolve technical unknowns and establish best practices for implementing an in-memory CLI todo application using Python 3.13+, uv, and pytest with TDD methodology.

## Research Areas

### 1. Python Dataclasses for Task Model

**Decision**: Use `@dataclass` decorator from Python standard library for Task model

**Rationale**:
- Built-in to Python 3.7+ (well-established in 3.13+)
- Automatic generation of `__init__`, `__repr__`, `__eq__` methods
- Type hints support for field validation
- Immutable option via `frozen=True` if needed
- No external dependencies required
- Excellent IDE support and introspection

**Alternatives Considered**:
- **NamedTuple**: Considered but rejected - immutable by default, less flexible for methods
- **attrs library**: Considered but rejected - external dependency conflicts with zero-dependency requirement
- **Pydantic**: Considered but rejected - heavy external dependency, overkill for simple in-memory app
- **Plain class**: Considered but rejected - requires boilerplate code that dataclass eliminates

**Implementation Pattern**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class Task:
    id: int
    description: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

---

### 2. In-Memory Storage Pattern

**Decision**: Use Python list with linear search for simplicity and compliance with requirements

**Rationale**:
- Specification requires "no database, no persistence, in-memory only"
- Performance requirement: <100ms for up to 1000 tasks
- Linear search O(n) is acceptable for n ≤ 1000
- Standard library only - no external data structures
- Simple, testable, and maintainable

**Alternatives Considered**:
- **Dictionary (dict) by ID**: Considered but rejected - O(1) lookup overkill for small scale; list maintains insertion order naturally
- **OrderedDict**: Considered but rejected - unnecessary complexity; regular dict maintains insertion order in Python 3.7+
- **sqlite3 (in-memory mode)**: Considered but rejected - conflicts with "no database" requirement; adds complexity
- **Collections.deque**: Considered but rejected - no advantage over list for this use case

**Implementation Pattern**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        task = Task(id=self._next_id, description=description, priority=priority)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)
```

---

### 3. Console Color Output

**Decision**: Use ANSI escape codes via standard library (no external dependencies)

**Rationale**:
- Clarification session specified green text for completed tasks
- ANSI codes work across Unix/Linux/macOS terminals
- Windows 10+ supports ANSI codes in modern terminals
- Standard library only (no colorama/rich/click dependencies)
- Fallback: plain text if ANSI not supported

**Alternatives Considered**:
- **colorama library**: Considered but rejected - external dependency
- **rich library**: Considered but rejected - external dependency, heavy
- **termcolor library**: Considered but rejected - external dependency
- **No colors**: Considered but rejected - specification explicitly requires visual distinction via color

**Implementation Pattern**:
```python
class Colors:
    GREEN = '\033[92m'
    RESET = '\033[0m'

    @staticmethod
    def is_supported() -> bool:
        """Check if terminal supports ANSI colors"""
        import os
        import sys
        return (
            hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
            and os.getenv('TERM') != 'dumb'
        )

    @staticmethod
    def green(text: str) -> str:
        if Colors.is_supported():
            return f"{Colors.GREEN}{text}{Colors.RESET}"
        return text
```

---

### 4. Input Validation Strategy

**Decision**: Implement validation at UI layer with explicit error messages

**Rationale**:
- Separation of concerns: UI handles user interaction, Manager handles business logic
- FR-017 requires "clear error messages for all invalid inputs"
- Prevents invalid data from reaching business logic layer
- Testable validation functions in UI module

**Validation Rules** (from spec):
- Task description: 1-500 characters, non-empty after stripping whitespace (FR-011, FR-020)
- Task ID: positive integer, must exist in task list (FR-012)
- Priority: Must be H/M/L or valid Priority enum value
- Menu choice: Must be valid menu option number or exit command

**Implementation Pattern**:
```python
def validate_description(description: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)"""
    description = description.strip()
    if not description:
        return False, "Description cannot be empty"
    if len(description) > 500:
        return False, "Description cannot exceed 500 characters"
    return True, ""

def validate_task_id(task_id_input: str, manager: TaskManager) -> tuple[int | None, str]:
    """Returns (task_id, error_message)"""
    try:
        task_id = int(task_id_input)
        if task_id <= 0:
            return None, "Task ID must be a positive number"
        if manager.get_task_by_id(task_id) is None:
            return None, f"Task ID {task_id} not found"
        return task_id, ""
    except ValueError:
        return None, "Task ID must be a number"
```

---

### 5. uv Project Setup Best Practices

**Decision**: Use pyproject.toml with src/ layout and uv as package manager

**Rationale**:
- Constitution requires uv for environment management
- pyproject.toml is PEP 518/621 standard for Python projects
- src/ layout prevents accidental imports from project root
- Enables `uv run todo.main` as entry point

**Configuration**:
```toml
[project]
name = "todo"
version = "0.1.0"
description = "In-memory CLI todo application"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0"]

[project.scripts]
todo = "todo.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**Setup Commands**:
```bash
uv init --lib --package todo
uv add --dev pytest
uv run pytest
uv run todo
```

---

### 6. TDD Workflow with pytest

**Decision**: Follow strict Red-Green-Refactor with pytest fixtures and parametrize

**Rationale**:
- Constitution mandates test-first (NON-NEGOTIABLE)
- pytest provides excellent fixture support for test isolation
- Parametrize reduces code duplication for multiple test cases
- Clear test organization (unit/integration/contract)

**Test Structure**:
```python
# tests/unit/test_manager.py
import pytest
from todo.models import Task, Priority
from todo.manager import TaskManager

@pytest.fixture
def manager():
    """Fresh TaskManager for each test"""
    return TaskManager()

def test_add_task_creates_task_with_incremented_id(manager):
    # Red: Write failing test
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    assert task1.id == 1
    assert task2.id == 2

@pytest.mark.parametrize("description,priority", [
    ("High priority task", Priority.HIGH),
    ("Medium priority task", Priority.MEDIUM),
    ("Low priority task", Priority.LOW),
])
def test_add_task_with_priority(manager, description, priority):
    task = manager.add_task(description, priority)
    assert task.priority == priority
```

---

### 7. Menu Loop Pattern

**Decision**: Infinite loop with exception handling and graceful exit

**Rationale**:
- FR-016: Return to main menu after each action
- FR-018: Allow clean exit from main menu
- Exception handling prevents crashes on unexpected input

**Implementation Pattern**:
```python
def main():
    manager = TaskManager()

    while True:
        try:
            display_menu()
            choice = input("Enter choice: ").strip()

            if choice in ['0', 'q', 'quit', 'exit']:
                print("Goodbye!")
                break

            handle_menu_choice(choice, manager)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            # Continue loop - don't crash
```

---

## Summary

All technical decisions resolved using Python 3.13+ standard library only (zero runtime dependencies). Architecture follows clean separation (UI → Manager → Model), satisfies all constitution principles, and supports TDD workflow with pytest. Implementation patterns identified for:

1. Task model using dataclass
2. In-memory list storage with linear search
3. ANSI color codes for terminal output
4. UI-layer input validation
5. uv project configuration
6. pytest test structure
7. Main menu loop pattern

**Next Phase**: Phase 1 (Design & Contracts) - Generate data-model.md and API contracts
