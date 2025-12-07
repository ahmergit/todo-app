"""Task management business logic"""
from todo.models import Task, Priority


class TaskManager:
    """
    Manages task lifecycle and maintains task collection integrity.
    
    All task operations (create, read, update, delete) go through this manager.
    Tasks are stored in-memory and lost when the application exits.
    """

    def __init__(self):
        """Initialize TaskManager with empty task list"""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        """
        Create and add a new task to the task list.

        Args:
            description: Task description (1-500 chars, required)
            priority: Task priority (optional, defaults to MEDIUM)

        Returns:
            The newly created task with assigned ID

        Raises:
            ValueError: If description is empty or >500 characters
            TypeError: If description is not a string or priority is not Priority enum
        """
        task = Task(
            id=self._next_id,
            description=description,
            priority=priority
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        """
        Retrieve a task by its unique ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task if found, None otherwise
        """
        return next((t for t in self._tasks if t.id == task_id), None)

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in creation order.

        Returns:
            List of all tasks (may be empty)
        """
        return self._tasks.copy()

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update the description of an existing task.

        Args:
            task_id: ID of task to update
            new_description: New description (1-500 chars)

        Returns:
            True if task found and updated, False otherwise

        Raises:
            ValueError: If new_description is empty or >500 characters
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Validate new description
        description = new_description.strip()
        if not description:
            raise ValueError("Description cannot be empty")
        if len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")

        # Update the task description
        # Note: We need to recreate the task with validation
        task_index = self._tasks.index(task)
        updated_task = Task(
            id=task.id,
            description=new_description,
            priority=task.priority,
            completed=task.completed,
            created_at=task.created_at
        )
        self._tasks[task_index] = updated_task
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the task list.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task found and deleted, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of task to toggle

        Returns:
            True if task found and toggled, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Recreate task with toggled completion status
        task_index = self._tasks.index(task)
        updated_task = Task(
            id=task.id,
            description=task.description,
            priority=task.priority,
            completed=not task.completed,
            created_at=task.created_at
        )
        self._tasks[task_index] = updated_task
        return True

    def set_priority(self, task_id: int, priority: Priority) -> bool:
        """
        Set the priority of an existing task.

        Args:
            task_id: ID of task to update
            priority: New priority level

        Returns:
            True if task found and priority updated, False otherwise

        Raises:
            TypeError: If priority is not a Priority enum value
        """
        if not isinstance(priority, Priority):
            raise TypeError("Priority must be a Priority enum value")

        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Recreate task with new priority
        task_index = self._tasks.index(task)
        updated_task = Task(
            id=task.id,
            description=task.description,
            priority=priority,
            completed=task.completed,
            created_at=task.created_at
        )
        self._tasks[task_index] = updated_task
        return True
