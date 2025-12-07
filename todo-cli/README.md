# CLI Todo Application

A simple in-memory command-line todo application built with Python 3.13+.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete
- Set task priorities (High, Medium, Low)
- Interactive console menu
- Color-coded task display (green for completed tasks)

## Requirements

- Python 3.13 or higher
- uv (package manager)

## Installation

```bash
# Install dependencies
uv add --dev pytest

# Run the application
uv run todo
```

## Usage

Launch the application and follow the interactive menu prompts to manage your tasks.

## Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_models.py
```

## Development

This project follows Test-Driven Development (TDD) principles:
1. Write tests first (Red phase)
2. Implement minimal code to pass tests (Green phase)
3. Refactor while keeping tests green (Refactor phase)

## Architecture

- **Models** (`src/todo/models.py`): Task dataclass and Priority enum
- **Manager** (`src/todo/manager.py`): Business logic for task management
- **UI** (`src/todo/ui.py`): User interface layer
- **Main** (`src/todo/main.py`): Application entry point

## License

This is a personal project for learning purposes.
