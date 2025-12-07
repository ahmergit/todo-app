# Quickstart Guide: CLI Todo Application

**Feature**: 001-cli-todo-app
**Version**: 1.0.0
**Date**: 2025-12-05

## Purpose

This guide provides step-by-step instructions for setting up, developing, testing, and running the CLI todo application. Follows Test-Driven Development (TDD) workflow as mandated by the project constitution.

---

## Prerequisites

### Required
- **Python**: 3.13 or higher
- **uv**: Package and environment manager ([installation instructions](https://github.com/astral-sh/uv))
- **Git**: For version control
- **Terminal**: Command-line interface (cmd, PowerShell, bash, zsh, etc.)

### Verification
```bash
python --version  # Should show 3.13.x or higher
uv --version      # Should show uv version
git --version     # Should show git version
```

---

## Project Setup

### 1. Initialize Project with uv

```bash
# Navigate to project root
cd C:\phase1\todo-app

# Initialize Python project with uv
uv init --lib --package todo

# This creates:
# - pyproject.toml (project configuration)
# - src/todo/ (package directory)
# - .python-version (Python version specification)
```

### 2. Create Project Structure

```bash
# Create source directories
mkdir -p src/todo
touch src/todo/__init__.py
touch src/todo/models.py
touch src/todo/manager.py
touch src/todo/ui.py
touch src/todo/main.py

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/contract

# Create test files
touch tests/unit/test_models.py
touch tests/unit/test_manager.py
touch tests/unit/test_ui.py
touch tests/integration/test_app_flow.py
touch tests/contract/test_manager_contract.py

# Create configuration files
touch .gitignore
touch README.md
```

### 3. Configure pyproject.toml

Edit `pyproject.toml` with the following content:

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
addopts = "-v --tb=short"
```

### 4. Install Development Dependencies

```bash
# Add pytest for testing
uv add --dev pytest

# Verify installation
uv pip list
```

### 5. Configure .gitignore

Create `.gitignore` with:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
.venv/
venv/
ENV/
env/

# uv
.uv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Development Workflow (TDD)

### Phase 1: RED - Write Failing Tests

#### Step 1: Write Model Tests First

**File**: `tests/unit/test_models.py`

```python
import pytest
from datetime import datetime
from todo.models import Task, Priority

def test_task_creation_with_all_fields():
    """Test creating a task with all fields specified"""
    task = Task(
        id=1,
        description="Buy groceries",
        priority=Priority.HIGH,
        completed=False,
        created_at=datetime.now()
    )
    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.priority == Priority.HIGH
    assert task.completed == False

def test_task_default_values():
    """Test that task uses default values correctly"""
    task = Task(id=1, description="Test task")
    assert task.priority == Priority.MEDIUM
    assert task.completed == False
    assert isinstance(task.created_at, datetime)

def test_task_empty_description_raises_error():
    """Test that empty description raises ValueError"""
    with pytest.raises(ValueError, match="empty"):
        Task(id=1, description="")

# Add more tests...
```

**Run tests (they should FAIL)**:
```bash
uv run pytest tests/unit/test_models.py -v
```

Expected output: All tests fail because `todo.models` doesn't exist yet.

#### Step 2: Write Manager Tests

**File**: `tests/unit/test_manager.py`

```python
import pytest
from todo.models import Task, Priority
from todo.manager import TaskManager

@pytest.fixture
def manager():
    """Provide a fresh TaskManager for each test"""
    return TaskManager()

def test_add_task_creates_task_with_id(manager):
    """Test that adding a task assigns an ID"""
    task = manager.add_task("Buy groceries")
    assert task.id == 1

def test_add_multiple_tasks_increments_id(manager):
    """Test that IDs increment correctly"""
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    assert task1.id == 1
    assert task2.id == 2

def test_get_task_by_id_returns_task(manager):
    """Test retrieving a task by ID"""
    task = manager.add_task("Test task")
    retrieved = manager.get_task_by_id(task.id)
    assert retrieved is not None
    assert retrieved.description == "Test task"

# Add more tests...
```

**Run tests (they should FAIL)**:
```bash
uv run pytest tests/unit/test_manager.py -v
```

### Phase 2: GREEN - Implement Minimal Code

#### Step 1: Implement Task Model

**File**: `src/todo/models.py`

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

    def __post_init__(self):
        description = self.description.strip()
        if not description:
            raise ValueError("Description cannot be empty")
        if len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")
```

**Run tests (some should PASS)**:
```bash
uv run pytest tests/unit/test_models.py -v
```

#### Step 2: Implement TaskManager

**File**: `src/todo/manager.py`

```python
from todo.models import Task, Priority

class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        task = Task(
            id=self._next_id,
            description=description,
            priority=priority
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def get_all_tasks(self) -> list[Task]:
        return self._tasks.copy()

    # Implement other methods...
```

**Run tests (more should PASS)**:
```bash
uv run pytest tests/unit/test_manager.py -v
```

### Phase 3: REFACTOR - Clean Up Code

- Remove code duplication
- Improve naming
- Add docstrings
- Ensure tests still pass

```bash
uv run pytest -v
```

---

## Running the Application

### Development Mode

```bash
# Run from project root
uv run python -m todo.main

# Or use the configured script
uv run todo
```

### Expected Output

```
=================================
   TODO LIST APPLICATION
=================================

Main Menu:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Complete Task
6. Set Priority
0. Exit

Enter choice:
```

---

## Testing

### Run All Tests

```bash
# Run all tests with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=todo --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_models.py -v

# Run specific test function
uv run pytest tests/unit/test_models.py::test_task_creation_with_all_fields -v
```

### Test Organization

```
tests/
├── unit/            # Fast, isolated tests
│   ├── test_models.py       # Task dataclass tests
│   ├── test_manager.py      # TaskManager logic tests
│   └── test_ui.py           # UI helper function tests
├── integration/     # Slower, end-to-end tests
│   └── test_app_flow.py     # Complete user workflows
└── contract/        # Interface contract tests
    └── test_manager_contract.py  # TaskManager interface verification
```

### Test Execution Order

1. **Unit tests first** (fastest feedback)
2. **Contract tests** (interface verification)
3. **Integration tests** (end-to-end flows)

```bash
# Run in order
uv run pytest tests/unit/ -v
uv run pytest tests/contract/ -v
uv run pytest tests/integration/ -v
```

---

## Debugging

### Enable Debug Mode

```python
# In main.py, add debug flag
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    logger.debug("Application starting...")
    # ...
```

### pytest Debugging

```bash
# Stop on first failure
uv run pytest -x

# Show local variables on failure
uv run pytest -l

# Enter debugger on failure
uv run pytest --pdb
```

---

## Common Issues & Solutions

### Issue 1: Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'todo'`

**Solution**:
```bash
# Ensure you're running from project root
cd C:\phase1\todo-app

# Verify package structure
ls src/todo/__init__.py  # Should exist

# Use uv run
uv run pytest  # Not just 'pytest'
```

### Issue 2: Tests Not Found

**Symptom**: `no tests ran in X seconds`

**Solution**:
```bash
# Check test file naming (must start with test_)
ls tests/unit/test_*.py

# Verify pytest configuration in pyproject.toml
cat pyproject.toml | grep testpaths
```

### Issue 3: Python Version Mismatch

**Symptom**: `Python 3.13 or higher is required`

**Solution**:
```bash
# Check current Python version
python --version

# Set Python version for uv
uv python pin 3.13

# Verify .python-version file
cat .python-version
```

---

## Next Steps

### After Quickstart

1. **Complete TDD Cycle**:
   - Write tests for all TaskManager methods
   - Implement methods to make tests pass
   - Refactor for clarity

2. **Implement UI Layer**:
   - Write tests for UI helper functions (input validation, formatting)
   - Implement ui.py with menu display and input handling
   - Test with mock TaskManager

3. **Build Main Entry Point**:
   - Write integration tests for complete workflows
   - Implement main.py with menu loop
   - Test full application flow

4. **Add Features**:
   - Follow User Story priorities (P1 → P2 → P3 → P4)
   - Each feature: tests first, then implementation

### Continuous Practices

- **Commit often**: After each passing test or working feature
- **Run tests continuously**: Before every commit
- **Refactor regularly**: Keep code clean as you go
- **Follow TDD**: Red → Green → Refactor (always)

---

## Resources

### Documentation
- **Feature Spec**: `specs/001-cli-todo-app/spec.md`
- **Data Model**: `specs/001-cli-todo-app/data-model.md`
- **Contracts**: `specs/001-cli-todo-app/contracts/`
- **Constitution**: `.specify/memory/constitution.md`

### Tools
- **uv Documentation**: https://github.com/astral-sh/uv
- **pytest Documentation**: https://docs.pytest.org/
- **Python Dataclasses**: https://docs.python.org/3/library/dataclasses.html

### Code Quality
```bash
# Run linter (if added)
uv run ruff check src/

# Format code (if added)
uv run ruff format src/
```

---

## Summary

This quickstart guide provides everything needed to set up, develop, test, and run the CLI todo application following TDD principles. The workflow emphasizes:

1. **Setup**: uv project initialization with proper structure
2. **TDD**: Write failing tests, implement minimal code, refactor
3. **Testing**: Comprehensive test suite (unit/integration/contract)
4. **Execution**: Run via `uv run todo`
5. **Debugging**: Tools and techniques for troubleshooting

Follow the Red-Green-Refactor cycle strictly, and ensure all tests pass before moving to the next feature.
