"""Unit tests for TaskManager business logic"""
import pytest
from todo.models import Task, Priority
from todo.manager import TaskManager


class TestTaskManagerInit:
    """Tests for TaskManager initialization"""

    def test_manager_initializes_with_empty_task_list(self):
        """Test that TaskManager starts with no tasks"""
        manager = TaskManager()
        assert len(manager.get_all_tasks()) == 0

    def test_manager_initializes_with_id_starting_at_one(self):
        """Test that first task ID will be 1"""
        manager = TaskManager()
        task = manager.add_task("First task")
        assert task.id == 1


class TestTaskManagerAddTask:
    """Tests for adding tasks"""

    @pytest.fixture
    def manager(self):
        """Fresh TaskManager for each test"""
        return TaskManager()

    def test_add_task_returns_task_object(self, manager):
        """Test that add_task returns a Task instance"""
        task = manager.add_task("Buy groceries")
        assert isinstance(task, Task)

    def test_add_task_assigns_unique_id(self, manager):
        """Test that each task gets a unique ID"""
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_default_priority(self, manager):
        """Test that task gets MEDIUM priority by default"""
        task = manager.add_task("Test task")
        assert task.priority == Priority.MEDIUM

    def test_add_task_with_high_priority(self, manager):
        """Test that task can be created with HIGH priority"""
        task = manager.add_task("Urgent task", Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_add_task_with_low_priority(self, manager):
        """Test that task can be created with LOW priority"""
        task = manager.add_task("Low priority task", Priority.LOW)
        assert task.priority == Priority.LOW

    def test_add_task_defaults_to_incomplete(self, manager):
        """Test that new tasks are not completed by default"""
        task = manager.add_task("New task")
        assert task.completed == False

    def test_add_task_increments_task_count(self, manager):
        """Test that adding tasks increases the task list size"""
        assert len(manager.get_all_tasks()) == 0
        manager.add_task("Task 1")
        assert len(manager.get_all_tasks()) == 1
        manager.add_task("Task 2")
        assert len(manager.get_all_tasks()) == 2

    def test_add_task_with_empty_description_raises_error(self, manager):
        """Test that empty description raises ValueError"""
        with pytest.raises(ValueError, match="empty"):
            manager.add_task("")

    def test_add_task_with_whitespace_description_raises_error(self, manager):
        """Test that whitespace-only description raises ValueError"""
        with pytest.raises(ValueError, match="empty"):
            manager.add_task("   ")

    def test_add_task_with_too_long_description_raises_error(self, manager):
        """Test that description >500 chars raises ValueError"""
        description = "a" * 501
        with pytest.raises(ValueError, match="500 characters"):
            manager.add_task(description)


class TestTaskManagerGetTaskById:
    """Tests for retrieving tasks by ID"""

    @pytest.fixture
    def manager(self):
        """TaskManager with some pre-existing tasks"""
        mgr = TaskManager()
        mgr.add_task("Task 1", Priority.HIGH)
        mgr.add_task("Task 2", Priority.MEDIUM)
        mgr.add_task("Task 3", Priority.LOW)
        return mgr

    def test_get_task_by_id_returns_correct_task(self, manager):
        """Test that get_task_by_id returns the right task"""
        task = manager.get_task_by_id(2)
        assert task is not None
        assert task.id == 2
        assert task.description == "Task 2"
        assert task.priority == Priority.MEDIUM

    def test_get_task_by_id_returns_none_for_invalid_id(self, manager):
        """Test that invalid ID returns None"""
        task = manager.get_task_by_id(999)
        assert task is None

    def test_get_task_by_id_returns_none_for_negative_id(self, manager):
        """Test that negative ID returns None"""
        task = manager.get_task_by_id(-1)
        assert task is None

    def test_get_task_by_id_returns_none_for_zero_id(self, manager):
        """Test that zero ID returns None"""
        task = manager.get_task_by_id(0)
        assert task is None

    def test_get_task_by_id_after_deletion_returns_none(self, manager):
        """Test that deleted task ID returns None"""
        manager.delete_task(2)
        task = manager.get_task_by_id(2)
        assert task is None


class TestTaskManagerGetAllTasks:
    """Tests for retrieving all tasks"""

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self):
        """Test that get_all_tasks returns [] for new manager"""
        manager = TaskManager()
        tasks = manager.get_all_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_get_all_tasks_returns_all_added_tasks(self):
        """Test that get_all_tasks returns all tasks in order"""
        manager = TaskManager()
        manager.add_task("First")
        manager.add_task("Second")
        manager.add_task("Third")

        tasks = manager.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].description == "First"
        assert tasks[1].description == "Second"
        assert tasks[2].description == "Third"

    def test_get_all_tasks_maintains_insertion_order(self):
        """Test that tasks are returned in creation order"""
        manager = TaskManager()
        task1 = manager.add_task("A")
        task2 = manager.add_task("B")
        task3 = manager.add_task("C")

        tasks = manager.get_all_tasks()
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task3.id

    def test_get_all_tasks_excludes_deleted_tasks(self):
        """Test that deleted tasks don't appear in get_all_tasks"""
        manager = TaskManager()
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        manager.add_task("Task 3")

        manager.delete_task(2)

        tasks = manager.get_all_tasks()
        assert len(tasks) == 2
        assert all(t.id != 2 for t in tasks)
