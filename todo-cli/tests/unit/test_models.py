"""Unit tests for Task model and Priority enum"""
import pytest
from datetime import datetime
from todo.models import Task, Priority


class TestPriorityEnum:
    """Tests for Priority enum"""

    def test_priority_has_high_value(self):
        """Test that Priority.HIGH exists with correct value"""
        assert Priority.HIGH.value == "High"

    def test_priority_has_medium_value(self):
        """Test that Priority.MEDIUM exists with correct value"""
        assert Priority.MEDIUM.value == "Medium"

    def test_priority_has_low_value(self):
        """Test that Priority.LOW exists with correct value"""
        assert Priority.LOW.value == "Low"

    def test_priority_enum_has_three_values(self):
        """Test that Priority enum has exactly 3 values"""
        assert len(Priority) == 3

    def test_priority_values_are_unique(self):
        """Test that all priority values are distinct"""
        values = [p.value for p in Priority]
        assert len(values) == len(set(values))


class TestTaskDataclass:
    """Tests for Task dataclass"""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified"""
        now = datetime.now()
        task = Task(
            id=1,
            description="Buy groceries",
            priority=Priority.HIGH,
            completed=False,
            created_at=now
        )
        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.priority == Priority.HIGH
        assert task.completed == False
        assert task.created_at == now

    def test_task_default_priority_is_medium(self):
        """Test that task uses MEDIUM as default priority"""
        task = Task(id=1, description="Test task")
        assert task.priority == Priority.MEDIUM

    def test_task_default_completed_is_false(self):
        """Test that task defaults to incomplete"""
        task = Task(id=1, description="Test task")
        assert task.completed == False

    def test_task_created_at_auto_generated(self):
        """Test that created_at is automatically set to current time"""
        task = Task(id=1, description="Test task")
        assert isinstance(task.created_at, datetime)
        # Should be very recent (within 1 second)
        time_diff = (datetime.now() - task.created_at).total_seconds()
        assert time_diff < 1

    def test_task_empty_description_raises_error(self):
        """Test that empty description raises ValueError"""
        with pytest.raises(ValueError, match="empty"):
            Task(id=1, description="")

    def test_task_whitespace_only_description_raises_error(self):
        """Test that whitespace-only description raises ValueError"""
        with pytest.raises(ValueError, match="empty"):
            Task(id=1, description="   ")

    def test_task_description_max_length_500_chars(self):
        """Test that 500-character description is accepted"""
        description = "a" * 500
        task = Task(id=1, description=description)
        assert len(task.description) == 500

    def test_task_description_exceeds_500_chars_raises_error(self):
        """Test that description >500 characters raises ValueError"""
        description = "a" * 501
        with pytest.raises(ValueError, match="500 characters"):
            Task(id=1, description=description)

    def test_task_negative_id_raises_error(self):
        """Test that negative ID raises ValueError"""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=-1, description="Test task")

    def test_task_zero_id_raises_error(self):
        """Test that zero ID raises ValueError"""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=0, description="Test task")

    def test_task_non_string_description_raises_error(self):
        """Test that non-string description raises TypeError"""
        with pytest.raises(TypeError, match="string"):
            Task(id=1, description=123)

    def test_task_non_priority_enum_raises_error(self):
        """Test that invalid priority type raises TypeError"""
        with pytest.raises(TypeError, match="Priority enum"):
            Task(id=1, description="Test", priority="High")

    def test_task_non_boolean_completed_raises_error(self):
        """Test that non-boolean completed value raises TypeError"""
        with pytest.raises(TypeError, match="boolean"):
            Task(id=1, description="Test", completed="true")
