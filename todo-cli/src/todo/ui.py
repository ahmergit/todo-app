"""User interface layer for the todo application"""
from todo.models import Task, Priority
from todo.manager import TaskManager


def display_menu():
    """Display the main menu options"""
    print()
    print("=" * 40)
    print("   TODO LIST APPLICATION")
    print("=" * 40)
    print()
    print("Main Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Complete Task")
    print("6. Set Priority")
    print("0. Exit")
    print()


def get_menu_choice() -> str:
    """Get and validate menu choice from user"""
    while True:
        choice = input("Enter choice: ").strip().lower()
        if choice in ['q', 'quit', 'exit']:
            return '0'
        if choice in ['0', '1', '2', '3', '4', '5', '6']:
            return choice
        print("Invalid choice. Please enter a number from 0-6.")


def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate task description.

    Args:
        description: Description to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    description = description.strip()
    if not description:
        return False, "Description cannot be empty"
    if len(description) > 500:
        return False, "Description cannot exceed 500 characters"
    return True, ""


def validate_priority_input(priority_input: str) -> tuple[Priority | None, str]:
    """
    Validate and convert priority input.

    Args:
        priority_input: User input for priority ('H', 'M', 'L' or empty for default)

    Returns:
        Tuple of (Priority or None, error_message)
    """
    priority_input = priority_input.strip().upper()

    if not priority_input:
        return Priority.MEDIUM, ""

    if priority_input == 'H':
        return Priority.HIGH, ""
    elif priority_input == 'M':
        return Priority.MEDIUM, ""
    elif priority_input == 'L':
        return Priority.LOW, ""
    else:
        return None, "Priority must be H (High), M (Medium), or L (Low)"


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RESET = '\033[0m'

    @staticmethod
    def green(text: str) -> str:
        """Return text with green color if terminal supports it"""
        import os
        import sys
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and os.getenv('TERM') != 'dumb':
            return f"{Colors.GREEN}{text}{Colors.RESET}"
        return text


def format_task_display(task: Task) -> str:
    """
    Format a task for display.

    Args:
        task: Task to format

    Returns:
        Formatted string representation of the task
    """
    # Format priority
    priority_str = task.priority.value

    # Format status with color for completed tasks
    if task.completed:
        status = Colors.green("✓ COMPLETE")
    else:
        status = "○ Incomplete"

    # Format full display
    display = f"[{task.id}] {task.description}"
    display += f"\n    Priority: {priority_str} | Status: {status}"

    return display


def handle_add_task(manager: TaskManager):
    """Handle adding a new task"""
    print("\n--- Add New Task ---")

    # Get description
    description = input("Enter task description: ").strip()
    is_valid, error = validate_description(description)
    if not is_valid:
        print(f"Error: {error}")
        return

    # Get priority (optional)
    priority_input = input("Enter priority [H/M/L] or press Enter for Medium: ").strip()
    priority, error = validate_priority_input(priority_input)
    if priority is None:
        print(f"Error: {error}")
        return

    # Add task
    task = manager.add_task(description, priority)
    print(f"\n✓ Task added successfully! (ID: {task.id})")


def handle_view_tasks(manager: TaskManager):
    """Handle viewing all tasks"""
    print("\n--- All Tasks ---")

    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks found. Add a task to get started!")
        return

    for task in tasks:
        print(f"\n{format_task_display(task)}")

    print(f"\nTotal: {len(tasks)} task(s)")


def handle_update_task(manager: TaskManager):
    """Handle updating a task description"""
    print("\n--- Update Task ---")

    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks to update.")
        return

    # Show tasks for reference
    for task in tasks:
        print(f"  [{task.id}] {task.description}")

    # Get task ID
    task_id_input = input("\nEnter task ID to update: ").strip()
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    # Check if task exists
    task = manager.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Get new description
    print(f"Current description: {task.description}")
    new_description = input("Enter new description: ").strip()
    is_valid, error = validate_description(new_description)
    if not is_valid:
        print(f"Error: {error}")
        return

    # Update task
    try:
        if manager.update_task(task_id, new_description):
            print(f"\n✓ Task {task_id} updated successfully!")
        else:
            print(f"Error: Failed to update task {task_id}.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete_task(manager: TaskManager):
    """Handle deleting a task"""
    print("\n--- Delete Task ---")

    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks to delete.")
        return

    # Show tasks for reference
    for task in tasks:
        print(f"  [{task.id}] {task.description}")

    # Get task ID
    task_id_input = input("\nEnter task ID to delete: ").strip()
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    # Check if task exists
    task = manager.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Confirm deletion
    confirm = input(f"Delete task '{task.description}'? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return

    # Delete task
    if manager.delete_task(task_id):
        print(f"\n✓ Task {task_id} deleted successfully!")
    else:
        print(f"Error: Failed to delete task {task_id}.")


def handle_complete_task(manager: TaskManager):
    """Handle marking a task as complete/incomplete"""
    print("\n--- Complete Task ---")

    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks to complete.")
        return

    # Show tasks for reference
    for task in tasks:
        status = "✓" if task.completed else "○"
        print(f"  [{task.id}] {status} {task.description}")

    # Get task ID
    task_id_input = input("\nEnter task ID to toggle complete: ").strip()
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    # Check if task exists
    task = manager.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Toggle completion
    if manager.toggle_complete(task_id):
        new_status = "complete" if not task.completed else "incomplete"
        print(f"\n✓ Task {task_id} marked as {new_status}!")
    else:
        print(f"Error: Failed to update task {task_id}.")


def handle_set_priority(manager: TaskManager):
    """Handle setting task priority"""
    print("\n--- Set Priority ---")

    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks to update.")
        return

    # Show tasks for reference
    for task in tasks:
        print(f"  [{task.id}] {task.description} (Priority: {task.priority.value})")

    # Get task ID
    task_id_input = input("\nEnter task ID to set priority: ").strip()
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    # Check if task exists
    task = manager.get_task_by_id(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Get new priority
    print(f"Current priority: {task.priority.value}")
    priority_input = input("Enter new priority [H/M/L]: ").strip()
    priority, error = validate_priority_input(priority_input)
    if priority is None:
        print(f"Error: {error}")
        return

    # Set priority
    if manager.set_priority(task_id, priority):
        print(f"\n✓ Task {task_id} priority set to {priority.value}!")
    else:
        print(f"Error: Failed to update task {task_id}.")
