# CLI Todo Application

A simple in-memory command-line todo application built with Python 3.13+ using Test-Driven Development (TDD).

## Features

- ✅ Add tasks with optional priority
- ✅ View all tasks with status
- ✅ Update task descriptions
- ✅ Delete tasks with confirmation
- ✅ Mark tasks as complete/incomplete
- ✅ Set task priorities (High, Medium, Low)
- ✅ Interactive console menu
- ✅ Color-coded task display

## Requirements

- Python 3.13 or higher
- uv (package manager)

## Quick Start

```bash
# Navigate to the project
cd todo-cli

# Install dependencies
uv sync

# Run the application
uv run todo
```

## Usage

```
========================================
   TODO LIST APPLICATION
========================================

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

## Testing

```bash
cd todo-cli

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=todo
```

## Project Structure

```
todo-app/
├── README.md
├── MVP_COMPLETE.md
├── todo-cli/                 # Python application
│   ├── pyproject.toml
│   ├── src/todo/
│   │   ├── models.py         # Task dataclass, Priority enum
│   │   ├── manager.py        # Business logic
│   │   ├── ui.py             # User interface
│   │   └── main.py           # Entry point
│   └── tests/
│       ├── unit/             # Unit tests
│       └── integration/      # Integration tests
├── specs/                    # Specifications
└── history/                  # Development prompts
```

## Architecture

- **Models**: Task dataclass with Priority enum
- **Manager**: TaskManager with CRUD operations
- **UI**: Validation, formatting, and handlers
- **Main**: Application loop

## Development

This project follows TDD principles:
1. **Red**: Write failing tests first
2. **Green**: Implement minimal code to pass
3. **Refactor**: Clean up while keeping tests green

## Test Results

```
74 tests passed in < 1 second
- 64 unit tests
- 10 integration tests
```

## License

Personal learning project.
